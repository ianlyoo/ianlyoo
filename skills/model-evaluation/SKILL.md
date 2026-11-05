---
name: model-evaluation
description: Use for predictions, classification, forecasting, simulations, ranking models, uncertainty, scenarios, feature selection or metric justification.
---

# Evaluation before claims

1. State target and what is actually being predicted; specify horizon, unit, labels and allowed features.
2. Choose a transparent baseline first. Explain why MAE, RMSE, MAPE, log loss, F1, accuracy, calibration or another metric matches business cost. Avoid metrics invalid for zero/rare events.
3. Freeze a valid split (time-based, group-based or temporal holdout as appropriate). Check target leakage and label availability.
4. Train/compare only after recording settings and seed. Evaluate on held-out data.
5. Show errors by meaningful slice; check operational constraints and sensitivity, not only aggregate score.
6. Distinguish model forecast from actual measured value; communicate uncertainty honestly.
7. Document why this algorithm/threshold was selected, what alternatives were ruled out and what would invalidate it.

Never invent benchmark improvement or metrics not calculated from current task data.
