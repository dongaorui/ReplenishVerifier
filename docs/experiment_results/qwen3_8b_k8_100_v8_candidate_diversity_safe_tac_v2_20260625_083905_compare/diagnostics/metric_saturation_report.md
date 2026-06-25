# Metric Saturation Report

This report is diagnostic only and does not affect formal selection.

## Metric unique-value counts

| metric | unique_values | saturated | values |
| --- | --- | --- | --- |
| average_repair_feedback_count | 6 | False | [0.06, 0.08, 0.21, 0.22, 0.26, 0.33] |
| average_runtime_sec | 9 | False | [0.09893114556674845, 0.0991625971463509, 0.1003307722765021, 0.10169590505538509, 0.10176666521583684, 0.10192311649559997, 0.10533254864742048, 0.10718881436856463, 0.10731852537952363] |
| code_validity_rate | 1 | True | [1.0] |
| constraint_coverage | 5 | False | [0.8841666666666665, 0.9136111111111112, 0.9306944444444444, 0.9394444444444444, 0.9444444444444444] |
| executable_rate | 3 | False | [0.91, 0.93, 0.97] |
| inventory_balance_accuracy | 1 | True | [1.0] |
| mean_objective_gap | 9 | False | [0.02521487350406109, 0.11510148362945018, 0.11543912375010025, 0.11853790974628865, 0.11920555437867182, 0.12887548740789667, 0.13069974205493387, 0.1432223652661633, 0.14499946661667118] |
| mean_relative_error | 9 | False | [0.02521487350406109, 0.11510148362945018, 0.11543912375010025, 0.11853790974628865, 0.11920555437867182, 0.12887548740789667, 0.13069974205493387, 0.1432223652661633, 0.14499946661667118] |
| median_objective_gap | 1 | True | [0.0] |
| median_relative_error | 1 | True | [0.0] |
| median_runtime_sec | 8 | False | [0.09958378446754068, 0.09962119947886094, 0.10209531401051208, 0.1024559314828366, 0.10260358947562054, 0.10545015300158411, 0.10555626201676205, 0.1056914160726592] |
| objective_accuracy | 4 | False | [0.7, 0.82, 0.83, 0.84] |
| objective_accuracy_count | 4 | False | [70, 82, 83, 84] |
| objective_accuracy_total | 1 | True | [100] |
| objective_term_coverage | 7 | False | [0.9033333333333335, 0.9133333333333334, 0.9166666666666667, 0.92, 0.9233333333333333, 0.926666666666667, 0.9366666666666665] |
| objective_term_lp_coefficient_coverage | 5 | False | [0.9072164948453612, 0.9175257731958765, 0.9194139194139199, 0.9209621993127148, 0.9318996415770608] |
| objective_term_surface_coverage | 3 | False | [0.98, 0.9866666666666666, 1.0] |
| optimal_rate | 2 | True | [0.78, 0.87] |
| solver_status_error_rate | 3 | False | [0.03, 0.07, 0.09] |
| solver_status_infeasible_rate | 3 | False | [0.06, 0.08, 0.12] |
| solver_status_optimal_rate | 2 | True | [0.78, 0.87] |
| solver_status_timeout_rate | 1 | True | [0.0] |
| structure_complete_count | 1 | True | [0] |
| structure_complete_total | 1 | True | [100] |
| structure_completeness | 8 | False | [0.7489063492063489, 0.7805994047619054, 0.7900017857142855, 0.7900660714285712, 0.803203571428572, 0.8067105158730163, 0.8072660714285721, 0.807578571428572] |

## Saturated metrics

code_validity_rate, inventory_balance_accuracy, median_objective_gap, median_relative_error, objective_accuracy_total, optimal_rate, solver_status_optimal_rate, solver_status_timeout_rate, structure_complete_count, structure_complete_total

## High-overlap method pairs

High same_selection_rate can make headline metrics identical even when method names differ.

- Consensus only / Solver only: same_selection_rate=0.9500
- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-HybridSafe: same_selection_rate=1.0000
- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-TypeAware: same_selection_rate=0.9500
- ReplenishVerifier-ConsensusSafe / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=0.9800
- ReplenishVerifier-Full / ReplenishVerifier-FullV2: same_selection_rate=1.0000
- ReplenishVerifier-HybridSafe / ReplenishVerifier-TypeAware: same_selection_rate=0.9500
- ReplenishVerifier-HybridSafe / ReplenishVerifier-TypeAware-Consensus: same_selection_rate=0.9800
