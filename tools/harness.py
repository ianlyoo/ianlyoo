#!/usr/bin/env python3
"""Offline, stdlib-only task router and Codex harness bootstrap.

Never sends task content to any service. The optional --external installer
only fetches PUBLIC skills; nothing from workspace is supplied to those tools.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "profiles.json").read_text(encoding="utf-8"))
AGENT_ROLES = {x.stem for x in (ROOT / "agent_roles").glob("*.toml")}
MANDATORY_SKILLS = {"decision-journal", "independent-verification", "submission-gate"}
MODEL_HINT = "Use the platform-provided Codex model (Sol 6.1 if available), without external providers."

CAPS = {
    "ui": ("ui", "ux", "react", "next.js", "프론트", "웹", "dashboard", "대시보드", "화면", "사용자", "login", "로그인", "visualization", "시각화"),
    "data": ("데이터", "data", "csv", "xls", "sql", "db", "database", "데이터셋", "etl", "pipeline"),
    "ml": ("예측", "prediction", "forecast", "time series", "시계열", "machine learning", "classification", "회귀", "모델링", "학습", "predict"),
    "optimization": ("최적화", "optimization", "route", "routing", "배정", "스케줄", "목적함수", "constraint", "제약", "vehicle", "차량", "allocat", "schedule"),
    "agent": ("mcp", "에이전트", "agent", "workflow", "오케스트레이션", "tool calling", "자동화"),
    "document": ("pdf", "xlsx", "docx", "pptx", "문서", "보고서", "document", "invoice"),
    "security": ("보안", "security", "취약점", "threat", "privacy", "rbac"),
    "simulation": ("simulation", "시뮬레이션", "monte carlo", "민감도", "what-if", "scenario", "시나리오"),
}


def read_task(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Task file not found: {path}. Pass --task <path>.")
    if path.stat().st_size > 3_000_000:
        raise SystemExit("Task file too large for routing; use a plain text requirements file.")
    return path.read_text(encoding="utf-8-sig", errors="replace")


def match_count(text: str, term: str) -> int:
    """Count one hit per term, not frequency, to avoid verbose text bias."""
    term=term.lower()
    if re.fullmatch(r"[a-z0-9_\-]+", term):
        return int(bool(re.search(r"(?<![a-z0-9_])" + re.escape(term) + r"(?![a-z0-9_])", text)))
    return int(term in text)


def route(text: str) -> dict:
    lowered = text.lower()
    scores = {}
    evidence = {}
    for slug, profile in CONFIG["profiles"].items():
        matches = [x for x in profile["signals"] if match_count(lowered,x)]
        scores[slug] = len(matches)
        evidence[slug] = matches
    capabilities = {k:sum(match_count(lowered,s) for s in synonyms) for k,synonyms in CAPS.items()}
    ui, data = capabilities["ui"]>=2, capabilities["data"]>=2
    if ui and data:
        scores["fullstack-analytics"] += 5
    if ui and capabilities["ml"]>=2:
        scores["fullstack-analytics"] += 4
    if ui and capabilities["optimization"]>=2:
        scores["fullstack-analytics"] += 4
    if capabilities["ml"]>=2 and capabilities["optimization"]>=2 and not ui:
        scores["prediction-ml"] += 2
    if capabilities["document"]>=3 and not ui:
        scores["document-intelligence"] += 3
    if capabilities["agent"]>=2 and not ui:
        scores["agent-automation"] += 3
    ordered=sorted(scores,key=lambda slug:(-scores[slug],slug))
    profile = ordered[0] if scores[ordered[0]] else "backend-service"
    agents=list(CONFIG["profiles"][profile]["agents"])
    # Refine hybrid profiles using read-only routing: the main agent retains final say.
    if ui and capabilities["ml"]>=2 and capabilities["optimization"]<2:
        agents=["data-engineer","ml-engineer","frontend-engineer"]
    elif ui and capabilities["optimization"]>=2:
        agents=["data-engineer","optimization-engineer","frontend-engineer"]
    elif ui and capabilities["agent"]>=2 and capabilities["data"]<3:
        agents=["tooling-engineer","backend-engineer","frontend-engineer"]
    elif ui and capabilities["document"]>=3:
        agents=["document-engineer","data-engineer","frontend-engineer"]
    elif ui and capabilities["security"]>=3:
        agents=["security-engineer","backend-engineer","frontend-engineer"]
    return {"profile":profile,"agents":agents,"scores":scores,"evidence":evidence,
            "capabilities":capabilities,"ranked":ordered[:4],"recommendations_only":True}


def external_selection(profile: dict, capabilities: dict, task: str) -> list[str]:
    chosen = list(profile.get("external_skills", []))
    # Only add expensive/specific skills when task clearly calls for them.
    for skill in profile.get("optional_skills", []):
        s=task.lower()
        if skill == "mcp-builder" and "mcp" in s:
            chosen.append(skill)
        elif skill == "docx" and ".docx" in s:
            chosen.append(skill)
        elif skill == "pptx" and ".pptx" in s:
            chosen.append(skill)
        elif skill == "secure-workflow-guide" and ("threat" in s or "위협" in s):
            chosen.append(skill)
    # Design skills not useful without a frontend requirement.
    if capabilities["ui"] < 2:
        chosen = [x for x in chosen if x not in ("impeccable", "web-design-guidelines", "react-best-practices")]
    # Do not presume React or Next; main can explicitly override after choosing a stack.
    if "react" not in task.lower() and "next.js" not in task.lower():
        chosen = [x for x in chosen if x!="react-best-practices"]
    if "python" not in task.lower() and "파이썬" not in task.lower():
        chosen = [x for x in chosen if x!="modern-python"]
    if "xlsx" not in task.lower() and ".xls" not in task.lower():
        chosen = [x for x in chosen if x!="xlsx"]
    if "pdf" not in task.lower():
        chosen = [x for x in chosen if x!="pdf"]
    return list(dict.fromkeys(chosen))


def write_if_missing(path:Path, contents:str)->bool:
    if path.exists():
        print(f"KEEP (not overwritten): {path}")
        return False
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(contents,encoding="utf-8")
    print(f"CREATE {path}")
    return True


def decision_docs(workspace:Path)->None:
    for name in ("DECISION_LOG.md","EXPLAINABILITY_NOTES.md","VERIFICATION_MATRIX.md","WORK_PLAN.md"):
        src=ROOT/"templates"/name
        write_if_missing(workspace/name,src.read_text(encoding="utf-8"))


def install_local_skills(workspace:Path,skills:list[str])->None:
    out=workspace/".agents"/"skills"
    for name in skills:
        src=ROOT/"skills"/name
        dst=out/name
        if not dst.exists():
            shutil.copytree(src,dst)
            print(f"SKILL {name}")
        else:
            print(f"KEEP installed skill {name}")


def add_superpowers(workspace:Path, enabled:bool)->None:
    if not enabled:
        return
    base=workspace/".hackathon"/"vendor"/"superpowers"
    if not (base/"skills").is_dir():
        base.parent.mkdir(parents=True,exist_ok=True)
        command=["git","clone","--depth","1","https://github.com/obra/superpowers.git",str(base)]
        print("FETCH public Superpowers repository")
        try:
            subprocess.run(command, check=True,timeout=95,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        except Exception as exc:
            print(f"WARNING: Superpowers download not completed: {exc}. Use Codex /plugins to install or retry.")
            return
    dst=workspace/".agents"/"skills"/"superpowers"
    if dst.exists() or dst.is_symlink():
        return
    dst.parent.mkdir(parents=True,exist_ok=True)
    try:
        dst.symlink_to(os.path.relpath(base/"skills",dst.parent),target_is_directory=True)
    except (OSError,NotImplementedError):
        shutil.copytree(base/"skills",dst)
    print("SKILL Superpowers ready (reload Codex to discover skills if necessary)")


def install_external(workspace:Path, keys:list[str], enabled:bool)->None:
    if not keys:
        print("No external skills selected by conservative task routing.")
        return
    commands=[]
    for key in keys:
        source=CONFIG["external_catalog"][key]
        commands.append(["npx","--yes","skills","add",source["repo"],"--skill",source["skill"],"--agent","codex","--copy","--yes"])
    print("PUBLIC SKILL COMMANDS (only downloads publicly available instructions):")
    for command in commands:
        print("  " + " ".join(command))
    if not enabled:
        print("SKIPPED remote installs (add --external to execute). Bundled skills remain usable offline.")
        return
    env=os.environ.copy()
    env["DISABLE_TELEMETRY"]="1"
    env["npm_config_update_notifier"]="false"
    for command in commands:
        try:
            print(f"INSTALL {command[5]}")
            subprocess.run(command,cwd=workspace,env=env,check=True,timeout=110)
        except Exception as exc:
            print(f"WARNING: external skill install failed: {exc}. Continue with bundled skills.")


def agent_instruction(profile:str,agents:list[str],external:list[str])->str:
    detail=CONFIG["profiles"][profile]
    return f'''# HACKATHON AGENTS — local project context\n\nUse ONLY the actual exam task instructions as authoritative requirements. The public harness is reusable guidance, not a solution to any exam.\n\n## Project profile\n- Selected: `{profile}` — {detail['title']} (provisional; main must verify after reading actual task).\n- Main + exactly 3 workers total (4 agents maximum). Never launch reviewers or nested agents on top of the three workers.\n- Workers (reuse them for future review): {', '.join(agents)}.\n- Main owns contracts, architecture, delegated file ownership, cross-module integration and independent acceptance verification.\n- Model: provided Codex; use Sol 6.1 if available; inherit main's model for subagents. No external models/API keys.\n- Add specialized skills only if relevant. External suggestions: {', '.join(external) if external else 'none'}\n\n## Mandatory process\n1. Read unmodified official README/task and any local schema/data instructions. Extract mandatory deliverables in `VERIFICATION_MATRIX.md`. Identify confirmed facts versus unknowns.\n2. Ask the platform's permitted business contact only to clarify operational ambiguity. No made-up stakeholder replies or user decisions.\n3. Main defines interfaces and file ownership before parallel implementation; workers do not edit shared files at the same time.\n4. Keep `DECISION_LOG.md` continuously: objectives, assumptions, sources, alternatives rejected, selection rationale, validation and fallbacks. Make concise, factual entries.\n5. Update `EXPLAINABILITY_NOTES.md` with what the participant needs to understand: why the model/threshold/algorithm, data rights and permissions, failures, uncertainty, tradeoffs and tested evidence. Record the difference between operator-specified intent and agent-proposed options.\n6. Build a thin end-to-end vertical slice early. Favor mandatory correctness and real tests over optional design polish. Verify optimization/prediction with a separate oracle and honest metrics.\n7. Before completion verify output schema, manual UI preview if required, server-side permissions, data persistence and restart, paths/files, and status. Start submission verification with at least 10 minutes left.\n8. Follow all proctoring constraints: no Computer Use or browser automation, no Git Push, no external task data/results sharing, no bypass of controls or upload restrictions. The local project may install PUBLIC skills if allowed.\n9. After submission, use NO AI to answer restricted human-only follow-up questions. Documents can prepare the participant's own understanding beforehand, never supply post-submission answers.\n\n## Evidence integrity\nMark every claimed outcome as VERIFIED with executed evidence, FAILED, or NOT TESTED. Do not fabricate measurements, citations, conversations, manual actions or tests. Keep decisions auditable.\n\n## Next step\nRead `.hackathon/START.md` for the chosen profile, routes, and exact external skill commands.\n'''


def start_instructions(profile:str,agents:list[str],ranked:list[str],caps:dict,ext:list[str])->str:
    return f'''# START — Time-boxed Codex harness\n\n## Detected task profile\n**{profile}**. Alternatives: {', '.join(ranked)}.\nCapabilities by keyword evidence: {json.dumps(caps,ensure_ascii=False)}.\n\nThis is a heuristic suggestion, NOT an authoritative task interpretation. Main must read the actual task, correct wrong classifications and rerun `setup --profile PROFILE` if necessary. When routing to a hybrid task, main should explicitly pick three workers by capability.\n\n## Spawn limit and roles\nMain + 3 total. Selected workers: {', '.join(agents)}. Codex settings live under `.codex/config.toml` and `.codex/agents/`. If the provided platform blocks agent spawning, do not override its restrictions.\n\n## Skills\nBundled task skills are installed under `.agents/skills/`. Public external suggestions: {', '.join(ext) if ext else '(none by conservative auto-selection)'}.\nSuperpowers can be installed from the public repository via the setup command's `--superpowers` option, or the provided Codex `/plugins` command. With NPM + permission, `--external` installs recommended public skills into the workspace. Restart/reload Codex when discovery requires it. Check each external skill's behavior before execution.\n\n## Task execution\n1. Read official task README and identify mandatory artifacts.\n2. Freeze a minimal contract and define 3 disjoint work packages; delegate simultaneously.\n3. Create a working vertical slice and independent tests; compare data/model/optimization results against task-specified constraints.\n4. Update `DECISION_LOG.md`, `EXPLAINABILITY_NOTES.md`, `VERIFICATION_MATRIX.md` at milestones, not only at the end.\n5. Human-owned intent is not inferable from code; log it as an assumption until explicitly confirmed.\n6. Reserve submission time. No test or answer claims without evidence. No Computer Use, outbound task upload, prohibited API or Git Push.\n\n**The profile is not a substitute for the real grading requirements.**\n'''


def report(route_info:dict,selected:str,agents:list[str],external:list[str],task:Path)->str:
    lines=[f"# Task routing report", "", f"- Source: `{task.name}` (local only; never uploaded)",
           f"- Suggested profile: `{route_info['profile']}`", f"- Configured profile: `{selected}`",
           f"- Agent roles (main + 3): {', '.join(agents)}", f"- External skills: {', '.join(external) if external else '(none)'}", "",
           "## Ranked profiles (keyword heuristic)", ""]
    for slug in route_info["ranked"]:
        matched=", ".join(route_info["evidence"][slug]) or "none"
        lines.append(f"- `{slug}`: score {route_info['scores'][slug]} | signals {matched}")
    lines.extend(["", "**Caution:** The agent must verify the profile against the entire official task; keyword scores are not a substitute for reasoning.",""])
    return "\n".join(lines)


def setup(args)->None:
    workspace=Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        raise SystemExit(f"Workspace must exist: {workspace}")
    task=Path(args.task)
    if not task.is_absolute():
        task=workspace/task
    raw=read_task(task)
    guess=route(raw)
    selected=guess["profile"] if args.profile=="auto" else args.profile
    if selected not in CONFIG["profiles"]:
        raise SystemExit(f"Unknown profile: {selected}")
    p=CONFIG["profiles"][selected]
    agents=guess["agents"] if selected==guess["profile"] else p["agents"]
    if args.agents:
        agents=args.agents.split(",")
    if len(agents)!=3 or len(set(agents))!=3 or not set(agents).issubset(AGENT_ROLES):
        raise SystemExit("--agents must contain EXACTLY 3 unique agent role names from agent_roles/")
    external=external_selection(p,guess["capabilities"],raw)
    if args.add_external:
        for name in args.add_external.split(","):
            if name not in CONFIG["external_catalog"]:
                raise SystemExit(f"Unknown external skill: {name}")
            external.append(name)
    external=list(dict.fromkeys(external))
    built_in=list(dict.fromkeys(list(MANDATORY_SKILLS)+p["built_in_skills"]))
    print(f"Profile: {selected}; main + {len(agents)} workers: {', '.join(agents)}")
    if args.dry_run:
        print(report(guess,selected,agents,external,task))
        return
    cfg_dir=workspace/".codex"
    agent_dir=cfg_dir/"agents"
    agent_dir.mkdir(parents=True,exist_ok=True)
    config_path=cfg_dir/"config.toml"
    write_if_missing(config_path,"# Main agent + 3 spawned workers. Do not bypass platform-managed restrictions.\n[agents]\nmax_concurrent_threads_per_session = 3\n")
    for role in agents:
        write_if_missing(agent_dir/f"{role}.toml",(ROOT/"agent_roles"/f"{role}.toml").read_text(encoding="utf-8"))
    # Existing AGENTS.md may carry task constraints; never replace/append to it.
    write_if_missing(workspace/"AGENTS.md",agent_instruction(selected,agents,external))
    write_if_missing(workspace/".hackathon"/"PROJECT_AGENT_RULES.md",agent_instruction(selected,agents,external))
    write_if_missing(workspace/".hackathon"/"START.md",start_instructions(selected,agents,guess["ranked"],guess["capabilities"],external))
    write_if_missing(workspace/".hackathon"/"ROUTING_REPORT.md",report(guess,selected,agents,external,task))
    decision_docs(workspace)
    install_local_skills(workspace,built_in)
    add_superpowers(workspace,args.superpowers)
    install_external(workspace,external,args.external)
    print("SETUP COMPLETE. No official task files were changed. Read AGENTS.md and .hackathon/START.md.")
    if (workspace/"AGENTS.md").read_text(encoding="utf-8")!=agent_instruction(selected,agents,external):
        print("NOTE: Existing AGENTS.md preserved. Explicitly tell Codex to read .hackathon/PROJECT_AGENT_RULES.md.")


def main():
    parser=argparse.ArgumentParser(description="Safe, task-aware 4-agent Codex hackathon harness")
    sub=parser.add_subparsers(dest="command",required=True)
    ins=sub.add_parser("inspect",help="Offline profile suggestion only; no file changes")
    ins.add_argument("--task",required=True,help="Local task file (e.g. README.md)")
    ins.add_argument("--json",action="store_true")
    run=sub.add_parser("setup",help="Initialize selected harness in an existing exam workspace")
    run.add_argument("--workspace",default=".",help="Existing exam workspace (never overwritten wholesale)")
    run.add_argument("--task",default="README.md",help="Local task instructions file, relative to workspace")
    run.add_argument("--profile",default="auto",choices=["auto",*CONFIG["profiles"]])
    run.add_argument("--agents",default="",help="Optional exact three roles, comma separated")
    run.add_argument("--add-external",default="",help="Additional curated external skill keys, comma separated")
    run.add_argument("--superpowers",action="store_true",help="Clone public Superpowers skill into workspace")
    run.add_argument("--external",action="store_true",help="Install curated PUBLIC skills via npx, if Node is installed")
    run.add_argument("--dry-run",action="store_true",help="Print recommendation only without writing files")
    args=parser.parse_args()
    if args.command=="inspect":
        inf=route(read_task(Path(args.task)))
        if args.json:
            print(json.dumps(inf,indent=2,ensure_ascii=False))
        else:
            print(report(inf,inf["profile"],inf["agents"],external_selection(CONFIG["profiles"][inf["profile"]],inf["capabilities"],read_task(Path(args.task))),Path(args.task)))
    else:
        setup(args)

if __name__=="__main__":
    main()
