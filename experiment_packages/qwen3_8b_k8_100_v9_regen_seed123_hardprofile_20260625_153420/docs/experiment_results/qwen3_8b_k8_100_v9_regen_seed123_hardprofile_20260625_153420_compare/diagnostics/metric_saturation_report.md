# Metric Saturation Report

This report is diagnostic only and does not affect formal selection.

## Metric unique-value counts

| metric | unique_values | saturated | values |
| --- | --- | --- | --- |
| average_repair_feedback_count | 5 | False | [0.06, 0.07, 0.19, 0.24, 0.28] |
| average_runtime_sec | 9 | False | [0.1010373286518734, 0.10120772168389522, 0.1024982967460528, 0.10348472798708826, 0.10415938197402283, 0.10433343678945675, 0.1081963108596392, 0.10967191092669965, 0.11088437444530427] |
| code_validity_rate | 1 | True | [1.0] |
| constraint_coverage | 5 | False | [0.8708333333333332, 0.9258333333333333, 0.9366666666666665, 0.9416666666666665, 0.9479166666666665] |
| executable_rate | 3 | False | [0.9, 0.94, 0.97] |
| inventory_balance_accuracy | 1 | True | [1.0] |
| mean_objective_gap | 9 | False | [0.0605824814546796, 0.14746602743650278, 0.14848435198957988, 0.15278913472762068, 0.152981575186416, 0.16103655740803302, 0.16433031567266587, 0.16472504985684194, 0.17549670644352247] |
| mean_relative_error | 9 | False | [0.0605824814546796, 0.14746602743650278, 0.14848435198957988, 0.15278913472762068, 0.152981575186416, 0.16103655740803302, 0.16433031567266587, 0.16472504985684194, 0.17549670644352247] |
| median_objective_gap | 1 | True | [0.0] |
| median_relative_error | 1 | True | [0.0] |
| median_runtime_sec | 8 | False | [0.10024032049113885, 0.10036261496134102, 0.10230693401535973, 0.10239995399024338, 0.10264108254341409, 0.10825728304916993, 0.10835062304977328, 0.10836391249904409] |
| objective_accuracy | 5 | False | [0.67, 0.78, 0.8, 0.81, 0.82] |
| objective_accuracy_count | 5 | False | [67, 78, 80, 81, 82] |
| objective_accuracy_total | 1 | True | [100] |
| objective_term_coverage | 7 | False | [0.9066666666666668, 0.9116666666666667, 0.9133333333333337, 0.915, 0.92, 0.9266666666666665, 0.94] |
| objective_term_lp_coefficient_coverage | 5 | False | [0.9037037037037041, 0.9106529209621995, 0.9209621993127148, 0.9243986254295533, 0.9361702127659575] |
| objective_term_surface_coverage | 4 | False | [0.975, 0.9866666666666666, 0.9883333333333334, 1.0] |
| optimal_rate | 2 | True | [0.77, 0.87] |
| solver_status_error_rate | 3 | False | [0.03, 0.06, 0.1] |
| solver_status_infeasible_rate | 3 | False | [0.07, 0.08, 0.12] |
| solver_status_optimal_rate | 2 | True | [0.77, 0.87] |
| solver_status_timeout_rate | 1 | True | [0.0] |
| structure_complete_count | 1 | True | [0] |
| structure_complete_total | 1 | True | [100] |
| structure_completeness | 8 | False | [0.7374920634920632, 0.7898369047619052, 0.7914214285714278, 0.791914285714285, 0.8041702380952386, 0.8081355158730164, 0.8086910714285719, 0.8088577380952385] |

## Saturated metrics

code_validity_rate, inventory_balance_accuracy, median_objective_gap, median_relative_error, objective_accuracy_total, optimal_rate, solver_status_optimal_rate, solver_status_timeout_rate, structure_complete_count, structure_complete_total

## High-overlap method pairs

High same_selection_rate can make headline metrics identical even when method names differ.

- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-HybridSafe: same_selection_rate=1.0000
- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-TypeAware: same_selection_rate=0.9700
- ReplenishVerifier-Full / ReplenishVerifier-FullV2: same_selection_rate=1.0000
- ReplenishVerifier-HybridSafe / ReplenishVerifier-TypeAware: same_selection_rate=0.9700
