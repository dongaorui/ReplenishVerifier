# qwen3_8b_k8_100_v8_candidate_diversity_safe_tac_20260624_201823

This directory contains the Qwen3-8B k=8 candidate-diversity safe TypeAware-Consensus experiment.

## Key Files

- `main_results.md`: full method results
- `analysis_summary.md`: high-level interpretation
- `diagnostics/suspicious_consensus_clusters.csv`: suspicious consensus diagnostics
- `diagnostics/consensus_only_vs_tac_diff.csv`: Consensus only vs TypeAware-Consensus comparison
- `diagnostics/structure_only_vs_tac_diff.csv`: Structure only vs TypeAware-Consensus comparison
- `diagnostics/selector_score_components.csv`: selector score components
- `paper_metrics/table_by_problem_type.md`: by-problem-type analysis
- `paper_metrics/table_hard_subset.md`: hard subset robustness analysis
- `no_leakage_audit.json`: no-reference leakage audit

## No-Reference Policy

Formal selection methods do not use reference objectives, objective correctness labels, oracle labels, reference LPs, or reference answers. Oracle metrics are post-hoc diagnostics only.
