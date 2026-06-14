# Difficulty-wise Results

| method | n | executable_rate | optimal_rate | objective_accuracy | structure_completeness | inventory_balance_accuracy | constraint_coverage | average_runtime_sec | average_repair_feedback_count | group | difficulty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Best-of-K | 3 | 1.0000 | 1.0000 | 0.0000 | 0.6000 | 0.0000 | 0.6000 | 0.4027 | 2.0000 | easy | easy |
| Best-of-K | 6 | 1.0000 | 1.0000 | 0.0000 | 0.6857 | 1.0000 | 0.6667 | 0.4021 | 2.0000 | hard | hard |
| Best-of-K | 6 | 1.0000 | 1.0000 | 0.0000 | 0.8333 | 1.0000 | 0.8000 | 0.4114 | 1.0000 | medium | medium |
| Direct | 3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.3842 | 0.0000 | easy | easy |
| Direct | 6 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.3961 | 0.0000 | hard | hard |
| Direct | 6 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.4064 | 0.0000 | medium | medium |
| OptArgus-like Audit | 3 | 1.0000 | 1.0000 | 0.0000 | 0.6000 | 0.0000 | 0.6000 | 0.4027 | 2.0000 | easy | easy |
| OptArgus-like Audit | 6 | 1.0000 | 1.0000 | 0.0000 | 0.6857 | 1.0000 | 0.6667 | 0.4021 | 2.0000 | hard | hard |
| OptArgus-like Audit | 6 | 1.0000 | 1.0000 | 0.0000 | 0.8333 | 1.0000 | 0.8000 | 0.4114 | 1.0000 | medium | medium |
| OptiRepair-like Repair-Prompt | 3 | 1.0000 | 1.0000 | 0.0000 | 0.6000 | 0.0000 | 0.6000 | 0.4027 | 2.0000 | easy | easy |
| OptiRepair-like Repair-Prompt | 6 | 1.0000 | 1.0000 | 0.0000 | 0.6857 | 1.0000 | 0.6667 | 0.4021 | 2.0000 | hard | hard |
| OptiRepair-like Repair-Prompt | 6 | 1.0000 | 1.0000 | 0.0000 | 0.8333 | 1.0000 | 0.8000 | 0.4114 | 1.0000 | medium | medium |
| ReplenishVerifier-Full | 3 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.4711 | 0.0000 | easy | easy |
| ReplenishVerifier-Full | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4358 | 0.0000 | hard | hard |
| ReplenishVerifier-Full | 6 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 0.4248 | 0.0000 | medium | medium |
| ReplenishVerifier-Repair | 3 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.4711 | 0.0000 | easy | easy |
| ReplenishVerifier-Repair | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4358 | 0.0000 | hard | hard |
| ReplenishVerifier-Repair | 6 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 0.4248 | 0.0000 | medium | medium |
| SIRL-like LP-Stats | 3 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.4711 | 0.0000 | easy | easy |
| SIRL-like LP-Stats | 6 | 1.0000 | 1.0000 | 0.6667 | 0.8524 | 1.0000 | 0.8611 | 0.4144 | 0.8333 | hard | hard |
| SIRL-like LP-Stats | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4388 | 0.0000 | medium | medium |
| Solver-Filter | 3 | 1.0000 | 1.0000 | 0.0000 | 0.6000 | 0.0000 | 0.6000 | 0.4027 | 2.0000 | easy | easy |
| Solver-Filter | 6 | 1.0000 | 1.0000 | 0.0000 | 0.6857 | 1.0000 | 0.6667 | 0.4021 | 2.0000 | hard | hard |
| Solver-Filter | 6 | 1.0000 | 1.0000 | 0.0000 | 0.8333 | 1.0000 | 0.8000 | 0.4114 | 1.0000 | medium | medium |
| Structure-Only | 3 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.4711 | 0.0000 | easy | easy |
| Structure-Only | 6 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.4358 | 0.0000 | hard | hard |
| Structure-Only | 6 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 0.4248 | 0.0000 | medium | medium |
