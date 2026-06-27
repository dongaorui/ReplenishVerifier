"""Legacy benchmark constants.

Structure schema definitions live in ``replenishverifier.data.structure_schema``.
This module remains as a compatibility import location for benchmark problem-type
metadata and the legacy ``STRUCTURE_KEYS`` symbol.
"""

from replenishverifier.data.structure_schema import STRUCTURE_KEYS


BASE_PROBLEM_TYPES = [
    "single_period_newsvendor",
    "single_item_multi_period",
    "single_item_multi_period_shortage",
    "multi_item_capacity",
    "fixed_order_cost_big_m",
]

EXTENDED_PROBLEM_TYPES = [
    "single_item_multi_period_lead_time",
    "single_item_multi_period_service_level",
    "single_item_multi_period_moq_batch",
]

PROBLEM_TYPES = BASE_PROBLEM_TYPES
ALL_PROBLEM_TYPES = BASE_PROBLEM_TYPES + EXTENDED_PROBLEM_TYPES

DIFFICULTY_BY_TYPE = {
    "single_period_newsvendor": "easy",
    "single_item_multi_period": "medium",
    "single_item_multi_period_shortage": "medium",
    "multi_item_capacity": "hard",
    "fixed_order_cost_big_m": "hard",
    "single_item_multi_period_lead_time": "hard",
    "single_item_multi_period_service_level": "hard",
    "single_item_multi_period_moq_batch": "hard",
}


def empty_structures():
    return {k: False for k in STRUCTURE_KEYS}
