from replenishverifier.verifier.lp_parser import parse_lp_text
from replenishverifier.verifier.structure_rules import check_structures


def test_structure_detection():
    text = """
Minimize
OBJ: 2 Q_0 + 3 I_0 + 10 Y_0
Subject To
inventory_balance_0: I_0 - Q_0 = -5
big_m_0: Q_0 - 100 Y_0 <= 0
Binaries
Y_0
End
"""
    parsed = parse_lp_text(text)
    expected = {
        "inventory_balance": True,
        "order_variable": True,
        "inventory_variable": True,
        "shortage_variable": False,
        "capacity_constraint": False,
        "binary_order_variable": True,
        "big_m_constraint": True,
        "lead_time": False,
        "holding_cost": True,
        "shortage_cost": False,
        "fixed_order_cost": True,
    }
    result = check_structures(parsed, expected)
    assert result.structure_score == 1.0
    assert not result.missing
    assert result.certificates
    cert = {item["rule_name"]: item for item in result.certificates}
    assert cert["inventory_balance"]["evidence"]
    assert cert["big_m_constraint"]["passed"] is True
    assert cert["big_m_constraint"]["evidence"]
    assert cert["fixed_order_cost"]["evidence"]
    assert result.weak_evidence["big_m_like_constraints"]["found"] is True
    assert result.weak_evidence["fixed_cost_binary_terms"]["found"] is True


def test_structure_detection_with_descriptive_variable_names():
    text = """
Minimize
OBJ: 2 order_qty_0 + 3 ending_inventory_0 + 10 setup_0
Subject To
stock_flow_0: ending_inventory_0 - order_qty_0 = -5
setup_link_0: order_qty_0 - 100 setup_0 <= 0
Binaries
setup_0
End
"""
    parsed = parse_lp_text(text)
    expected = {
        "inventory_balance": True,
        "order_variable": True,
        "inventory_variable": True,
        "shortage_variable": False,
        "capacity_constraint": False,
        "binary_order_variable": True,
        "big_m_constraint": True,
        "lead_time": False,
        "holding_cost": True,
        "shortage_cost": False,
        "fixed_order_cost": True,
    }
    result = check_structures(parsed, expected)
    assert result.structure_score == 1.0
    assert not result.missing
    cert = {item["rule_name"]: item for item in result.certificates}
    assert cert["order_variable"]["passed"] is True
    assert cert["fixed_order_cost"]["evidence"]
    assert result.weak_evidence["inventory_recurrence_candidates"]["found"] is True
