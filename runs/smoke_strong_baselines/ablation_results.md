# Ablation Results

| method | n | executable_rate | optimal_rate | objective_accuracy | structure_completeness | inventory_balance_accuracy | constraint_coverage | average_runtime_sec | average_repair_feedback_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OptArgus-like Audit | 15 | 1.0000 | 1.0000 | 0.0000 | 0.7276 | 1.0000 | 0.7037 | 0.4059 | 1.6000 |
| OptiRepair-like Repair-Prompt | 15 | 1.0000 | 1.0000 | 0.0000 | 0.7276 | 1.0000 | 0.7037 | 0.4059 | 1.6000 |
| ReplenishVerifier-Full | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4385 | 0.0000 |
| ReplenishVerifier-Repair | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4385 | 0.0000 |
| SIRL-like LP-Stats | 15 | 1.0000 | 1.0000 | 0.8667 | 0.9410 | 1.0000 | 0.9383 | 0.4355 | 0.3333 |
| Solver-Filter | 15 | 1.0000 | 1.0000 | 0.0000 | 0.7276 | 1.0000 | 0.7037 | 0.4059 | 1.6000 |
| Structure-Only | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4385 | 0.0000 |
