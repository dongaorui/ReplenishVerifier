# Qwen3-8B v2 vs v3 vs v4 MetricsFix Comparison

This report compares formatfix_v2, v3, and the v4_metricsfix rerun using the updated evaluation/diagnostics code.

| method | metric | v2_formatfix | v3 | v4_metricsfix | delta_v4_vs_v2 | delta_v4_vs_v3 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Best-of-K | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Best-of-K | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Best-of-K | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Best-of-K | structure_completeness | 0.7643 | 0.7656 | 0.7656 | +0.0013 | +0.0000 |
| Best-of-K | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Best-of-K | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Consensus only | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Consensus only | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Consensus only | objective_accuracy | 0.6800 | 0.6800 | 0.6800 | +0.0000 | +0.0000 |
| Consensus only | structure_completeness | 0.7643 | 0.7652 | 0.7652 | +0.0009 | +0.0000 |
| Consensus only | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Consensus only | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Direct | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Direct | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Direct | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Direct | structure_completeness | 0.7643 | 0.7643 | 0.7643 | +0.0000 | +0.0000 |
| Direct | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Direct | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| OR-R1-like Voting | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| OR-R1-like Voting | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| OR-R1-like Voting | objective_accuracy | 0.6800 | 0.6800 | 0.6800 | +0.0000 | +0.0000 |
| OR-R1-like Voting | structure_completeness | 0.7643 | 0.7652 | 0.7652 | +0.0009 | +0.0000 |
| OR-R1-like Voting | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| OR-R1-like Voting | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| OptArgus-like Audit | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| OptArgus-like Audit | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| OptArgus-like Audit | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| OptArgus-like Audit | structure_completeness | 0.7643 | 0.7656 | 0.7656 | +0.0013 | +0.0000 |
| OptArgus-like Audit | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| OptArgus-like Audit | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| OptiRepair-like Repair-Prompt | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| OptiRepair-like Repair-Prompt | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| OptiRepair-like Repair-Prompt | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| OptiRepair-like Repair-Prompt | structure_completeness | 0.7643 | 0.7656 | 0.7656 | +0.0013 | +0.0000 |
| OptiRepair-like Repair-Prompt | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| OptiRepair-like Repair-Prompt | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| ReplenishVerifier-Full | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| ReplenishVerifier-Full | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| ReplenishVerifier-Full | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| ReplenishVerifier-Full | structure_completeness | 0.7656 | 0.7656 | 0.7656 | +0.0000 | +0.0000 |
| ReplenishVerifier-Full | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| ReplenishVerifier-Full | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| ReplenishVerifier-Repair | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| ReplenishVerifier-Repair | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| ReplenishVerifier-Repair | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| ReplenishVerifier-Repair | structure_completeness | 0.7656 | 0.7656 | 0.7656 | +0.0000 | +0.0000 |
| ReplenishVerifier-Repair | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| ReplenishVerifier-Repair | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| SIRL-like LP-Stats | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| SIRL-like LP-Stats | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| SIRL-like LP-Stats | objective_accuracy | 0.6400 | 0.6400 | 0.6400 | +0.0000 | +0.0000 |
| SIRL-like LP-Stats | structure_completeness | 0.7643 | 0.7656 | 0.7656 | +0.0013 | +0.0000 |
| SIRL-like LP-Stats | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| SIRL-like LP-Stats | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Solver + Consensus | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Solver + Consensus | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Solver + Consensus | objective_accuracy | 0.6800 | 0.6800 | 0.6800 | +0.0000 | +0.0000 |
| Solver + Consensus | structure_completeness | 0.7643 | 0.7652 | 0.7652 | +0.0009 | +0.0000 |
| Solver + Consensus | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Solver + Consensus | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Solver + Structure | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Solver + Structure | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Solver + Structure | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Solver + Structure | structure_completeness | 0.7656 | 0.7656 | 0.7656 | +0.0000 | +0.0000 |
| Solver + Structure | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Solver + Structure | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Solver + Structure + Consensus | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Solver + Structure + Consensus | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Solver + Structure + Consensus | objective_accuracy | 0.6800 | 0.6800 | 0.6800 | +0.0000 | +0.0000 |
| Solver + Structure + Consensus | structure_completeness | 0.7652 | 0.7652 | 0.7652 | +0.0000 | +0.0000 |
| Solver + Structure + Consensus | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Solver + Structure + Consensus | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Solver only | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Solver only | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Solver only | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Solver only | structure_completeness | 0.7643 | 0.7656 | 0.7656 | +0.0013 | +0.0000 |
| Solver only | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Solver only | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Solver-Filter | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Solver-Filter | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Solver-Filter | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Solver-Filter | structure_completeness | 0.7643 | 0.7656 | 0.7656 | +0.0013 | +0.0000 |
| Solver-Filter | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Solver-Filter | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Structure + Consensus | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Structure + Consensus | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Structure + Consensus | objective_accuracy | 0.6800 | 0.6800 | 0.6800 | +0.0000 | +0.0000 |
| Structure + Consensus | structure_completeness | 0.7652 | 0.7652 | 0.7652 | +0.0000 | +0.0000 |
| Structure + Consensus | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Structure + Consensus | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Structure only | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Structure only | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Structure only | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Structure only | structure_completeness | 0.7656 | 0.7656 | 0.7656 | +0.0000 | +0.0000 |
| Structure only | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Structure only | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Structure-Grounded Consistency | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Structure-Grounded Consistency | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Structure-Grounded Consistency | objective_accuracy | 0.6800 | 0.6800 | 0.6800 | +0.0000 | +0.0000 |
| Structure-Grounded Consistency | structure_completeness | 0.7652 | 0.7652 | 0.7652 | +0.0000 | +0.0000 |
| Structure-Grounded Consistency | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Structure-Grounded Consistency | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
| Structure-Only | executable_rate | 0.9400 | 0.9400 | 0.9400 | +0.0000 | +0.0000 |
| Structure-Only | optimal_rate | 0.8800 | 0.8800 | 0.8800 | +0.0000 | +0.0000 |
| Structure-Only | objective_accuracy | 0.6600 | 0.6600 | 0.6600 | +0.0000 | +0.0000 |
| Structure-Only | structure_completeness | 0.7656 | 0.7656 | 0.7656 | +0.0000 | +0.0000 |
| Structure-Only | inventory_balance_accuracy | 0.9744 | 0.9744 | 0.9744 | +0.0000 | +0.0000 |
| Structure-Only | constraint_coverage | 0.9579 | 0.9579 | 0.8978 | -0.0601 | -0.0601 |
