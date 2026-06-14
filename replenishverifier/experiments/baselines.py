"""Strong non-domain-specific baselines for paper experiments.

These baselines intentionally avoid replenishment semantics and expected_structures.
They use only candidate-observable execution signals and generic LP artifacts.
"""

import re


DOMAIN_TERMS = {
    "inventory",
    "balance",
    "shortage",
    "backlog",
    "capacity",
    "setup",
    "fixed",
    "big_m",
    "bigm",
    "holding",
}


def compute_lp_stats(parsed):
    if parsed is None:
        return {
            "lp_exported": False,
            "objective_present": False,
            "constraints_present": False,
            "variables_count": 0,
            "constraints_count": 0,
            "binary_variables_count": 0,
            "bounds_count": 0,
            "bounds_present": False,
        }
    return {
        "lp_exported": True,
        "objective_present": bool(parsed.objective.strip()),
        "constraints_present": len(parsed.constraint_names) > 0,
        "variables_count": len(parsed.variable_names),
        "constraints_count": len(parsed.constraint_names),
        "binary_variables_count": len(parsed.binary_variables),
        "bounds_count": len(parsed.bounds),
        "bounds_present": len(parsed.bounds) > 0,
    }


def _cap_count(value, cap):
    if value <= 0:
        return 0.0
    return min(float(value) / float(cap), 1.0)


def sirl_like_lp_stats_score(execution_result, lp_stats):
    """Generic solver + LP artifact score, with no replenishment semantics."""
    executable = 1.0 if execution_result.get("executable") else 0.0
    optimal = 1.0 if execution_result.get("status") == "Optimal" else 0.0
    lp_exported = 1.0 if lp_stats.get("lp_exported") else 0.0
    objective_present = 1.0 if lp_stats.get("objective_present") else 0.0
    constraints_present = 1.0 if lp_stats.get("constraints_present") else 0.0
    variable_signal = _cap_count(lp_stats.get("variables_count", 0), cap=5)
    constraint_signal = _cap_count(lp_stats.get("constraints_count", 0), cap=5)
    binary_signal = 1.0 if lp_stats.get("binary_variables_count", 0) > 0 else 0.0
    bounds_signal = 1.0 if lp_stats.get("bounds_present") else 0.0

    return float(
        0.22 * executable
        + 0.22 * optimal
        + 0.12 * lp_exported
        + 0.10 * objective_present
        + 0.10 * constraints_present
        + 0.08 * variable_signal
        + 0.08 * constraint_signal
        + 0.04 * binary_signal
        + 0.04 * bounds_signal
    )


def _name_is_suspicious(name):
    lowered = name.lower()
    if lowered in {"x", "x_0", "var", "var_0", "dummy", "dummy_0"}:
        return True
    return any(term in lowered for term in {"dummy", "foo", "bar", "test"})


def compute_optargus_audit(parsed, execution_result=None):
    lp_stats = compute_lp_stats(parsed)
    variable_names = parsed.variable_names if parsed is not None else []
    constraint_names = parsed.constraint_names if parsed is not None else []
    objective = parsed.objective if parsed is not None else ""

    suspicious_names = [name for name in variable_names if _name_is_suspicious(name)]
    empty_model = not lp_stats["objective_present"] or not lp_stats["variables_count"] or not lp_stats["constraints_count"]
    objective_has_variable = any(name in objective for name in variable_names)
    bounded_ratio = 1.0 if lp_stats["bounds_present"] else 0.0
    if variable_names:
        bounded_names = set()
        for bound in (parsed.bounds if parsed is not None else []):
            for name in variable_names:
                if name in bound:
                    bounded_names.add(name)
        # PuLP often omits default nonnegative bounds, so do not over-penalize missing bounds.
        bounded_ratio = max(bounded_ratio, len(bounded_names) / max(len(variable_names), 1))

    audit = {
        "objective_present": lp_stats["objective_present"],
        "variables_present": lp_stats["variables_count"] > 0,
        "constraints_present": lp_stats["constraints_count"] > 0,
        "empty_model": empty_model,
        "objective_has_variable": objective_has_variable,
        "bounded_variables_ratio": float(bounded_ratio),
        "suspicious_variable_names": suspicious_names,
        "suspicious_variable_name_count": len(suspicious_names),
        "solver_error": bool(execution_result and execution_result.get("status") in {"Error", "Timeout", "Missing"}),
    }
    return audit


def optargus_like_audit_score(execution_result, audit):
    executable = 1.0 if execution_result.get("executable") else 0.0
    optimal = 1.0 if execution_result.get("status") == "Optimal" else 0.0
    objective_present = 1.0 if audit.get("objective_present") else 0.0
    variables_present = 1.0 if audit.get("variables_present") else 0.0
    constraints_present = 1.0 if audit.get("constraints_present") else 0.0
    non_empty = 0.0 if audit.get("empty_model") else 1.0
    objective_has_variable = 1.0 if audit.get("objective_has_variable") else 0.0
    bounded_ratio = float(audit.get("bounded_variables_ratio", 0.0))
    suspicious_penalty = min(audit.get("suspicious_variable_name_count", 0) * 0.1, 0.3)

    score = (
        0.18 * executable
        + 0.16 * optimal
        + 0.14 * objective_present
        + 0.14 * variables_present
        + 0.14 * constraints_present
        + 0.10 * non_empty
        + 0.08 * objective_has_variable
        + 0.06 * bounded_ratio
        - suspicious_penalty
    )
    return float(max(score, 0.0))


def optirepair_like_score(execution_result, audit):
    """Generic repair-style baseline score.

    This imitates generic diagnosis/repair readiness: prefer executable/optimal
    candidates with fewer generic audit issues, but do not use replenishment
    semantics or expected structures.
    """
    executable = 1.0 if execution_result.get("executable") else 0.0
    optimal = 1.0 if execution_result.get("status") == "Optimal" else 0.0
    audit_score = optargus_like_audit_score(execution_result, audit)
    return float(0.35 * executable + 0.25 * optimal + 0.40 * audit_score)


def generic_repair_feedback(execution_result, audit):
    messages = []
    if not execution_result.get("executable"):
        messages.append("Fix Python/PuLP execution errors so the model can be built and solved.")
    if not audit.get("objective_present"):
        messages.append("Add a clear optimization objective to the PuLP model.")
    if not audit.get("variables_present"):
        messages.append("Add decision variables to the model.")
    if not audit.get("constraints_present"):
        messages.append("Add constraints that define the feasible region.")
    if audit.get("empty_model"):
        messages.append("The model appears empty or underspecified; ensure objective, variables, and constraints are all present.")
    if audit.get("suspicious_variable_names"):
        messages.append("Rename suspicious placeholder variables to meaningful decision-variable names.")
    if not messages:
        messages.append("No generic optimization-model audit issue found; if the model is wrong, inspect domain-specific constraints.")
    return "\n".join(f"- {message}" for message in messages)


def classify_error_type(row):
    execution = row.get("execution") or {}
    structure = row.get("structure_verification") or {}
    audit = row.get("optargus_audit") or {}
    missing = structure.get("missing") or []

    if not execution.get("executable"):
        status = execution.get("status")
        if status == "Timeout":
            return "execution_timeout"
        return "execution_error"
    if execution.get("status") != "Optimal":
        return "solver_not_optimal"
    if audit.get("empty_model"):
        return "generic_empty_or_underspecified_model"
    if "inventory_balance" in missing:
        return "missing_inventory_balance"
    if "capacity_constraint" in missing:
        return "missing_capacity_constraint"
    if "big_m_constraint" in missing:
        return "missing_big_m_constraint"
    if "binary_order_variable" in missing:
        return "missing_binary_order_variable"
    if "shortage_variable" in missing:
        return "missing_shortage_variable"
    if any(key in missing for key in ["holding_cost", "shortage_cost", "fixed_order_cost"]):
        return "missing_cost_term"
    if missing:
        return "other_missing_structure"
    if not row.get("objective_correct", 0.0):
        return "objective_mismatch_after_selection"
    return "no_error_detected"
