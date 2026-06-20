# Qwen3-8B k=8 / 100-problem TypeAware Consensus Rerank Experiment

This folder contains the final experiment artifacts for:

- model: Qwen/Qwen3-8B
- benchmark: data/generated/test_100_v6.jsonl
- candidates: data/candidates/qwen3_8b_k8_100_v6_typeaware.jsonl
- k: 8
- number of problems: 100
- total candidates: 800

## Contents

- `main_results.md`: main method comparison table
- `diagnostics/`: selection diagnostics and redundancy analysis
- `paper_metrics/`: paper-ready metrics and oracle/pass@k tables
- `candidates/`: the 800 generated candidate records used for this experiment
- `logs/`: execution logs for reproducibility

## Important Note

The candidate file contains already-generated LLM outputs. The experiment reruns selection, diagnostics, error analysis, leakage audit, and paper metrics without regenerating candidates.

Formal selection must not use reference objective, objective_correct, oracle, reference LP, or reference answer.
