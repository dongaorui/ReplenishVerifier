# qwen3_8b_k8_100_v9_regen_seed123_hardprofile_20260625_153420

This directory contains the regenerated-candidate robustness experiment for Qwen3-8B k=8.

## Experiment Purpose

This experiment regenerates 800 candidates using a new candidate file and evaluates whether the hard-profile TypeAware-Consensus selector remains effective on a fresh candidate pool.

## Inputs

- Benchmark: `data/generated/test_100_v6.jsonl`
- Candidates: `data/candidates/qwen3_8b_k8_100_v9_regen_seed123.jsonl`
- Problems: 100
- Candidates per problem: 8

## Key Files

- `main_results.md`: full method results
- `analysis_summary.md`: high-level interpretation
- `diagnostics/`: diagnostic reports
- `paper_metrics/`: paper-ready metrics
- `no_leakage_audit.json`: no-reference leakage audit
- `candidates/qwen3_8b_k8_100_v9_regen_seed123.jsonl.gz`: compressed regenerated candidate file

## No-Reference Policy

Formal selection methods do not use reference objectives, objective correctness labels, oracle labels, reference LPs, or reference answers. Oracle metrics are post-hoc diagnostics only.
