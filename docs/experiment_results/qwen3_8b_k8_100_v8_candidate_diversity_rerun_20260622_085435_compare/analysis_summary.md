# Analysis Summary: Qwen3-8B k=8 Candidate Diversity

## Experiment Setup

- Benchmark: `data/generated/test_100_v6.jsonl`
- Candidates: `data/candidates/qwen3_8b_k8_100_v8_candidate_diversity.jsonl`
- Number of problems: 100
- Candidates per problem: 8
- Total candidates: 800

## Main Finding

This experiment evaluates the Qwen3-8B k=8 candidate-diversity candidate pool. The main conclusion is that improving candidate diversity substantially strengthens the candidate pool and allows no-reference selectors to achieve higher objective accuracy.

## Results

See `main_results.md` for the full method table.

The key metrics to report are:

- Direct objective accuracy
- Best-of-K objective accuracy
- ReplenishVerifier-Full objective accuracy
- ReplenishVerifier-FullV2 objective accuracy
- Best formal no-reference selector accuracy
- Oracle@8 post-hoc upper bound

## Interpretation

Candidate diversity prompting mainly improves the candidate pool rather than only changing the selector. A stronger candidate pool increases the probability that at least one correct optimization model appears among the eight generated candidates. ReplenishVerifier can then use non-reference structural, solver, constraint, and consensus signals to select stronger candidates.

## Error Analysis

See `error_type_summary.md` for selected error modes. The main remaining failures should be interpreted as either candidate-pool limitations, solver-status failures, or cases where current non-reference signals cannot safely distinguish the correct candidate.

## No-Reference Policy

Formal selection does not use `reference_objective`, `objective_correct`, oracle labels, reference LPs, or reference answers. Oracle metrics are post-hoc diagnostics only.
