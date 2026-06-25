# Table: Selection Collapse Diagnostics

| diagnostic_type | method_a | method_b | methods | n_common | same_selection_rate | count | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_same_selection_pair | ReplenishVerifier-ConsensusSafe | ReplenishVerifier-HybridSafe | ReplenishVerifier-ConsensusSafe; ReplenishVerifier-HybridSafe | 100 | 1.0000 | 100 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-ConsensusSafe | ReplenishVerifier-TypeAware | ReplenishVerifier-ConsensusSafe; ReplenishVerifier-TypeAware | 100 | 0.9700 | 97 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-Full | ReplenishVerifier-FullV2 | ReplenishVerifier-Full; ReplenishVerifier-FullV2 | 100 | 1.0000 | 100 | Methods select the same candidate on nearly all shared problems. |
| high_same_selection_pair | ReplenishVerifier-HybridSafe | ReplenishVerifier-TypeAware | ReplenishVerifier-HybridSafe; ReplenishVerifier-TypeAware | 100 | 0.9700 | 97 | Methods select the same candidate on nearly all shared problems. |
| metric_duplicate_group |  |  | ReplenishVerifier-ConsensusSafe; ReplenishVerifier-HybridSafe |  |  | 2 | Methods have identical headline metric values. |
| metric_duplicate_group |  |  | ReplenishVerifier-Full; ReplenishVerifier-FullV2; Structure only |  |  | 3 | Methods have identical headline metric values. |
| candidate_rank_distribution | Best-of-K |  | Best-of-K | 100 |  | 100 | k0=21, k1=14, k2=1, k3=21, k4=11, k5=13, k6=9, k7=10 |
| candidate_rank_distribution | Consensus only |  | Consensus only | 100 |  | 100 | k0=14, k1=14, k2=12, k3=10, k4=13, k5=17, k6=9, k7=11 |
| candidate_rank_distribution | Direct |  | Direct | 100 |  | 100 | k0=100 |
| candidate_rank_distribution | ReplenishVerifier-ConsensusSafe |  | ReplenishVerifier-ConsensusSafe | 100 |  | 100 | k0=11, k1=15, k2=2, k3=23, k4=14, k5=16, k6=8, k7=11 |
| candidate_rank_distribution | ReplenishVerifier-Full |  | ReplenishVerifier-Full | 100 |  | 100 | k0=47, k1=17, k2=2, k3=24, k4=4, k5=3, k6=2, k7=1 |
| candidate_rank_distribution | ReplenishVerifier-FullV2 |  | ReplenishVerifier-FullV2 | 100 |  | 100 | k0=47, k1=17, k2=2, k3=24, k4=4, k5=3, k6=2, k7=1 |
| candidate_rank_distribution | ReplenishVerifier-HybridSafe |  | ReplenishVerifier-HybridSafe | 100 |  | 100 | k0=11, k1=15, k2=2, k3=23, k4=14, k5=16, k6=8, k7=11 |
| candidate_rank_distribution | ReplenishVerifier-TypeAware |  | ReplenishVerifier-TypeAware | 100 |  | 100 | k0=11, k1=16, k2=2, k3=22, k4=16, k5=14, k6=8, k7=11 |
| candidate_rank_distribution | ReplenishVerifier-TypeAware-Consensus |  | ReplenishVerifier-TypeAware-Consensus | 100 |  | 100 | k0=12, k1=18, k2=2, k3=25, k4=12, k5=15, k6=6, k7=10 |
| candidate_rank_distribution | Solver only |  | Solver only | 100 |  | 100 | k0=14, k1=13, k2=13, k3=10, k4=14, k5=18, k6=7, k7=11 |
| candidate_rank_distribution | Structure only |  | Structure only | 100 |  | 100 | k0=52, k1=19, k2=2, k3=20, k4=2, k5=2, k6=2, k7=1 |
