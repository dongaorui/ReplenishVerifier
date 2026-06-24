# Analysis Summary: Safe TypeAware-Consensus

## Experiment Setup

- Benchmark: `data/generated/test_100_v6.jsonl`
- Candidates: `data/candidates/qwen3_8b_k8_100_v8_candidate_diversity.jsonl`
- Problems: 100
- Candidates per problem: 8

## Goal

This experiment improves the existing `ReplenishVerifier-TypeAware-Consensus` selector by replacing raw objective consensus with verifier-guided safe consensus. The goal is not to weaken Consensus-only or Structure-only baselines, but to make the final selector more robust against wrong consensus, missing objective terms, and problem-type-specific structural omissions.

## Interpretation

Consensus-only is a strong ablation because objective agreement across candidates is informative. However, raw consensus can be unsafe when multiple candidates share the same modeling error. The enhanced TypeAware-Consensus selector therefore uses consensus only after checking solver safety, structure validity, constraint coverage, objective-term coverage, problem-type schema coverage, and text-triggered hard gates.

## No-Reference Policy

Formal selection does not use `reference_objective`, `objective_correct`, oracle labels, reference LPs, or reference answers. These fields may appear only in post-hoc diagnostics.
