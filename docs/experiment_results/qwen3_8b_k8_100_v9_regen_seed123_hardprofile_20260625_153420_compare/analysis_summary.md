# Analysis Summary: Regenerated Candidate Robustness Test

## Setup

This experiment evaluates the hard-profile `ReplenishVerifier-TypeAware-Consensus` selector on a newly regenerated k=8 candidate pool.

- Benchmark: `data/generated/test_100_v6.jsonl`
- Candidate file: `data/candidates/qwen3_8b_k8_100_v9_regen_seed123.jsonl`
- Number of problems: 100
- Candidates per problem: 8

## Purpose

The purpose is to test whether the previous hard-profile TAC result remains robust when the candidate pool is regenerated. This helps distinguish a stable no-reference selection improvement from a result that only works on one fixed candidate file.

## Evaluation Principle

The selector is evaluated under the same no-reference formal selection policy. Reference objectives, objective correctness labels, oracle labels, reference LPs, and reference answers are not used by formal selection. They may appear only in post-hoc diagnostics and oracle upper-bound metrics.
