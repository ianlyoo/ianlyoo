# Requirement-to-evidence matrix

> Add every hard requirement before coding. "Implemented" is NOT "verified". Tests and results must be real.

| ID | Source/requirement | Implemented at | Test/oracle | Result/evidence | Status |
|---|---|---|---|---|---|
| R-01 | [from official task] | [file:line] | [command or manual] | [observed] | NOT TESTED |

## Edge-case checklist (adapt to actual task)
- [ ] Invalid/missing input columns, broken foreign keys, empty data
- [ ] Time/date boundary, time zones, calendar/holiday rules (if relevant)
- [ ] Zero, missing, negative, duplicated or extreme numerical inputs
- [ ] Hard constraints independently recomputed
- [ ] Unauthorized API access and cross-user data exposure
- [ ] Transaction rollback, stale plan/version and service restart
- [ ] Regression across alternate datasets, not only provided baseline
- [ ] Browser preview/manual accessibility for UI where permitted
- [ ] Submission schema, required filenames, environment, container/build
- [ ] Document evidence and participant explanation are consistent

## Acceptance status
- Verified:
- Failed:
- Not tested / known risks:
