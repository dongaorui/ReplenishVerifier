# Ablation Results

| method | n | executable_rate | optimal_rate | objective_accuracy | structure_completeness | inventory_balance_accuracy | constraint_coverage | average_runtime_sec | average_repair_feedback_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ReplenishVerifier-Full | 15 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4795 | 0.0000 |
| ReplenishVerifier-Repair | 15 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4795 | 0.0000 |
| Solver-Filter | 15 | 1.0000 | 1.0000 | 1.0000 | 0.9600 | 1.0000 | 0.9630 | 0.4731 | 0.2000 |
| Structure-Only | 15 | 1.0000 | 1.0000 | 0.8000 | 1.0000 | 1.0000 | 1.0000 | 0.4689 | 0.0000 |
