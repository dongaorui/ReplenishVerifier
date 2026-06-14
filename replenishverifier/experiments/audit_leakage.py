import argparse
import sys
from pathlib import Path

from replenishverifier.utils.io import read_jsonl


FORMAL_METHODS = {"Solver-Filter", "ReplenishVerifier-Full", "ReplenishVerifier-Repair"}


def audit(exp_dir):
    exp_dir = Path(exp_dir)
    issues = []
    main_path = exp_dir / "main_results.jsonl"
    rows = read_jsonl(main_path)
    if not rows:
        issues.append(f"No main_results rows found at {main_path}")
        return issues

    for idx, row in enumerate(rows):
        method = row.get("method_name")
        if method in FORMAL_METHODS:
            if row.get("uses_reference_objective_for_selection") is not False:
                issues.append(f"Row {idx} method={method} does not explicitly mark no reference-objective selection.")
            policy = str(row.get("selection_policy", "")).lower()
            if "reference objective" not in policy or "no reference" not in policy:
                issues.append(f"Row {idx} method={method} selection_policy is missing no-reference statement: {row.get('selection_policy')}")
            if row.get("selection_score") != row.get("score"):
                issues.append(f"Row {idx} method={method} score and selection_score differ unexpectedly.")

        # Objective metrics may be saved for reporting, but should not be selected by policy.
        if "objective_accuracy" in row or "objective_correct" in row or "objective_score" in row:
            policy = str(row.get("selection_policy", "")).lower()
            if method in FORMAL_METHODS and "no reference" not in policy:
                issues.append(f"Row {idx} method={method} stores objective metrics without no-reference selection policy.")

    # Check table summaries exist; they can report objective accuracy post-selection.
    expected = [
        "main_results.jsonl",
        "candidate_evaluations.jsonl",
        "ablation_results.jsonl",
        "low_resource_results.jsonl",
        "summary.md",
    ]
    for name in expected:
        if not (exp_dir / name).exists():
            issues.append(f"Missing expected output file: {exp_dir / name}")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Audit experiment outputs for ground-truth objective leakage in formal candidate selection.")
    parser.add_argument("--exp_dir", required=True)
    args = parser.parse_args()

    issues = audit(args.exp_dir)
    if issues:
        print("LEAKAGE AUDIT FAILED")
        for issue in issues:
            print(f"WARNING: {issue}")
        sys.exit(1)
    print("LEAKAGE AUDIT PASSED: no reference_objective usage detected in formal selection scores.")


if __name__ == "__main__":
    main()
