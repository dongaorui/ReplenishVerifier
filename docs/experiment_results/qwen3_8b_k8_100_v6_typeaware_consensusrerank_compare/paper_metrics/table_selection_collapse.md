# Table: Selection Collapse Diagnostics

| diagnostic_type | method_a | method_b | methods | n_common | same_selection_rate | count | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_same_selection_pair | Best-of-K | Direct | Best-of-K; Direct | 100 | 1.0000 | 100 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Best-of-K | ReplenishVerifier-Full | Best-of-K; ReplenishVerifier-Full | 100 | 0.9900 | 99 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Best-of-K | Structure only | Best-of-K; Structure only | 100 | 1.0000 | 100 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Consensus only | ReplenishVerifier-TypeAware | Consensus only; ReplenishVerifier-TypeAware | 100 | 0.9900 | 99 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Consensus only | ReplenishVerifier-TypeAware-Consensus | Consensus only; ReplenishVerifier-TypeAware-Consensus | 100 | 0.9900 | 99 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Consensus only | Solver only | Consensus only; Solver only | 100 | 0.9800 | 98 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Direct | ReplenishVerifier-Full | Direct; ReplenishVerifier-Full | 100 | 0.9900 | 99 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | Direct | Structure only | Direct; Structure only | 100 | 1.0000 | 100 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-Full | Structure only | ReplenishVerifier-Full; Structure only | 100 | 0.9900 | 99 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-TypeAware | ReplenishVerifier-TypeAware-Consensus | ReplenishVerifier-TypeAware; ReplenishVerifier-TypeAware-Consensus | 100 | 1.0000 | 100 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-TypeAware | Solver only | ReplenishVerifier-TypeAware; Solver only | 100 | 0.9700 | 97 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-TypeAware-Consensus | Solver only | ReplenishVerifier-TypeAware-Consensus; Solver only | 100 | 0.9700 | 97 | Methods select the same candidate on nearly all shared problems. |
| metric_duplicate_group |  |  | Best-of-K; Consensus only; Direct; ReplenishVerifier-Full; ReplenishVerifier-TypeAware; ReplenishVerifier-TypeAware-Consensus; Solver only; Structure only |  |  | 8 | Methods have identical headline metric values. |
| candidate_rank_distribution | Best-of-K |  | Best-of-K | 100 |  | 100 | k0=100 |
| candidate_rank_distribution | Consensus only |  | Consensus only | 100 |  | 100 | k0=13, k1=14, k2=18, k3=11, k4=8, k5=11, k6=13, k7=12 |
| candidate_rank_distribution | Direct |  | Direct | 100 |  | 100 | k0=100 |
| candidate_rank_distribution | ReplenishVerifier-Full |  | ReplenishVerifier-Full | 100 |  | 100 | k0=99, k1=1 |
| candidate_rank_distribution | ReplenishVerifier-TypeAware |  | ReplenishVerifier-TypeAware | 100 |  | 100 | k0=13, k1=13, k2=18, k3=11, k4=8, k5=12, k6=13, k7=12 |
| candidate_rank_distribution | ReplenishVerifier-TypeAware-Consensus |  | ReplenishVerifier-TypeAware-Consensus | 100 |  | 100 | k0=13, k1=13, k2=18, k3=11, k4=8, k5=12, k6=13, k7=12 |
| candidate_rank_distribution | Solver only |  | Solver only | 100 |  | 100 | k0=13, k1=13, k2=19, k3=12, k4=8, k5=11, k6=12, k7=12 |
| candidate_rank_distribution | Structure only |  | Structure only | 100 |  | 100 | k0=100 |
