"""Problem-type-specific replenishment structure schema.

Required structures contribute to the main structure score. Optional structures are
reported in certificates but do not affect the main score.
"""

from replenishverifier.benchmark.schemas import STRUCTURE_KEYS


STRUCTURE_SCHEMA = {
    "single_period_newsvendor": {
        "required": [
            "order_variable",
            "inventory_variable",
            "shortage_variable",
            "holding_cost",
            "shortage_cost",
        ],
        "optional": ["inventory_balance"],
    },
    "single_item_multi_period": {
        "required": [
            "inventory_balance",
            "order_variable",
            "inventory_variable",
            "holding_cost",
        ],
        "optional": ["capacity_constraint", "lead_time"],
    },
    "single_item_multi_period_shortage": {
        "required": [
            "inventory_balance",
            "order_variable",
            "inventory_variable",
            "shortage_variable",
            "holding_cost",
            "shortage_cost",
        ],
        "optional": ["lead_time"],
    },
    "multi_item_capacity": {
        "required": [
            "inventory_balance",
            "order_variable",
            "inventory_variable",
            "capacity_constraint",
            "holding_cost",
        ],
        "optional": ["shortage_variable", "lead_time"],
    },
    "fixed_order_cost_big_m": {
        "required": [
            "inventory_balance",
            "order_variable",
            "inventory_variable",
            "binary_order_variable",
            "big_m_constraint",
            "holding_cost",
            "fixed_order_cost",
        ],
        "optional": ["capacity_constraint", "lead_time"],
    },
}


def schema_for_problem_type(problem_type):
    return STRUCTURE_SCHEMA.get(problem_type, {"required": [], "optional": []})


def expected_from_schema(problem_type):
    schema = schema_for_problem_type(problem_type)
    expected = {key: False for key in STRUCTURE_KEYS}
    for key in schema.get("required", []):
        expected[key] = True
    return expected


def split_expected_structures(expected, problem_type=None):
    """Return required/optional structure names for scoring and reporting.

    If a known problem_type is supplied, its schema is authoritative for required
    and optional structures. Otherwise, all truthy expected structures are treated
    as required for backward compatibility.
    """
    if problem_type in STRUCTURE_SCHEMA:
        schema = schema_for_problem_type(problem_type)
        required = [key for key in schema.get("required", []) if expected.get(key, True)]
        optional = list(schema.get("optional", []))
        return required, optional

    required = [key for key, value in (expected or {}).items() if value]
    optional = [key for key in STRUCTURE_KEYS if key not in required]
    return required, optional
