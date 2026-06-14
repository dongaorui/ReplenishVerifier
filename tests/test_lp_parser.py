from replenishverifier.verifier.lp_parser import parse_lp_text


def test_parse_simple_lp():
    text = """
Minimize
OBJ: 2 Q_0 + 3 I_0
Subject To
inventory_balance_0: I_0 - Q_0 = -5
Bounds
End
"""
    parsed = parse_lp_text(text)
    assert "inventory_balance_0" in parsed.constraint_names
    assert "Q_0" in parsed.variable_names
    assert "I_0" in parsed.variable_names
