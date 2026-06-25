import argparse
import json
from pathlib import Path

from replenishverifier.experiments.evaluation import save_markdown_table, save_result_bundle, summarize_by_method
from replenishverifier.experiments.methods import APPENDIX_METHODS, MAIN_METHODS, METHODS, select_for_method
from replenishverifier.experiments.paper_metrics import candidate_index
from replenishverifier.utils.io import read_jsonl, write_jsonl


def _group_by_problem(rows):
    grouped = {}
    for row in rows:
        grouped.setdefault(row.get("problem_id"), []).append(row)
    return grouped


def _benchmark_from_candidates(rows):
    benchmark = {}
    for row in rows:
        pid = row.get("problem_id")
        if pid not in benchmark:
            benchmark[pid] = {
                "id": pid,
                "problem_type": row.get("problem_type"),
                "difficulty": row.get("difficulty"),
                "natural_language": row.get("natural_language", row.get("problem_text", "")),
            }
    return benchmark


def _write_low_resource_outputs(out_dir, evaluated_by_problem, benchmark, k_values, allow_feasible_selection=False):
    low_resource_rows = []
    low_resource_summary = []
    methods = [
        "Best-of-K",
        "Solver-Filter",
        "OR-R1-like Voting",
        "Structure-Grounded Consistency",
        "SIRL-like LP-Stats",
        "OptArgus-like Audit",
        "OptiRepair-like Repair-Prompt",
        "Structure-Only",
        "ReplenishVerifier-TypeAware",
        "ReplenishVerifier-TypeAware-Consensus",
        "ReplenishVerifier-ConsensusSafe",
        "ReplenishVerifier-HybridSafe",
        "ReplenishVerifier-FullV2",
        "ReplenishVerifier-Full",
    ]
    for k in k_values:
        eval_k = {
            pid: sorted(rows, key=lambda row: candidate_index(row.get("candidate_id")))[:k]
            for pid, rows in evaluated_by_problem.items()
        }
        for method in methods:
            selected = select_for_method(method, eval_k, benchmark, allow_feasible_selection=allow_feasible_selection)
            for row in selected:
                row["k"] = k
            low_resource_rows.extend(selected)
            summary = summarize_by_method(selected)[0]
            summary["k"] = k
            low_resource_summary.append(summary)
    save_result_bundle(out_dir / "low_resource_results", low_resource_rows, summary_rows=low_resource_summary, title="Low-Resource K Analysis")


def reselect_existing(exp_dir, out_dir, appendix_methods_in_main=False, allow_feasible_selection=False, k_values=None):
    exp_dir = Path(exp_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    candidate_rows = read_jsonl(exp_dir / "candidate_evaluations.jsonl")
    evaluated_by_problem = _group_by_problem(candidate_rows)
    benchmark = _benchmark_from_candidates(candidate_rows)
    main_methods = METHODS if appendix_methods_in_main else MAIN_METHODS
    main_rows = []
    for method in main_methods:
        main_rows.extend(select_for_method(method, evaluated_by_problem, benchmark, allow_feasible_selection=allow_feasible_selection))
    main_summary = summarize_by_method(main_rows)
    save_result_bundle(out_dir / "main_results", main_rows, summary_rows=main_summary, title="Main Results")
    write_jsonl(out_dir / "candidate_evaluations.jsonl", candidate_rows)
    ablation_methods = [
        "Direct",
        "Best-of-K",
        "Solver only",
        "Structure only",
        "Consensus only",
        "Solver + Structure",
        "Solver + Consensus",
        "Structure + Consensus",
        "Solver + Structure + Consensus",
        "ReplenishVerifier full",
        "Solver-Filter",
        "OR-R1-like Voting",
        "Structure-Grounded Consistency",
        "Structure-Only",
        "ReplenishVerifier-TypeAware",
        "ReplenishVerifier-TypeAware-Consensus",
        "ReplenishVerifier-Full",
        "ReplenishVerifier-FullV2-CandidatePoolAware",
    ]
    ablation_rows = []
    for method in ablation_methods:
        ablation_rows.extend(select_for_method(method, evaluated_by_problem, benchmark, allow_feasible_selection=allow_feasible_selection))
    save_result_bundle(out_dir / "ablation_results", ablation_rows, summary_rows=summarize_by_method(ablation_rows), title="Ablation Results")
    _write_low_resource_outputs(out_dir, evaluated_by_problem, benchmark, k_values or [1, 2, 4, 8], allow_feasible_selection=allow_feasible_selection)
    save_markdown_table(out_dir / "summary.md", main_summary, title="Experiment Summary")
    manifest = {
        "source_exp_dir": str(exp_dir),
        "out_dir": str(out_dir),
        "n_candidates": len(candidate_rows),
        "n_problems": len(benchmark),
        "main_methods": main_methods,
        "appendix_methods": APPENDIX_METHODS,
        "appendix_methods_in_main": bool(appendix_methods_in_main),
        "allow_feasible_selection": bool(allow_feasible_selection),
        "k_values": k_values or [1, 2, 4, 8],
        "selection_only_rerun": True,
        "uses_reference_objective_for_selection": False,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Re-select methods from existing candidate_evaluations.jsonl without re-executing candidates.")
    parser.add_argument("--exp_dir", required=True)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--appendix_methods_in_main", action="store_true")
    parser.add_argument("--allow_feasible_selection", action="store_true")
    parser.add_argument("--k_values", default="1,2,4,8")
    args = parser.parse_args()
    k_values = [int(part.strip()) for part in str(args.k_values).split(",") if part.strip()]
    reselect_existing(
        args.exp_dir,
        args.out_dir,
        appendix_methods_in_main=args.appendix_methods_in_main,
        allow_feasible_selection=args.allow_feasible_selection,
        k_values=k_values,
    )


if __name__ == "__main__":
    main()
