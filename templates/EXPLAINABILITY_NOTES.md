# Explainability notes — participant study sheet (BEFORE submission)

> These are preparation notes. The participant must understand and independently answer any human-only follow-up. Do not generate or use AI answers after the prohibited-AI boundary.

## 1. What problem was actually solved?
- Task's objective and target user:
- Non-negotiable requirements (and where verified):
- Out-of-scope items:

## 2. Why this solution?
- Architecture and alternatives:
- Which preferences are participant-confirmed vs agent-proposed?
- What assumptions were made when business context was unknown?

## 3. Why these data and methods?
- Dataset origins, joins, missingness, validation:
- Predicted quantity vs historical/actual quantity:
- Baseline, chosen method/model/algorithm and rejected choices:
- Metric, objective function, weights, thresholds and units:
- Leakage, drift, bias, sensitivity and uncertainty:

## 4. What happens when things go wrong?
- Invalid data and atomic rollback:
- Authorization and access control:
- Capacity/resource/operating-rule violations:
- Service restart, outage or inconsistent dataset version:
- Model failure or poor extrapolation:

## 5. Why can this implementation be trusted?
- Exact tests executed and outcomes (never invented):
- Independently checked constraints and metrics:
- Remaining unverified areas and limitations:
- Actual user/stakeholder confirmations (quote/paraphrase from in-platform context only):

## 6. Six likely oral/written-review themes to rehearse unaided
1. Why this objective, metric or algorithm?
2. What real data backs the conclusion and what is assumed?
3. How did you choose among alternatives and what tradeoff was accepted?
4. How are incorrect inputs, permission boundaries and failure cases handled?
5. What did the AI implement and what did you personally decide or verify?
6. What evidence supports correctness and how would you improve the result?

> For each answer, cite a real file, code path, test, or `DECISION_LOG.md` entry. Don't memorize fabricated generic justifications.
