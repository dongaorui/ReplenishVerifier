# qwen3_8b_k8_100_v8_candidate_diversity_rerun_20260622_085435

This directory contains the Qwen3-8B k=8 candidate-diversity experiment results on the 100-problem replenishment optimization benchmark.

## Key Files

- `main_results.md`: main method comparison
- `analysis_summary.md`: high-level interpretation
- `error_type_summary.md`: error type summary
- `diagnostics/`: diagnostic reports
- `paper_metrics/`: paper-ready metrics
- `no_leakage_audit.json`: no-reference leakage audit
- `candidates/qwen3_8b_k8_100_v8_candidate_diversity.jsonl.gz`: compressed candidate file

## No-Reference Policy

Formal selection methods do not use reference objectives, objective correctness, oracle labels, reference LPs, or reference answers. Oracle metrics are post-hoc diagnostics only.
