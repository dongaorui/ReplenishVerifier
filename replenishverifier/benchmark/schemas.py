STRUCTURE_KEYS = [
    "inventory_balance",
    "order_variable",
    "inventory_variable",
    "shortage_variable",
    "capacity_constraint",
    "binary_order_variable",
    "big_m_constraint",
    "lead_time",
    "holding_cost",
    "shortage_cost",
    "fixed_order_cost",
]

PROBLEM_TYPES = [
    "single_period_newsvendor",
    "single_item_multi_period",
    "single_item_multi_period_shortage",
    "multi_item_capacity",
    "fixed_order_cost_big_m",
]

DIFFICULTY_BY_TYPE = {
    "single_period_newsvendor": "easy",
    "single_item_multi_period": "medium",
    "single_item_multi_period_shortage": "medium",
    "multi_item_capacity": "hard",
    "fixed_order_cost_big_m": "hard",
}


def empty_structures():
    return {k: False for k in STRUCTURE_KEYS}
