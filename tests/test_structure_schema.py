from replenishverifier.data.structure_schema import expected_from_schema, split_expected_structures


def test_problem_type_schema_separates_required_and_optional():
    expected = expected_from_schema("fixed_order_cost_big_m")
    required, optional = split_expected_structures(expected, problem_type="fixed_order_cost_big_m")

    assert "big_m_constraint" in required
    assert "fixed_order_cost" in required
    assert "capacity_constraint" in optional
    assert expected["big_m_constraint"] is True
    assert expected["capacity_constraint"] is False
