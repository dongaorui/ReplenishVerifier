# Metric Saturation Report

This report is diagnostic only and does not affect formal selection.

## Metric unique-value counts

| metric | unique_values | saturated | values |
| --- | --- | --- | --- |
| average_repair_feedback_count | 7 | False | [0.06, 0.08, 0.21, 0.22, 0.26, 0.3, 0.32] |
| average_runtime_sec | 8 | False | [0.0991262622573413, 0.09933002069825307, 0.10052835343638435, 0.10196166803594679, 0.10429036881192587, 0.10677578186267056, 0.1068824558344204, 0.10730941630899907] |
| code_validity_rate | 1 | True | [1.0] |
| constraint_coverage | 6 | False | [0.8841666666666665, 0.9136111111111112, 0.9323333333333335, 0.9344444444444444, 0.9394444444444444, 0.9444444444444444] |
| executable_rate | 3 | False | [0.91, 0.93, 0.97] |
| inventory_balance_accuracy | 1 | True | [1.0] |
| mean_objective_gap | 8 | False | [0.02716798195453856, 0.11189754690487945, 0.11543912375010025, 0.12207044617125418, 0.1230962450121015, 0.12745990711705193, 0.13069974205493387, 0.1432223652661633] |
| mean_relative_error | 8 | False | [0.02716798195453856, 0.11189754690487945, 0.11543912375010025, 0.12207044617125418, 0.1230962450121015, 0.12745990711705193, 0.13069974205493387, 0.1432223652661633] |
| median_objective_gap | 1 | True | [0.0] |
| median_relative_error | 1 | True | [0.0] |
| median_runtime_sec | 7 | False | [0.09992320649325848, 0.10006520949536934, 0.10174474550876766, 0.102280612452887, 0.1077951259794645, 0.10885346995200962, 0.10986655455781147] |
| objective_accuracy | 4 | False | [0.7, 0.81, 0.82, 0.83] |
| objective_accuracy_count | 4 | False | [70, 81, 82, 83] |
| objective_accuracy_total | 1 | True | [100] |
| objective_term_coverage | 6 | False | [0.9033333333333335, 0.9133333333333334, 0.9166666666666667, 0.9233333333333333, 0.926666666666667, 0.9366666666666665] |
| objective_term_lp_coefficient_coverage | 4 | False | [0.9072164948453612, 0.9194139194139199, 0.9209621993127148, 0.9318996415770608] |
| objective_term_surface_coverage | 3 | False | [0.98, 0.9866666666666666, 1.0] |
| optimal_rate | 2 | True | [0.78, 0.87] |
| solver_status_error_rate | 3 | False | [0.03, 0.07, 0.09] |
| solver_status_infeasible_rate | 3 | False | [0.06, 0.08, 0.12] |
| solver_status_optimal_rate | 2 | True | [0.78, 0.87] |
| solver_status_timeout_rate | 1 | True | [0.0] |
| structure_complete_count | 1 | True | [0] |
| structure_complete_total | 1 | True | [100] |
| structure_completeness | 7 | False | [0.7489063492063489, 0.7805994047619054, 0.7907476190476187, 0.7927952380952378, 0.803203571428572, 0.8067105158730163, 0.807578571428572] |

## Saturated metrics

code_validity_rate, inventory_balance_accuracy, median_objective_gap, median_relative_error, objective_accuracy_total, optimal_rate, solver_status_optimal_rate, solver_status_timeout_rate, structure_complete_count, structure_complete_total

## High-overlap method pairs

High same_selection_rate can make headline metrics identical even when method names differ.

- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-HybridSafe: same_selection_rate=1.0000
- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-TypeAware: same_selection_rate=0.9500
- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=1.0000
- ReplenishVerifier-Full / ReplenishVerifier-FullV2: same_selection_rate=1.0000
- ReplenishVerifier-HybridSafe / ReplenishVerifier-TypeAware: same_selection_rate=0.9500
- ReplenishVerifier-HybridSafe / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=1.0000
- ReplenishVerifier-TypeAware / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=0.9500
