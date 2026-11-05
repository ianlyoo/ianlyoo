# Work plan — main + 3 agents, 180-minute default budget

> This is a starting budget, not an official allocation. Adapt for the actual exam timeline.

| Phase | Typical minutes | Main responsibility | Exit condition |
|---|---:|---|---|
| Requirements & routing | 0-15 | confirm hard criteria, data, business unknowns | matrix + contracts + 3 scoped delegations |
| Parallel vertical slice | 15-105 | integrate continuously, own shared APIs | mandatory paths can run end-to-end |
| Integration & robustness | 105-145 | fix cross-module issues | data/model/UI and persistence consistent |
| Verification & documentation | 145-170 | independent checks, decision log | evidence-supported acceptance |
| Submit buffer | 170-180 | inspect files, submit | no incomplete writes or missing artifacts |

## Roles, interfaces and ownership (update before spawn)
- Main: architecture, task-facing communication, shared contracts, auth/API integration, final verification, decision docs.
- Worker 1: [specific files/contract]
- Worker 2: [specific files/contract]
- Worker 3: [specific files/contract]

## Integration contract
- Inputs and source of truth:
- Shared API/DB schema and versioning:
- Error types and status response:
- Definition of done for each worker:
- Fallback if worker is slow or unavailable:
