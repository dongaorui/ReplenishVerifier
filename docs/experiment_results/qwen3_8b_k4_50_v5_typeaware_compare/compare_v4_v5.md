# Qwen3-8B v4 MetricsFix vs v5 TypeAware Comparison

This report compares the previous metrics-fix evaluation with the new type-aware generation and selection experiment.

| method | metric | v4_metricsfix | v5_typeaware | delta_v5_vs_v4 |
| --- | --- | ---: | ---: | ---: |
| Best-of-K | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Best-of-K | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Best-of-K | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| Best-of-K | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| Best-of-K | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Best-of-K | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Consensus only | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Consensus only | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Consensus only | objective_accuracy | 0.6800 | 0.7000 | +0.0200 |
| Consensus only | structure_completeness | 0.7652 | 0.7770 | +0.0118 |
| Consensus only | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Consensus only | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Direct | executable_rate | 0.9400 | 0.9000 | -0.0400 |
| Direct | optimal_rate | 0.8800 | 0.8000 | -0.0800 |
| Direct | objective_accuracy | 0.6600 | 0.6800 | +0.0200 |
| Direct | structure_completeness | 0.7643 | 0.7446 | -0.0197 |
| Direct | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Direct | constraint_coverage | 0.8978 | 0.8775 | -0.0203 |
| OR-R1-like Voting | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| OR-R1-like Voting | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| OR-R1-like Voting | objective_accuracy | 0.6800 | 0.7000 | +0.0200 |
| OR-R1-like Voting | structure_completeness | 0.7652 | 0.7770 | +0.0118 |
| OR-R1-like Voting | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| OR-R1-like Voting | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| OptArgus-like Audit | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| OptArgus-like Audit | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| OptArgus-like Audit | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| OptArgus-like Audit | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| OptArgus-like Audit | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| OptArgus-like Audit | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| OptiRepair-like Repair-Prompt | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| OptiRepair-like Repair-Prompt | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| OptiRepair-like Repair-Prompt | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| OptiRepair-like Repair-Prompt | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| OptiRepair-like Repair-Prompt | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| OptiRepair-like Repair-Prompt | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| ReplenishVerifier-Full | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| ReplenishVerifier-Full | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| ReplenishVerifier-Full | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| ReplenishVerifier-Full | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| ReplenishVerifier-Full | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| ReplenishVerifier-Full | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| ReplenishVerifier-Repair | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| ReplenishVerifier-Repair | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| ReplenishVerifier-Repair | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| ReplenishVerifier-Repair | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| ReplenishVerifier-Repair | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| ReplenishVerifier-Repair | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| ReplenishVerifier-TypeAware | executable_rate | N/A | 0.9400 | N/A |
| ReplenishVerifier-TypeAware | optimal_rate | N/A | 0.8200 | N/A |
| ReplenishVerifier-TypeAware | objective_accuracy | N/A | 0.7200 | N/A |
| ReplenishVerifier-TypeAware | structure_completeness | N/A | 0.7770 | N/A |
| ReplenishVerifier-TypeAware | inventory_balance_accuracy | N/A | 1.0000 | N/A |
| ReplenishVerifier-TypeAware | constraint_coverage | N/A | 0.9128 | N/A |
| SIRL-like LP-Stats | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| SIRL-like LP-Stats | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| SIRL-like LP-Stats | objective_accuracy | 0.6400 | 0.7000 | +0.0600 |
| SIRL-like LP-Stats | structure_completeness | 0.7656 | 0.7770 | +0.0114 |
| SIRL-like LP-Stats | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| SIRL-like LP-Stats | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Solver + Consensus | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Solver + Consensus | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Solver + Consensus | objective_accuracy | 0.6800 | 0.7000 | +0.0200 |
| Solver + Consensus | structure_completeness | 0.7652 | 0.7770 | +0.0118 |
| Solver + Consensus | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Solver + Consensus | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Solver + Structure | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Solver + Structure | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Solver + Structure | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| Solver + Structure | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| Solver + Structure | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Solver + Structure | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Solver + Structure + Consensus | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Solver + Structure + Consensus | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Solver + Structure + Consensus | objective_accuracy | 0.6800 | 0.7000 | +0.0200 |
| Solver + Structure + Consensus | structure_completeness | 0.7652 | 0.7770 | +0.0118 |
| Solver + Structure + Consensus | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Solver + Structure + Consensus | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Solver only | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Solver only | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Solver only | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| Solver only | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| Solver only | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Solver only | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Solver-Filter | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Solver-Filter | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Solver-Filter | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| Solver-Filter | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| Solver-Filter | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Solver-Filter | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Structure + Consensus | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Structure + Consensus | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Structure + Consensus | objective_accuracy | 0.6800 | 0.7000 | +0.0200 |
| Structure + Consensus | structure_completeness | 0.7652 | 0.7770 | +0.0118 |
| Structure + Consensus | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Structure + Consensus | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Structure only | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Structure only | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Structure only | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| Structure only | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| Structure only | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Structure only | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Structure-Grounded Consistency | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Structure-Grounded Consistency | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Structure-Grounded Consistency | objective_accuracy | 0.6800 | 0.7000 | +0.0200 |
| Structure-Grounded Consistency | structure_completeness | 0.7652 | 0.7770 | +0.0118 |
| Structure-Grounded Consistency | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Structure-Grounded Consistency | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
| Structure-Only | executable_rate | 0.9400 | 0.9400 | +0.0000 |
| Structure-Only | optimal_rate | 0.8800 | 0.8200 | -0.0600 |
| Structure-Only | objective_accuracy | 0.6600 | 0.7000 | +0.0400 |
| Structure-Only | structure_completeness | 0.7656 | 0.7774 | +0.0118 |
| Structure-Only | inventory_balance_accuracy | 0.9744 | 1.0000 | +0.0256 |
| Structure-Only | constraint_coverage | 0.8978 | 0.9128 | +0.0150 |
