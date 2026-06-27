from replenishverifier.experiments.deep_semantic_validation import (
    compute_deep_type_aware_validation,
    compute_semantic_structure_validation,
)
from replenishverifier.experiments.methods import select_for_method
from replenishverifier.verifier.lp_parser import parse_lp_text


FORBIDDEN_SELECTION_KEYS = {
    "reference_objective",
    "objective_correct",
    "objective_accuracy",
    "relative_error",
    "oracle",
    "oracle_rank",
    "reference_lp",
    "reference_answer",
}


def _lp(objective="OBJ: Q_0 + I_0", constraints=None, bounds=None, binaries=None):
    constraints = constraints or {"c0": "I_0 - Q_0 = 0"}
    bounds = bounds or ["0 <= Q_0", "0 <= I_0"]
    lines = ["Minimize", objective, "Subject To"]
    lines.extend(f" {name}: {expr}" for name, expr in constraints.items())
    if bounds:
        lines.append("Bounds")
        lines.extend(f" {line}" for line in bounds)
    if binaries:
        lines.append("Binaries")
        lines.extend(f" {name}" for name in binaries)
    lines.append("End")
    return parse_lp_text("\n".join(lines))


def _row(candidate_id="c0", problem_type="single_item_multi_period", parsed=None, code="", objective=10.0, consensus=0.5):
    parsed = parsed or _lp()
    return {
        "problem_id": "p0",
        "candidate_id": candidate_id,
        "problem_type": problem_type,
        "generated_code": code,
        "execution": {"executable": True, "status": "Optimal", "objective": objective, "lp_path": f"{candidate_id}.lp"},
        "lp_stats": {"lp_exported": True, "objective_present": True, "constraints_count": len(parsed.constraints), "variables_count": len(parsed.variable_names), "binary_variables_count": len(parsed.binary_variables), "bounds_present": bool(parsed.bounds)},
        "structure_score": 1.0,
        "structure_verification": {"structure_score": 1.0, "required_structures": ["inventory_balance"], "missing": [], "certificates": []},
        "objective_consensus_score": consensus,
        "objective_term_coverage": 1.0,
        "objective_term_lp_coefficient_coverage": 1.0,
        "code_output_format_valid": True,
        "static_validation_score": 1.0,
        "type_aware_static_validation": {"score": 1.0, "hard_gate_score": 1.0, "hard_gate_failures": [], "missing_items": []},
        "type_aware_static_validation_errors": [],
        "parsed_lp": parsed,
    }


def test_newsvendor_python_max_on_lp_variable_is_deep_error():
    code = """
def build_model():
    Q = pulp.LpVariable('Q_0', lowBound=0)
    leftover = max(Q - 10, 0)
    model += leftover
"""
    result = compute_deep_type_aware_validation("single_period_newsvendor", generated_code=code, parsed=None)

    assert result["score"] < 1.0
    assert "newsvendor_python_max_on_lp_variable" in result["errors"]
    assert result["hard_gate_score"] < 1.0


def test_shortage_variable_without_shortage_cost_is_deep_error():
    parsed = _lp(
        objective="OBJ: 2 Q_0 + I_0",
        constraints={"balance_0": "I_0 - B_0 - Q_0 = -5"},
        bounds=["0 <= Q_0", "0 <= I_0", "0 <= B_0"],
    )

    result = compute_semantic_structure_validation("single_item_multi_period_shortage", parsed=parsed, generated_code="")

    assert result["score"] < 1.0
    assert "shortage_variable_without_shortage_cost" in result["errors"]


def test_single_variable_upper_bound_is_not_strong_shared_capacity():
    parsed = _lp(
        constraints={"capacity_0": "Q_0 <= 100", "balance_0": "I_0 - Q_0 = -5"},
        bounds=["0 <= Q_0", "0 <= I_0"],
    )

    result = compute_semantic_structure_validation("multi_item_capacity", parsed=parsed, generated_code="")

    assert result["capacity_shared_aggregation"] is False
    assert "capacity_not_shared_aggregation" in result["errors"]


def test_lead_time_uses_q_t_minus_l_not_current_q_t():
    wrong = _lp(
        constraints={"inventory_balance_2": "I_2 - I_1 - Q_2 = -20"},
        bounds=["0 <= Q_0", "0 <= Q_1", "0 <= Q_2", "0 <= I_1", "0 <= I_2"],
    )
    right = _lp(
        constraints={"lead_time_balance_2": "I_2 - I_1 - Q_0 = -20"},
        bounds=["0 <= Q_0", "0 <= Q_1", "0 <= Q_2", "0 <= I_1", "0 <= I_2"],
    )

    wrong_result = compute_semantic_structure_validation("single_item_multi_period_lead_time", parsed=wrong, generated_code="", parameters={"lead_time": 2})
    right_result = compute_semantic_structure_validation("single_item_multi_period_lead_time", parsed=right, generated_code="", parameters={"lead_time": 2})

    assert "lead_time_uses_current_order" in wrong_result["errors"]
    assert "lead_time_uses_current_order" not in right_result["errors"]
    assert right_result["score"] > wrong_result["score"]


def test_service_level_requires_explicit_service_constraint_not_only_shortage_penalty():
    parsed = _lp(
        objective="OBJ: Q_0 + 100 B_0",
        constraints={"balance_0": "I_0 - B_0 - Q_0 = -10"},
        bounds=["0 <= Q_0", "0 <= I_0", "0 <= B_0"],
    )

    result = compute_semantic_structure_validation("single_item_multi_period_service_level", parsed=parsed, generated_code="")

    assert "missing_service_level_constraint" in result["errors"]
    assert result["score"] < 1.0


def test_moq_forces_every_period_order_is_deep_error():
    parsed = _lp(
        constraints={"moq_0": "Q_0 >= 10", "balance_0": "I_0 - Q_0 = -5"},
        bounds=["0 <= Q_0", "0 <= I_0"],
    )

    result = compute_semantic_structure_validation("single_item_multi_period_moq_batch", parsed=parsed, generated_code="")

    assert "moq_forces_order_every_period" in result["errors"]


def test_batch_multiplier_must_be_integer():
    parsed = _lp(
        constraints={"batch_0": "Q_0 - 5 z_0 = 0"},
        bounds=["0 <= Q_0", "0 <= z_0"],
    )

    result = compute_semantic_structure_validation("single_item_multi_period_moq_batch", parsed=parsed, generated_code="")

    assert "batch_multiplier_not_integer" in result["errors"]


def test_formal_tac_deep_components_exclude_reference_oracle_keys():
    bad = _row(
        "bad_k0",
        problem_type="single_item_multi_period_shortage",
        parsed=_lp(objective="OBJ: Q_0 + I_0", constraints={"balance_0": "I_0 - B_0 - Q_0 = -5"}, bounds=["0 <= Q_0", "0 <= I_0", "0 <= B_0"]),
        consensus=0.9,
    )
    good = _row(
        "good_k1",
        problem_type="single_item_multi_period_shortage",
        parsed=_lp(objective="OBJ: Q_0 + I_0 + 9 B_0", constraints={"balance_0": "I_0 - B_0 - Q_0 = -5"}, bounds=["0 <= Q_0", "0 <= I_0", "0 <= B_0"]),
        consensus=0.5,
    )
    for row in [bad, good]:
        row["reference_objective"] = 123
        row["objective_correct"] = 0
        row["semantic_structure_validation"] = compute_semantic_structure_validation(row["problem_type"], parsed=row["parsed_lp"], generated_code=row["generated_code"])
        row["deep_type_aware_validation"] = compute_deep_type_aware_validation(row["problem_type"], generated_code=row["generated_code"], parsed=row["parsed_lp"])

    selected = select_for_method(
        "ReplenishVerifier-TypeAware-Consensus",
        {"p0": [bad, good]},
        {"p0": {"problem_type": "single_item_multi_period_shortage"}},
    )[0]

    assert selected["candidate_id"] == "good_k1"
    assert set(selected["selection_components"]).isdisjoint(FORBIDDEN_SELECTION_KEYS)
    assert "deep_semantic_score" in selected["selection_components"]


def test_old_fixed_order_binary_big_m_behavior_still_prefers_binary_linked_candidate():
    required = ["inventory_balance", "order_variable", "binary_order_variable", "big_m_constraint", "fixed_order_cost"]
    bad = _row("continuous_k0", problem_type="fixed_order_cost_big_m", parsed=_lp(binaries=[]), consensus=0.9)
    bad["structure_verification"] = {"structure_score": 0.8, "required_structures": required, "missing": ["binary_order_variable"], "certificates": []}
    bad["structure_score"] = 0.8
    good = _row("binary_k1", problem_type="fixed_order_cost_big_m", parsed=_lp(binaries=["Y_0"], constraints={"big_m_0": "Q_0 - 100 Y_0 <= 0", "balance_0": "I_0 - Q_0 = -5"}), consensus=0.4)
    good["structure_verification"] = {"structure_score": 1.0, "required_structures": required, "missing": [], "certificates": []}

    selected = select_for_method("ReplenishVerifier-TypeAware-Consensus", {"p0": [bad, good]}, {"p0": {"problem_type": "fixed_order_cost_big_m"}})[0]

    assert selected["candidate_id"] == "binary_k1"
