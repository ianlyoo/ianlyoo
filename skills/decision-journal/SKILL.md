---
name: decision-journal
description: Use whenever choosing an architecture, objective, threshold, validation rule, model, fallback, shortcut or significant tradeoff during a timed engineering task.
---

# Decision journal discipline

Before implementing a nontrivial decision, add a short entry to `DECISION_LOG.md` using the template. Record: **decision, real objective, requirement/evidence, alternatives, rationale, measurable tradeoffs, uncertainty, validation, fallback, owner, timestamp and status**. Do not backfill guessed motives or claim user assent.

Use `EXPLAINABILITY_NOTES.md` as a separate concise human-facing account: Why this solution? Why this data treatment? Why this metric? What can go wrong and how recover? What did the operator actually confirm? Keep factual origin tags `TASK`, `DATA`, `STAKEHOLDER`, `ENGINEERING_ASSUMPTION`, `TEST`. Include rejected alternatives.

When changing an earlier choice, mark it `superseded`; never silently rewrite history. Log only meaningful decisions to avoid wasting time. At checkpoints (initial contract, first working vertical slice, integration, handoff) make main consolidate the journal and ask user about any critical ambiguous assumption using platform-approved communication.

**Do not use AI for restricted post-submission written responses.** These records are preparation material for the participant's own understanding before submission, not text to paste into a restricted assessment.
