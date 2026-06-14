import argparse
import csv
from collections import defaultdict
from pathlib import Path

from replenishverifier.utils.io import read_jsonl, write_jsonl


def _feedback_count(row):
    structure = row.get("structure_verification") or {}
    return len(structure.get("missing") or [])


def _preference_score(row):
    execution = row.get("execution") or {}
    structure_score = float(row.get("structure_score", (row.get("structure_verification") or {}).get("structure_score", 0.0)) or 0.0)
    executable = 1.0 if execution.get("executable") else 0.0
    optimal = 1.0 if execution.get("status") == "Optimal" else 0.0
    feedback_penalty = min(_feedback_count(row) / 10.0, 1.0)
    return 0.25 * executable + 0.25 * optimal + 0.40 * structure_score + 0.10 * (1.0 - feedback_penalty)


def _candidate_text(row):
    return row.get("generated_text") or row.get("generated_code") or ""


def build_preference_pairs(exp_dir, out_path, min_score_gap=0.10, max_pairs_per_problem=3):
    exp_dir = Path(exp_dir)
    rows = read_jsonl(exp_dir / "candidate_evaluations.jsonl")
    if not rows:
        raise ValueError(f"No candidate_evaluations.jsonl found in {exp_dir}")

    grouped = defaultdict(list)
    for row in rows:
        grouped[row.get("problem_id")].append(row)

    pairs = []
    for pid, items in grouped.items():
        ranked = sorted(items, key=_preference_score, reverse=True)
        made = 0
        for chosen in ranked:
            if made >= max_pairs_per_problem:
                break
            for rejected in reversed(ranked):
                gap = _preference_score(chosen) - _preference_score(rejected)
                if gap < min_score_gap:
                    continue
                if chosen.get("candidate_id") == rejected.get("candidate_id"):
                    continue
                pairs.append({
                    "problem_id": pid,
                    "chosen_candidate_id": chosen.get("candidate_id"),
                    "rejected_candidate_id": rejected.get("candidate_id"),
                    "chosen_score": _preference_score(chosen),
                    "rejected_score": _preference_score(rejected),
                    "score_gap": gap,
                    "chosen_structure_score": chosen.get("structure_score"),
                    "rejected_structure_score": rejected.get("structure_score"),
                    "chosen_feedback_count": _feedback_count(chosen),
                    "rejected_feedback_count": _feedback_count(rejected),
                    "chosen": _candidate_text(chosen),
                    "rejected": _candidate_text(rejected),
                    "selection_policy": "preference pairs from executable + optimal + structure completeness + lower repair feedback; no reference objective",
                    "uses_reference_objective_for_preference": False,
                })
                made += 1
                break

    write_jsonl(out_path, pairs)
    write_csv(Path(out_path).with_suffix(".csv"), pairs)
    return pairs


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = [
        "problem_id",
        "chosen_candidate_id",
        "rejected_candidate_id",
        "chosen_score",
        "rejected_score",
        "score_gap",
        "chosen_structure_score",
        "rejected_structure_score",
        "chosen_feedback_count",
        "rejected_feedback_count",
        "selection_policy",
        "uses_reference_objective_for_preference",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def main():
    parser = argparse.ArgumentParser(description="Build preference pairs from ReplenishVerifier candidate evaluations.")
    parser.add_argument("--exp_dir", required=True, help="Experiment directory produced by run_all_methods.")
    parser.add_argument("--out", required=True, help="Output JSONL path for preference pairs.")
    parser.add_argument("--min_score_gap", type=float, default=0.10)
    parser.add_argument("--max_pairs_per_problem", type=int, default=3)
    args = parser.parse_args()

    pairs = build_preference_pairs(
        exp_dir=args.exp_dir,
        out_path=args.out,
        min_score_gap=args.min_score_gap,
        max_pairs_per_problem=args.max_pairs_per_problem,
    )
    print(f"Wrote {len(pairs)} preference pairs to {args.out}")


if __name__ == "__main__":
    main()
