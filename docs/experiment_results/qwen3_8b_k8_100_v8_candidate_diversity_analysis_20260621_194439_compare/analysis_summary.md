# Analysis Summary: Qwen3-8B k=8 Candidate Diversity Prompting

## Experiment Setup

- Benchmark: `data/generated/test_100_v6.jsonl`
- Candidates: `data/candidates/qwen3_8b_k8_100_v8_candidate_diversity.jsonl`
- Number of problems: 100
- Candidates per problem: 8
- Total candidates: 800

This experiment evaluates candidate-specific diversity prompting for Qwen3-8B on the 100-problem replenishment optimization benchmark.

## Main Finding

Candidate diversity prompting substantially improves the candidate pool. Compared with the previous k=8 pool, oracle@8 improves from 0.7800 to 0.8600, and the best formal no-reference selector improves from 0.7400 to 0.8300.

## Main Results

| Method | Objective Accuracy | Executable Rate | Structure Completeness | Constraint Coverage |
| --- | ---: | ---: | ---: | ---: |
| Direct | 0.7000 | 0.9100 | 0.7489 | 0.8842 |
| Solver only | 0.7800 | 0.9700 | 0.7898 | 0.9319 |
| Best-of-K | 0.7900 | 0.9700 | 0.8032 | 0.9394 |
| Consensus only | 0.8200 | 0.9700 | 0.7904 | 0.9319 |
| Structure only | 0.8200 | 0.9700 | 0.8076 | 0.9444 |
| ReplenishVerifier-Full | 0.8200 | 0.9700 | 0.8076 | 0.9444 |
| ReplenishVerifier-FullV2 | 0.8200 | 0.9700 | 0.8076 | 0.9444 |
| ReplenishVerifier-ConsensusSafe | 0.8300 | 0.9700 | 0.8067 | 0.9444 |
| ReplenishVerifier-HybridSafe | 0.8300 | 0.9700 | 0.8067 | 0.9444 |
| ReplenishVerifier-TypeAware | 0.8300 | 0.9300 | 0.7806 | 0.9136 |
| ReplenishVerifier-TypeAware-Consensus | 0.8300 | 0.9700 | 0.8067 | 0.9444 |

## Comparison with Previous Candidate Pool

| Metric | Previous k=8 pool | New diversity pool | Change |
| --- | ---: | ---: | ---: |
| Direct objective accuracy | 0.6900 | 0.7000 | +0.0100 |
| Best-of-K objective accuracy | 0.7400 | 0.7900 | +0.0500 |
| ReplenishVerifier-Full | 0.7400 | 0.8200 | +0.0800 |
| ReplenishVerifier-FullV2 | 0.7400 | 0.8200 | +0.0800 |
| Best formal selector | 0.7400 | 0.8300 | +0.0900 |
| Oracle@8 | 0.7800 | 0.8600 | +0.0800 |

## Interpretation

The improvement is mainly caused by a stronger candidate pool rather than a selector-only change. Direct improves only slightly, from 0.6900 to 0.7000, while oracle@8 improves from 0.7800 to 0.8600. This indicates that candidate diversity prompting increases the chance that at least one objective-correct formulation appears among the eight generated candidates.

Formal no-reference selectors can exploit this improved pool. The best formal selectors reach 0.8300 objective accuracy, leaving a remaining 0.0300 gap to oracle@8. This gap suggests that some correct candidates still cannot be safely distinguished by current non-reference signals.

## FullV2 Interpretation

FullV2 remains a conservative guarded extension of Full. In this experiment, FullV2 has the same objective accuracy as Full, 0.8200. This is not a regression: it means no challenger candidate satisfied the strict no-reference override conditions.

Post-hoc diagnostics show that Full still has 18 objective errors. Among them, 4 have an objective-correct candidate in the pool, but they are distinguishable only with oracle/reference information. The remaining 14 are pool-limited.

## Error Analysis

For ReplenishVerifier-Full, the main remaining errors are:

- execution_error: 3
- missing_capacity_constraint: 4
- missing_shortage_variable: 2
- objective_mismatch_after_selection: 4
- solver_not_optimal: 10

Candidate diversity prompting reduces key modeling errors, especially missing capacity constraints and objective mismatches, but solver-status failures remain a challenge.

## No-Reference Policy

Formal selection does not use `reference_objective`, `objective_correct`, oracle labels, reference LPs, or reference answers. Oracle metrics are post-hoc diagnostics only.
