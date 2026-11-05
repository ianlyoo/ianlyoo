---
name: optimization-audit
description: Use for route planning, allocation, scheduling, logistics, constraints, objective functions, heuristics or numerical optimization.
---

# Optimization design & audit

Classify constraints into **hard** (must always hold) and **soft** (optimization tradeoffs). Examples: capacities, exact assignment, allowed nodes, time windows, forbidden combinations vs travel time, distance, wait, fairness and resource count. The exact constraints come from the task; examples are not specifications.

Explicitly write objective vector and scalarization if used, weight and unit interpretation; consider lexicographic constraints before arbitrary weighted sums. Compare against a trivial feasible baseline. Preserve reproducibility; tie-breaking must be deterministic.

Independently recalculate from original input for every generated result: all required assignments, no prohibited assignment, resource capacity at every interval, start/end windows, direction-sensitive edge weights, date and time boundary behavior, and reproducibility. Check feasibility before calling result optimized.

Measure objective, feasible rate, runtime and tradeoffs; never label a heuristic globally optimal without proof. Log stakeholder-verified rules separately from engineering assumptions.
