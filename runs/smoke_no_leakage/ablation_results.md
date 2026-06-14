# Ablation Results

| method | n | executable_rate | optimal_rate | objective_accuracy | structure_completeness | inventory_balance_accuracy | constraint_coverage | average_runtime_sec | average_repair_feedback_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ReplenishVerifier-Full | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4827 | 0.0000 |
| ReplenishVerifier-Repair | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4827 | 0.0000 |
| Solver-Filter | 15 | 1.0000 | 1.0000 | 0.0000 | 0.7276 | 1.0000 | 0.7037 | 0.4558 | 1.6000 |
| Structure-Only | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4827 | 0.0000 |
