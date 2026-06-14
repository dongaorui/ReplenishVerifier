import time
from pathlib import Path

from replenishverifier.experiments.baselines import (
    code_output_format_valid,
    compute_lp_stats,
    compute_objective_consensus_scores,
    compute_optargus_audit,
    generic_repair_feedback,
    optargus_like_audit_score,
    optirepair_like_score,
    or_r1_like_voting_score,
    sirl_like_lp_stats_score,
)
from replenishverifier.pipeline.scoring import compute_score
from replenishverifier.solver.code_executor import execute_generated_code
from replenishverifier.verifier.feedback import generate_feedback
from replenishverifier.verifier.lp_parser import parse_lp_file
from replenishverifier.verifier.structure_rules import check_structures


METHODS = [
    "Direct",
    "Best-of-K",
    "Solver-Filter",
    "OR-R1-like Voting",
    "SIRL-like LP-Stats",
    "OptArgus-like Audit",
    "OptiRepair-like Repair-Prompt",
    "Structure-Only",
    "ReplenishVerifier-Full",
    "ReplenishVerifier-Repair",
]


def candidate_sort_key(candidate):
    cid = str(candidate.get("candidate_id", ""))
    return cid


def evaluate_candidate(candidate, reference, work_dir, timeout=30, force_skip_execution=False):
    start = time.perf_counter()
    pid = candidate.get("problem_id")
    cid = candidate.get("candidate_id", "candidate")

    if force_skip_execution:
        execution = {
            "executable": False,
            "status": "NotRun",
            "objective": None,
            "lp_path": None,
            "error": "Execution skipped by method.",
        }
        structure_dict = None
        feedback = "该方法不执行候选代码，因此没有结构反馈。"
    else:
        execution = execute_generated_code(
            candidate.get("generated_code", ""),
            run_dir=Path(work_dir) / pid / cid,
            candidate_id=cid,
            timeout=timeout,
        )
        parsed = None
        structure_dict = None
        feedback = "候选代码没有成功导出 LP，因此无法执行结构验证。"
        if execution.get("lp_path"):
            try:
                parsed = parse_lp_file(execution["lp_path"])
                structure_result = check_structures(parsed, reference["expected_structures"], problem_type=reference.get("problem_type"))
                structure_dict = structure_result.to_dict()
                feedback = generate_feedback(structure_result)
            except Exception as exc:
                structure_dict = {
                    "expected": reference.get("expected_structures", {}),
                    "detected": {},
                    "passed": {},
                    "missing": [],
                    "extra_detected": [],
                    "structure_score": 0.0,
                    "messages": [f"LP parse or structure check error: {exc}"],
                }
                feedback = f"LP 解析或结构验证失败：{exc}"

    if force_skip_execution:
        parsed = None
    lp_stats = compute_lp_stats(parsed)
    optargus_audit = compute_optargus_audit(parsed, execution)
    sirl_lp_stats_score = sirl_like_lp_stats_score(execution, lp_stats)
    optargus_audit_score = optargus_like_audit_score(execution, optargus_audit)
    optirepair_repair_score = optirepair_like_score(execution, optargus_audit)
    generic_feedback = generic_repair_feedback(execution, optargus_audit)

    runtime = time.perf_counter() - start
    base = {
        "problem_id": pid,
        "candidate_id": cid,
        "candidate_method": candidate.get("method"),
        "generated_text": candidate.get("generated_text", ""),
        "execution": execution,
        "structure_verification": structure_dict,
        "feedback": feedback,
        "generic_repair_feedback": generic_feedback,
        "lp_stats": lp_stats,
        "optargus_audit": optargus_audit,
        "sirl_like_lp_stats_score": sirl_lp_stats_score,
        "optargus_like_audit_score": optargus_audit_score,
        "optirepair_like_repair_score": optirepair_repair_score,
        "runtime_sec": float(runtime),
        "problem_type": reference.get("problem_type"),
        "difficulty": reference.get("difficulty"),
        "reference_objective": reference.get("reference_objective"),
        "reference_status": reference.get("reference_status"),
        "code_output_format_valid": code_output_format_valid(candidate.get("generated_code", "")),
        "objective_consensus_score": 0.0,
        "or_r1_like_voting_score": 0.0,
    }
    base.update(compute_score(execution, structure_dict, reference.get("reference_objective"), mode="full"))
    solver_score = compute_score(execution, structure_dict, reference.get("reference_objective"), mode="solver_only")
    structure_score = compute_score(execution, structure_dict, reference.get("reference_objective"), mode="structure_only")
    base["solver_only_score"] = solver_score["score"]
    base["structure_only_score"] = structure_score["score"]
    base["formal_selection_score"] = base["score"]
    return base


def annotate_consensus_scores(evaluated):
    """Attach ground-truth-free objective consensus and OR-R1-like scores."""
    for rows in evaluated.values():
        consensus_scores = compute_objective_consensus_scores(rows)
        for row, consensus_score in zip(rows, consensus_scores):
            row["objective_consensus_score"] = float(consensus_score)
            row["or_r1_like_voting_score"] = or_r1_like_voting_score(
                row.get("execution") or {},
                consensus_score=consensus_score,
                code_format_valid=row.get("code_output_format_valid", False),
            )
    return evaluated


def apply_objective_consensus_to_full_scores(evaluated, weight=0.10):
    """Optionally blend objective-consensus into ReplenishVerifier-Full selection.

    Consensus is computed only from candidate objectives within the same problem,
    never from the reference objective.
    """
    for rows in evaluated.values():
        for row in rows:
            base_score = float(row.get("score", 0.0) or 0.0)
            consensus = float(row.get("objective_consensus_score", 0.0) or 0.0)
            row["base_replenishverifier_score"] = base_score
            row["score"] = float((1.0 - weight) * base_score + weight * consensus)
            row["selection_score"] = row["score"]
            row["formal_selection_score"] = row["score"]
            row["selection_policy"] = (
                "executable + optimal + LP structure + semantic consistency + "
                "candidate objective consensus; no reference objective"
            )
    return evaluated


def evaluate_all_candidates(benchmark, candidates_by_problem, work_dir, timeout=30, max_k=None, use_objective_consensus=False):
    evaluated = {}
    for pid, reference in benchmark.items():
        candidates = sorted(candidates_by_problem.get(pid, []), key=candidate_sort_key)
        if max_k is not None:
            candidates = candidates[:max_k]
        rows = []
        for candidate in candidates:
            rows.append(evaluate_candidate(candidate, reference, work_dir=work_dir, timeout=timeout))
        evaluated[pid] = rows
    annotate_consensus_scores(evaluated)
    if use_objective_consensus:
        apply_objective_consensus_to_full_scores(evaluated)
    return evaluated


def _first_or_empty(pid, reference):
    return {
        "problem_id": pid,
        "candidate_id": "missing_candidate",
        "candidate_method": None,
        "execution": {"executable": False, "status": "Missing", "objective": None, "lp_path": None, "error": "No candidate for this problem."},
        "structure_verification": None,
        "feedback": "没有候选答案。",
        "runtime_sec": 0.0,
        "problem_type": reference.get("problem_type"),
        "difficulty": reference.get("difficulty"),
        "reference_objective": reference.get("reference_objective"),
        "reference_status": reference.get("reference_status"),
        "score": 0.0,
        "executable_score": 0.0,
        "feasible_score": 0.0,
        "optimal_score": 0.0,
        "objective_score": 0.0,
        "objective_correct": 0.0,
        "relative_error": None,
        "structure_score": 0.0,
        "semantic_consistency_score": 0.0,
        "solver_only_score": 0.0,
        "structure_only_score": 0.0,
    }


def select_for_method(method_name, evaluated_by_problem, benchmark):
    selected = []
    for pid, reference in benchmark.items():
        rows = list(evaluated_by_problem.get(pid, []))
        if not rows:
            best = _first_or_empty(pid, reference)
        elif method_name == "Direct":
            best = rows[0]
        elif method_name == "Best-of-K":
            executable = [row for row in rows if row.get("execution", {}).get("executable")]
            best = executable[0] if executable else rows[0]
        elif method_name == "Solver-Filter":
            best = max(rows, key=lambda row: row.get("solver_only_score", 0.0))
        elif method_name == "OR-R1-like Voting":
            best = max(rows, key=lambda row: row.get("or_r1_like_voting_score", 0.0))
        elif method_name == "SIRL-like LP-Stats":
            best = max(rows, key=lambda row: row.get("sirl_like_lp_stats_score", 0.0))
        elif method_name == "OptArgus-like Audit":
            best = max(rows, key=lambda row: row.get("optargus_like_audit_score", 0.0))
        elif method_name == "OptiRepair-like Repair-Prompt":
            best = max(rows, key=lambda row: row.get("optirepair_like_repair_score", 0.0))
        elif method_name == "Structure-Only":
            best = max(rows, key=lambda row: row.get("structure_only_score", 0.0))
        elif method_name in {"ReplenishVerifier-Full", "ReplenishVerifier-Repair"}:
            best = max(rows, key=lambda row: row.get("score", 0.0))
        else:
            raise ValueError(f"Unknown method: {method_name}")

        best = dict(best)
        best["method_name"] = method_name
        if method_name == "OR-R1-like Voting":
            best["score"] = best.get("or_r1_like_voting_score", 0.0)
            best["selection_score"] = best["score"]
            best["selection_policy"] = "executable + optimal + valid code/LP output + candidate objective consensus; no replenishment semantics; no reference objective"
        elif method_name == "SIRL-like LP-Stats":
            best["score"] = best.get("sirl_like_lp_stats_score", 0.0)
            best["selection_score"] = best["score"]
            best["selection_policy"] = "generic solver + LP artifact statistics; no replenishment semantics; no reference objective"
        elif method_name == "OptArgus-like Audit":
            best["score"] = best.get("optargus_like_audit_score", 0.0)
            best["selection_score"] = best["score"]
            best["selection_policy"] = "generic hallucination audit signals; no replenishment semantics; no reference objective"
        elif method_name == "OptiRepair-like Repair-Prompt":
            best["score"] = best.get("optirepair_like_repair_score", 0.0)
            best["selection_score"] = best["score"]
            best["selection_policy"] = "generic repair-readiness score from execution and audit issues; no replenishment semantics; no reference objective"
            best["feedback"] = best.get("generic_repair_feedback", best.get("feedback", ""))
        elif method_name == "Solver-Filter":
            best["score"] = best.get("solver_only_score", 0.0)
            best["selection_score"] = best["score"]
            best["selection_policy"] = "executable > optimal > has_objective; no reference objective"
        elif method_name == "Structure-Only":
            best["score"] = best.get("structure_only_score", 0.0)
            best["selection_score"] = best["score"]
            best["selection_policy"] = "replenishment LP structure completeness only; no reference objective"
        elif method_name == "Direct":
            best["selection_policy"] = "candidate order only; no reference objective"
        elif method_name == "Best-of-K":
            best["selection_policy"] = "first executable candidate in order; no reference objective"
        best["uses_reference_objective_for_selection"] = False
        best["selected"] = True
        selected.append(best)
    return selected


def build_repair_prompts(rows):
    """Build repair prompts for every candidate with missing required structures."""
    prompts = []
    for row in rows:
        structure = row.get("structure_verification") or {}
        missing = structure.get("missing") or []
        if not missing:
            continue
        prompt = {
            "problem_id": row["problem_id"],
            "candidate_id": row["candidate_id"],
            "method_name": row.get("method_name", "candidate"),
            "candidate_method": row.get("candidate_method"),
            "repair_feedback_count": len(missing),
            "missing_structures": missing,
            "feedback": row.get("feedback", ""),
            "repair_prompt": (
                "You are fixing a PuLP optimization model for an inventory replenishment problem.\n"
                "Revise the generated code according to the structure feedback below.\n"
                "Keep variable names interpretable: Q for order, I for inventory, B for shortage, Y for binary trigger.\n\n"
                f"Problem ID: {row.get('problem_id')}\n"
                f"Candidate ID: {row.get('candidate_id')}\n\n"
                f"Feedback:\n{row.get('feedback', '')}\n"
            ),
        }
        prompts.append(prompt)
    return prompts
