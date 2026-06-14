def relative_error(candidate_obj, reference_obj):
    if candidate_obj is None or reference_obj is None:
        return None
    err = abs(candidate_obj - reference_obj)
    denom = max(abs(reference_obj), 1.0)
    return float(err / denom)


def strict_objective_correct(candidate_obj, reference_obj, rel_tol=1e-4, abs_tol=1e-4):
    if candidate_obj is None or reference_obj is None:
        return False
    err = abs(candidate_obj - reference_obj)
    if abs(reference_obj) <= abs_tol:
        return err <= abs_tol
    return err / abs(reference_obj) <= rel_tol


def objective_accuracy(candidate_obj, reference_obj, rel_tol=1e-4, abs_tol=1e-4):
    """Evaluation-only soft objective score in [0, 1].

    This function uses the reference objective and must not be used for formal
    candidate selection. It is only for reporting metrics after selection.
    """
    if candidate_obj is None or reference_obj is None:
        return 0.0
    err = abs(candidate_obj - reference_obj)
    denom = max(abs(reference_obj), 1.0)
    rel = err / denom
    if err <= abs_tol or rel <= rel_tol:
        return 1.0
    return max(0.0, 1.0 - rel)


def semantic_consistency_score(structure_result):
    """Prototype semantic consistency: all required structures present => 1, else structure score."""
    if not structure_result:
        return 0.0
    missing = structure_result.get("missing", [])
    if not missing:
        return 1.0
    return float(structure_result.get("structure_score", 0.0))


def solver_selection_score(execution_result):
    """Ground-truth-free solver-only selection score.

    Solver-Filter is allowed to use only observed execution/solver signals from
    the candidate itself. It must not use reference_objective.
    """
    executable = 1.0 if execution_result.get("executable") else 0.0
    optimal = 1.0 if execution_result.get("status") == "Optimal" else 0.0
    has_objective = 1.0 if execution_result.get("objective") is not None else 0.0
    return float(0.45 * executable + 0.45 * optimal + 0.10 * has_objective)


def full_selection_score(execution_result, structure_result):
    """Ground-truth-free ReplenishVerifier selection score."""
    executable = 1.0 if execution_result.get("executable") else 0.0
    optimal = 1.0 if execution_result.get("status") == "Optimal" else 0.0
    struct_score = structure_result.get("structure_score", 0.0) if structure_result else 0.0
    semantic_score = semantic_consistency_score(structure_result)
    return float(0.25 * executable + 0.25 * optimal + 0.35 * struct_score + 0.15 * semantic_score)


def compute_score(execution_result, structure_result, reference_objective=None, mode="full"):
    """Compute both formal selection scores and evaluation-only metrics.

    The returned `score` is always the formal selection score for the requested
    mode and never uses reference_objective. Objective metrics are still reported
    for evaluation but are not used by candidate selection.
    """
    executable = 1.0 if execution_result.get("executable") else 0.0
    status = execution_result.get("status")
    feasible = 1.0 if status in {"Optimal", "Feasible"} else 0.0
    optimal = 1.0 if status == "Optimal" else 0.0
    obj_score = objective_accuracy(execution_result.get("objective"), reference_objective)
    obj_correct = 1.0 if strict_objective_correct(execution_result.get("objective"), reference_objective) else 0.0
    struct_score = structure_result.get("structure_score", 0.0) if structure_result else 0.0
    semantic_score = semantic_consistency_score(structure_result)

    if mode == "solver_only":
        total = solver_selection_score(execution_result)
        policy = "executable > optimal > has_objective; no reference objective"
    elif mode == "structure_only":
        total = struct_score
        policy = "LP structure completeness only; no reference objective"
    elif mode == "direct":
        total = 0.0
        policy = "candidate order only; no reference objective"
    else:
        total = full_selection_score(execution_result, structure_result)
        policy = "executable + optimal + LP structure + semantic consistency; no reference objective"

    return {
        "score": float(total),
        "selection_score": float(total),
        "selection_policy": policy,
        "uses_reference_objective_for_selection": False,
        "executable_score": executable,
        "feasible_score": feasible,
        "optimal_score": optimal,
        "objective_score": float(obj_score),
        "objective_correct": obj_correct,
        "objective_accuracy": obj_correct,
        "relative_error": relative_error(execution_result.get("objective"), reference_objective),
        "structure_score": float(struct_score),
        "semantic_consistency_score": float(semantic_score),
    }
