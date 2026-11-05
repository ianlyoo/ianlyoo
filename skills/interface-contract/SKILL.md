---
name: interface-contract
description: Use when multiple agents implement frontend/backend/data tool boundaries, API contracts, schema versions, role-based permissions or authentication.
---

# Contract-first parallel delivery

Before delegating: main defines minimal shared schema/API/endpoints, ownership of each file/folder, error format and state/version semantics. Subagents do not edit the same files concurrently. Main owns shared contract changes and integration.

Backend enforces authorization. Frontend hiding buttons is not access control. Test invalid ID, invalid role, stale data, malformed payload, partial persistence, restart, and mismatch between generated results and active input version.

For UX: no fake success on failed responses, no stale results presented as new, a distinguishable loading/error/empty state, and keyboard-accessible important controls.

Every changed contract requires notifying affected agents and updating acceptance matrix.
