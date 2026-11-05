# Adaptive 4-agent Codex hackathon harness

Reusable, task-driven **main + 3 workers** setup for timed engineering challenges. **Not a solver or a copy of any confidential exam prompt.** All included content is generic and safe to publish.

## Start from an official task workspace

From the exam workspace (which contains its official `README.md`), in the **provided platform's terminal**:

```bash
git clone --depth 1 --single-branch -b hackathon-harness \
  https://github.com/ianlyoo/ianlyoo.git /tmp/hackathon-harness
python3 /tmp/hackathon-harness/tools/harness.py setup \
  --workspace . --task README.md --superpowers --external
```

The first command downloads this public harness. The second reads the **local** task, recommends a profile, sets up `.codex/agents/`, `.codex/config.toml` (cap 3 spawned threads), `.agents/skills/`, documents and approved public skill installations. It does **not** upload the task, alter the provided `README.md`, or change the platform's controls. **If the installer needs a Codex reload to discover newly installed skills/agents, reload within permitted UI.**

> **Node dependency:** `--external` needs Node.js and `npx` (current `skills` CLI typically requires Node >=22.20). If unavailable, omit `--external` and let the task proceed using bundled local skills. `--superpowers` requires Git and fetches the public Superpowers repository. These are optional; failures do not block the local harness.

### Shortest message to type in Codex

**`README 읽고 .hackathon/START.md 따라 4에이전트로 풀어. 판단 근거는 DECISION_LOG.md에 계속 기록해.`**

If the task root already has an `AGENTS.md`, add **`.hackathon/PROJECT_AGENT_RULES.md도 읽어.`** (the harness keeps that file untouched).

## Run inspection without changing anything

```bash
python3 /tmp/hackathon-harness/tools/harness.py inspect --task README.md
python3 /tmp/hackathon-harness/tools/harness.py setup --workspace . --task README.md --dry-run
```

Main may override the heuristic after reading the actual task:

```bash
python3 /tmp/hackathon-harness/tools/harness.py setup \
  --workspace . --task README.md --profile prediction-ml \
  --agents data-engineer,ml-engineer,frontend-engineer \
  --add-external impeccable --superpowers --external
```

**Important:** setup is deliberately non-destructive. It will **not overwrite** existing `AGENTS.md`, config, role files, or logs; to switch profiles on an already-bootstrapped workspace, inspect and adjust the specific generated files yourself. Do not rerun setup expecting a profile switch to replace prior files.

## Available task profiles

| Profile | When it fits | Main + 3 workers |
|---|---|---|
| `fullstack-analytics` | Data, operational rules and interactive dashboard | data, optimization, frontend |
| `prediction-ml` | Forecasting/classification, time-series, ML evaluation | data, ML, independent verification |
| `optimization-operations` | Routing, allocation, rostering, optimization | data, optimization, independent verification |
| `web-product` | UI-heavy multi-role web app | frontend, backend, independent verification |
| `data-engineering` | CSV/SQL, ETL, versioning and data quality | data, backend, independent verification |
| `agent-automation` | Tool-driven workflows / MCP / orchestration | tooling, backend, independent verification |
| `document-intelligence` | PDF/Excel/DOCX extraction and reports | document, data, independent verification |
| `backend-service` | APIs, auth, persistence, deployment readiness | backend, data, independent verification |
| `algorithmic` | Algorithmic correctness/complexity | algorithm, independent verification, optimization |
| `simulation-decision` | Scenarios, risk, Monte Carlo, what-if | data, simulation, independent verification |
| `security-audit` | Security architecture, threat models, access control | security, backend, independent verification |

When a UI and forecasting/optimization are mixed, the router also substitutes a frontend worker even if a single profile name is imperfect. The **main must confirm** actual task requirements, adapt roles, and cap total agents at four.

## Skills approach

Always-on self-authored skills (conditional local copies): `decision-journal`, `data-quality`, `model-evaluation`, `optimization-audit`, `interface-contract`, `independent-verification`, `submission-gate`. They need no external AI service and do not include any private exam content.

Public skills are fetched **only on demand** if relevant: Superpowers (or Codex `/plugins`), Impeccable, Vercel React Best Practices and Web Design Guidelines, Trail of Bits modern-python/property-based-testing, Anthropic public MCP/document skills. `--external` opts into installation; the selection avoids React and format-specific skills unless task text indicates them. A human/agent can supply `--add-external` after choosing a framework. The installer disables `skills` CLI's anonymous telemetry through `DISABLE_TELEMETRY=1`.

The install commands are in `profiles.json`; the executable installer logs every command it runs. External skills and their dependencies can change; inspect them before execution. Their use never grants permission to call a prohibited model, send task data, push to GitHub, automate a proctored browser, or bypass platform controls.

## Decision documents created in the exam workspace

- `DECISION_LOG.md`: decisions, why chosen, assumptions, data evidence, rejected alternatives, tradeoffs, tests, fallback. Updated at milestones, not only at the end.
- `EXPLAINABILITY_NOTES.md`: concise participant-facing "why" study guide (before human-only questions).
- `VERIFICATION_MATRIX.md`: exact requirements → code → independent evidence → status.
- `WORK_PLAN.md`: time budget and file ownership, preventing simultaneous edits.

Agents **must never invent participant intent or stakeholder statements**. They should distinguish task-stated facts, validated data, agent-proposed engineering choices, participant confirmations and unresolved assumptions. Follow-up answers are human-only when the contest says so; never use AI in that phase.

## Important exam constraints

- No outbound task files, prompts, generated code or results. No Git Push. Public Git Clone/download is only for permitted reusable assets.
- Use only the provided Codex model; do not attach external model providers or API keys.
- No Computer Use / automated browser control in a proctored environment; use permitted local programmatic tests and platform browser preview manually.
- Do not rewrite official `README.md`, provided schemas, datasets or organizer rules.
- Project config only recommends **max 3 spawned agents** (main + 3). If proctoring/platform prevents agent spawning or skill installs, do **not** bypass its settings.

## Offline tests (do not install external skills)

```bash
python3 -m unittest discover -s tests -v
```

## Sources / acknowledgements

[Superpowers](https://github.com/obra/superpowers) · [Impeccable](https://github.com/pbakaus/impeccable) · [Vercel agent skills](https://github.com/vercel-labs/agent-skills) · [Trail of Bits skills](https://github.com/trailofbits/skills) · [Anthropic public skills](https://github.com/anthropics/skills) · [Agent Skills format](https://agentskills.io/).

This repository contains only original routing/configuration/templates. Third-party skills are not vendored or relicensed. No guarantees of contest compliance beyond the public rules; read the specific task and platform prompts.
