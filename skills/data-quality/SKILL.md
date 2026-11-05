---
name: data-quality
description: Use for CSV, Excel, databases, ingestion, schema validation, temporal joins, deduplication, missing values, reference integrity and dataset switching.
---

# Data trust gate

Build a data contract from real inputs: file presence, schema types, nullability, unique keys, foreign keys, domain constraints, units, time zones, date grain and bidirectional relations where relevant. Inspect data before asserting distributions. Report invalid rows with actionable diagnostics.

Separate **validation** from **activation**. A rejected dataset must not mutate active state. Use atomic persistence and regression-test partial failures, out-of-date plans, restart consistency and version mismatch.

For ML data: detect leakage, point-in-time joins, time-dependent groups and skew; no random split where time-order matters. Never replace all actual users with historic utilization unless explicitly allowed.

Capture the evidence and limitations in `DECISION_LOG.md`. Never send files, rows, metadata or user-supplied prompts to external tools.
