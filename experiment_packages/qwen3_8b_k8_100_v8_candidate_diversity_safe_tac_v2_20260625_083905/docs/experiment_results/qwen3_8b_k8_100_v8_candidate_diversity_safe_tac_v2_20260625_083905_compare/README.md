# qwen3_8b_k8_100_v8_candidate_diversity_safe_tac_v2_20260625_083905

This directory contains the Qwen3-8B k=8 candidate-diversity Safe TypeAware-Consensus v2 experiment.

## Key Files

- `main_results.md`: full method results
- `analysis_summary.md`: high-level interpretation
- `diagnostics/`: diagnostic reports
- `paper_metrics/`: paper-ready metrics
- `no_leakage_audit.json`: no-reference leakage audit
- `candidates/qwen3_8b_k8_100_v8_candidate_diversity.jsonl.gz`: compressed candidate file

## No-Reference Policy

Formal selection methods do not use reference objectives, objective correctness labels, oracle labels, reference LPs, or reference answers. Oracle metrics are post-hoc diagnostics only.
