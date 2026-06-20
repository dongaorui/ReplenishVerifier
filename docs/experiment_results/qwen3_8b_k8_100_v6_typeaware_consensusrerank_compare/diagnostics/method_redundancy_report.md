# Method Redundancy Report

This report is diagnostic only and does not affect formal selection.

## Method pairs with same_selection_rate >= 0.95

| method_a | method_b | n_common | same_count | same_selection_rate |
| --- | --- | --- | --- | --- |
| Best-of-K | Direct | 100 | 100 | 1.0000 |
| Best-of-K | ReplenishVerifier-Full | 100 | 99 | 0.9900 |
| Best-of-K | Structure only | 100 | 100 | 1.0000 |
| Consensus only | ReplenishVerifier-TypeAware | 100 | 99 | 0.9900 |
| Consensus only | ReplenishVerifier-TypeAware-Consensus | 100 | 99 | 0.9900 |
| Consensus only | Solver only | 100 | 98 | 0.9800 |
| Direct | ReplenishVerifier-Full | 100 | 99 | 0.9900 |
| Direct | Structure only | 100 | 100 | 1.0000 |
| ReplenishVerifier-Full | Structure only | 100 | 99 | 0.9900 |
| ReplenishVerifier-TypeAware | ReplenishVerifier-TypeAware-Consensus | 100 | 100 | 1.0000 |
| ReplenishVerifier-TypeAware | Solver only | 100 | 97 | 0.9700 |
| ReplenishVerifier-TypeAware-Consensus | Solver only | 100 | 97 | 0.9700 |

## Metrics-identical method groups

- Best-of-K, Direct, Structure only
- ReplenishVerifier-TypeAware, ReplenishVerifier-TypeAware-Consensus

## Same objective_accuracy but different selection groups

- Best-of-K, Consensus only, Direct, ReplenishVerifier-Full, ReplenishVerifier-TypeAware, ReplenishVerifier-TypeAware-Consensus, Solver only, Structure only

## Recommended display families

- Solver family: Solver only, Solver-Filter
- Structure family: Structure only, Structure-Only
- Consensus family: Consensus only, OR-R1-like Voting, Solver + Consensus
- Full verifier family: ReplenishVerifier-Full, ReplenishVerifier-Repair, Structure-Grounded Consistency
