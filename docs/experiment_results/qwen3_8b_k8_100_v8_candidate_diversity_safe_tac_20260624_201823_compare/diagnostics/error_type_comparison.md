# Error Type Comparison

| method | error_type | reported | recomputed | delta | status |
| --- | --- | --- | --- | --- | --- |
| Best-of-K | execution_error | 3 | 3 | 0 | OK |
| Best-of-K | missing_capacity_constraint | 4 | 4 | 0 | OK |
| Best-of-K | missing_shortage_variable | 2 | 2 | 0 | OK |
| Best-of-K | no_error_detected | 76 | 78 | 2 | MISMATCH |
| Best-of-K | objective_mismatch_after_selection | 5 | 3 | -2 | MISMATCH |
| Best-of-K | solver_not_optimal | 10 | 10 | 0 | OK |
| Consensus only | execution_error | 3 | 3 | 0 | OK |
| Consensus only | missing_capacity_constraint | 10 | 10 | 0 | OK |
| Consensus only | missing_shortage_variable | 2 | 2 | 0 | OK |
| Consensus only | no_error_detected | 71 | 71 | 0 | OK |
| Consensus only | objective_mismatch_after_selection | 4 | 4 | 0 | OK |
| Consensus only | solver_not_optimal | 10 | 10 | 0 | OK |
| Direct | execution_error | 9 | 9 | 0 | OK |
| Direct | missing_capacity_constraint | 9 | 9 | 0 | OK |
| Direct | no_error_detected | 61 | 61 | 0 | OK |
| Direct | objective_mismatch_after_selection | 8 | 8 | 0 | OK |
| Direct | solver_not_optimal | 13 | 13 | 0 | OK |
| ReplenishVerifier-ConsensusSafe | execution_error | 3 | 3 | 0 | OK |
| ReplenishVerifier-ConsensusSafe | missing_capacity_constraint | 4 | 4 | 0 | OK |
| ReplenishVerifier-ConsensusSafe | missing_shortage_variable | 2 | 2 | 0 | OK |
| ReplenishVerifier-ConsensusSafe | no_error_detected | 78 | 78 | 0 | OK |
| ReplenishVerifier-ConsensusSafe | objective_mismatch_after_selection | 3 | 3 | 0 | OK |
| ReplenishVerifier-ConsensusSafe | solver_not_optimal | 10 | 10 | 0 | OK |
| ReplenishVerifier-Full | execution_error | 3 | 3 | 0 | OK |
| ReplenishVerifier-Full | missing_capacity_constraint | 4 | 4 | 0 | OK |
| ReplenishVerifier-Full | missing_shortage_variable | 2 | 2 | 0 | OK |
| ReplenishVerifier-Full | no_error_detected | 77 | 78 | 1 | MISMATCH |
| ReplenishVerifier-Full | objective_mismatch_after_selection | 4 | 3 | -1 | MISMATCH |
| ReplenishVerifier-Full | solver_not_optimal | 10 | 10 | 0 | OK |
| ReplenishVerifier-FullV2 | execution_error | 3 | 3 | 0 | OK |
| ReplenishVerifier-FullV2 | missing_capacity_constraint | 4 | 4 | 0 | OK |
| ReplenishVerifier-FullV2 | missing_shortage_variable | 2 | 2 | 0 | OK |
| ReplenishVerifier-FullV2 | no_error_detected | 77 | 78 | 1 | MISMATCH |
| ReplenishVerifier-FullV2 | objective_mismatch_after_selection | 4 | 3 | -1 | MISMATCH |
| ReplenishVerifier-FullV2 | solver_not_optimal | 10 | 10 | 0 | OK |
| ReplenishVerifier-HybridSafe | execution_error | 3 | 3 | 0 | OK |
| ReplenishVerifier-HybridSafe | missing_capacity_constraint | 4 | 4 | 0 | OK |
| ReplenishVerifier-HybridSafe | missing_shortage_variable | 2 | 2 | 0 | OK |
| ReplenishVerifier-HybridSafe | no_error_detected | 78 | 78 | 0 | OK |
| ReplenishVerifier-HybridSafe | objective_mismatch_after_selection | 3 | 3 | 0 | OK |
| ReplenishVerifier-HybridSafe | solver_not_optimal | 10 | 10 | 0 | OK |
| ReplenishVerifier-TypeAware | execution_error | 7 | 7 | 0 | OK |
| ReplenishVerifier-TypeAware | missing_capacity_constraint | 4 | 4 | 0 | OK |
| ReplenishVerifier-TypeAware | missing_shortage_variable | 2 | 2 | 0 | OK |
| ReplenishVerifier-TypeAware | no_error_detected | 78 | 78 | 0 | OK |
| ReplenishVerifier-TypeAware | objective_mismatch_after_selection | 3 | 3 | 0 | OK |
| ReplenishVerifier-TypeAware | solver_not_optimal | 6 | 6 | 0 | OK |
| ReplenishVerifier-TypeAware-Consensus | execution_error | 3 | 3 | 0 | OK |
| ReplenishVerifier-TypeAware-Consensus | missing_capacity_constraint | 4 | 4 | 0 | OK |
| ReplenishVerifier-TypeAware-Consensus | missing_shortage_variable | 2 | 2 | 0 | OK |
| ReplenishVerifier-TypeAware-Consensus | no_error_detected | 78 | 78 | 0 | OK |
| ReplenishVerifier-TypeAware-Consensus | objective_mismatch_after_selection | 3 | 3 | 0 | OK |
| ReplenishVerifier-TypeAware-Consensus | solver_not_optimal | 10 | 10 | 0 | OK |
| Solver only | execution_error | 3 | 3 | 0 | OK |
| Solver only | missing_big_m_constraint | N/A | 1 | N/A | MISSING |
| Solver only | missing_capacity_constraint | 10 | 10 | 0 | OK |
| Solver only | missing_shortage_variable | 2 | 2 | 0 | OK |
| Solver only | no_error_detected | 71 | 70 | -1 | MISMATCH |
| Solver only | objective_mismatch_after_selection | 4 | 3 | -1 | MISMATCH |
| Solver only | other_missing_structure | N/A | 1 | N/A | MISSING |
| Solver only | solver_not_optimal | 10 | 10 | 0 | OK |
| Structure only | execution_error | 3 | 3 | 0 | OK |
| Structure only | missing_capacity_constraint | 4 | 4 | 0 | OK |
| Structure only | missing_shortage_variable | 2 | 2 | 0 | OK |
| Structure only | no_error_detected | 77 | 77 | 0 | OK |
| Structure only | objective_mismatch_after_selection | 4 | 4 | 0 | OK |
| Structure only | solver_not_optimal | 10 | 10 | 0 | OK |
