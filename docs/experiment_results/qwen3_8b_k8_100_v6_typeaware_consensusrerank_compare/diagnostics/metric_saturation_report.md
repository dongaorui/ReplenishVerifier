# Metric Saturation Report

This report is diagnostic only and does not affect formal selection.

## Metric unique-value counts

| metric | unique_values | saturated | values |
| --- | --- | --- | --- |
| average_repair_feedback_count | 1 | True | [0.0] |
| average_runtime_sec | 5 | False | [0.06925850716710556, 0.06925992443691939, 0.06933375373715535, 0.07334480768884533, 0.07336253229877912] |
| code_validity_rate | 1 | True | [1.0] |
| constraint_coverage | 1 | True | [0.0] |
| executable_rate | 1 | True | [0.0] |
| inventory_balance_accuracy | 1 | True | [0.0] |
| mean_objective_gap | 1 | True | [None] |
| mean_relative_error | 1 | True | [None] |
| median_objective_gap | 1 | True | [None] |
| median_relative_error | 1 | True | [None] |
| median_runtime_sec | 3 | False | [0.06892014099867083, 0.06893488400964998, 0.07279845300945453] |
| objective_accuracy | 1 | True | [0.0] |
| objective_accuracy_count | 1 | True | [0] |
| objective_accuracy_total | 1 | True | [100] |
| objective_term_coverage | 1 | True | [0.98] |
| objective_term_lp_coefficient_coverage | 1 | True | [None] |
| objective_term_surface_coverage | 1 | True | [0.98] |
| optimal_rate | 1 | True | [0.0] |
| solver_status_error_rate | 1 | True | [1.0] |
| solver_status_infeasible_rate | 1 | True | [0.0] |
| solver_status_optimal_rate | 1 | True | [0.0] |
| solver_status_timeout_rate | 1 | True | [0.0] |
| structure_complete_count | 1 | True | [0] |
| structure_complete_total | 1 | True | [100] |
| structure_completeness | 1 | True | [0.0] |

## Saturated metrics

average_repair_feedback_count, code_validity_rate, constraint_coverage, executable_rate, inventory_balance_accuracy, mean_objective_gap, mean_relative_error, median_objective_gap, median_relative_error, objective_accuracy, objective_accuracy_count, objective_accuracy_total, objective_term_coverage, objective_term_lp_coefficient_coverage, objective_term_surface_coverage, optimal_rate, solver_status_error_rate, solver_status_infeasible_rate, solver_status_optimal_rate, solver_status_timeout_rate, structure_complete_count, structure_complete_total, structure_completeness

## High-overlap method pairs

High same_selection_rate can make headline metrics identical even when method names differ.

- Best-of-K / Direct: same_selection_rate=1.0000
- Best-of-K / ReplenishVerifier-Full: same_selection_rate=0.9900
- Best-of-K / Structure only: same_selection_rate=1.0000
- Consensus only / ReplenishVerifier-TypeAware: same_selection_rate=0.9900
- Consensus only / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=0.9900
- Consensus only / Solver only: same_selection_rate=0.9800
- Direct / ReplenishVerifier-Full: same_selection_rate=0.9900
- Direct / Structure only: same_selection_rate=1.0000
- ReplenishVerifier-Full / Structure only: same_selection_rate=0.9900
- ReplenishVerifier-TypeAware / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=1.0000
- ReplenishVerifier-TypeAware / Solver only: same_selection_rate=0.9700
- ReplenishVerifier-TypeAware-Consensus / Solver only: same_selection_rate=0.9700
