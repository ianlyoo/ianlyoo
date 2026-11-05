---
name: independent-verification
description: Use for final acceptance, complicated invariants, edge cases, regression, model correctness, API authorization or offline local test generation.
---

# Independent verification

Create `VERIFICATION_MATRIX.md` by mapping **every mandatory requirement** to location, test/check command, observed result and status (verified/failed/unverified). Avoid a self-referential checker that copies the production algorithm. For numerical output, compare to small brute-force cases or independently recomputed constraints.

Test happy path, adversarial input, broken references, failed DB writes, process restart, time zones/date rollovers, multi-user authorization and stale UI states as applicable. Keep objective tests separate from visual/manual checks.

Do not claim tests were run when they were not; if browser auto-operation is prohibited, manually inspect in provided preview and mark programmatic UI testing not performed. In the final 10 minutes prioritize mandatory output/schema validation and submission file existence.
