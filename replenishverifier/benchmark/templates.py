import random
from copy import deepcopy

import pulp

from replenishverifier.data.structure_schema import expected_from_schema, get_structure_schema


def expected_for(problem_type):
    return expected_from_schema(problem_type)


def _structure_lists(problem_type):
    schema = get_structure_schema(problem_type)
    required = sorted(schema["required"])
    optional = sorted(schema["optional"])
    return required, optional, sorted(set(required) | set(optional))


def semantic_frame(problem_type, params):
    """Return a replenishment-specific semantic frame for one benchmark instance."""
    required, optional, structures = _structure_lists(problem_type)

    if problem_type == "single_period_newsvendor":
        frame = {
            "sets": {"selling_season": [0], "item": "single_sku"},
            "parameters": {
                "demand": params["demand"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
                "shortage_cost": params["shortage_cost"],
            },
            "decision_variables": {
                "order_quantity": "Q_0: units ordered before demand is realized",
                "ending_inventory": "I_0: leftover units after satisfying demand",
                "shortage_or_backlog": "B_0: unmet demand in the selling season",
            },
            "objective_terms": [
                "unit ordering cost for Q_0",
                "holding cost for leftover inventory I_0",
                "shortage penalty for unmet demand B_0",
            ],
            "constraints": [
                "single-period demand satisfaction: order quantity plus shortage minus ending inventory equals realized demand",
                "nonnegative order, inventory, and shortage variables",
            ],
            "solver_type": "linear_programming",
        }
    elif problem_type == "single_item_multi_period":
        periods = list(range(params["periods"]))
        frame = {
            "sets": {"periods": periods, "item": "single_sku"},
            "parameters": {
                "initial_inventory": params["initial_inventory"],
                "demand_by_period": params["demand"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
            },
            "decision_variables": {
                "order_quantity": "Q_t: replenishment quantity ordered in each period t",
                "inventory_level": "I_t: ending inventory carried from period t to t+1",
            },
            "objective_terms": [
                "period-by-period unit ordering cost for Q_t",
                "period-by-period holding cost for ending inventory I_t",
            ],
            "constraints": [
                "inventory balance in every period linking previous inventory, current order, demand, and ending inventory",
                "nonnegative order and inventory variables",
            ],
            "solver_type": "linear_programming",
        }
    elif problem_type == "single_item_multi_period_shortage":
        periods = list(range(params["periods"]))
        frame = {
            "sets": {"periods": periods, "item": "single_sku"},
            "parameters": {
                "initial_inventory": params["initial_inventory"],
                "demand_by_period": params["demand"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
                "shortage_cost": params["shortage_cost"],
            },
            "decision_variables": {
                "order_quantity": "Q_t: replenishment quantity ordered in each period t",
                "inventory_level": "I_t: positive ending stock after period t",
                "shortage_or_backlog": "B_t: backlogged unmet demand carried after period t",
            },
            "objective_terms": [
                "period-by-period unit ordering cost for Q_t",
                "holding cost for positive inventory I_t",
                "shortage/backorder penalty for B_t",
            ],
            "constraints": [
                "net-inventory balance in every period using I_t minus B_t",
                "backorder semantics linking previous inventory/backlog to current demand",
                "nonnegative order, inventory, and backlog variables",
            ],
            "solver_type": "linear_programming",
        }
    elif problem_type == "multi_item_capacity":
        periods = list(range(params["periods"]))
        items = list(range(params["items"]))
        frame = {
            "sets": {"items": items, "periods": periods},
            "parameters": {
                "initial_inventory_by_item": params["initial_inventory"],
                "demand_by_item_period": params["demand"],
                "item_volume": params["volume"],
                "storage_capacity": params["storage_capacity"],
                "unit_order_cost_by_item": params["unit_order_cost"],
                "holding_cost_by_item": params["holding_cost"],
            },
            "decision_variables": {
                "order_quantity": "Q_i_t: replenishment quantity for item i in period t",
                "inventory_level": "I_i_t: ending inventory of item i in period t",
            },
            "objective_terms": [
                "item-specific ordering cost for Q_i_t",
                "item-specific holding cost for I_i_t",
            ],
            "constraints": [
                "item-level inventory balance for every item and period",
                "shared warehouse capacity in every period using item volumes and ending inventory",
                "nonnegative item-period order and inventory variables",
            ],
            "solver_type": "linear_programming",
        }
    elif problem_type == "fixed_order_cost_big_m":
        periods = list(range(params["periods"]))
        frame = {
            "sets": {"periods": periods, "item": "single_sku"},
            "parameters": {
                "initial_inventory": params["initial_inventory"],
                "demand_by_period": params["demand"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
                "fixed_order_cost": params["fixed_order_cost"],
                "big_m": params["big_m"],
            },
            "decision_variables": {
                "order_quantity": "Q_t: replenishment quantity ordered in period t",
                "inventory_level": "I_t: ending inventory carried after period t",
                "order_trigger": "Y_t: binary variable indicating whether an order is placed in period t",
            },
            "objective_terms": [
                "unit ordering cost for Q_t",
                "holding cost for I_t",
                "fixed ordering/setup cost charged through binary trigger Y_t",
            ],
            "constraints": [
                "inventory balance in every period",
                "Big-M linking constraint Q_t <= M * Y_t tying order quantity to the binary trigger",
                "nonnegative order/inventory variables and binary order-trigger variables",
            ],
            "solver_type": "mixed_integer_linear_programming",
        }
    elif problem_type == "single_item_multi_period_lead_time":
        periods = list(range(params["periods"]))
        frame = {
            "sets": {"periods": periods, "item": "single_sku"},
            "parameters": {
                "initial_inventory": params["initial_inventory"],
                "demand_by_period": params["demand"],
                "lead_time": params["lead_time"],
                "scheduled_arrivals": params["scheduled_arrivals"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
            },
            "decision_variables": {
                "order_quantity": "Q_t: order placed in period t and received after L periods",
                "inventory_level": "I_t: ending inventory after delayed arrivals and demand",
            },
            "objective_terms": ["unit ordering cost for Q_t", "holding cost for delayed-ending inventory I_t"],
            "constraints": [
                "lead-time inventory balance I_t = I_{t-1} + arrivals_t - demand_t",
                "arrivals_t equals Q_{t-L} once t-L >= 0, otherwise scheduled_arrivals_t",
                "nonnegative order and inventory variables",
            ],
            "solver_type": "linear_programming",
        }
    elif problem_type == "single_item_multi_period_service_level":
        periods = list(range(params["periods"]))
        frame = {
            "sets": {"periods": periods, "item": "single_sku"},
            "parameters": {
                "initial_inventory": params["initial_inventory"],
                "demand_by_period": params["demand"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
                "service_level": params["service_level"],
            },
            "decision_variables": {
                "order_quantity": "Q_t: replenishment quantity ordered in each period",
                "inventory_level": "I_t: ending inventory after demand",
                "unmet_demand": "B_t: unmet demand used to enforce the service-level cap",
            },
            "objective_terms": ["unit ordering cost for Q_t", "holding cost for I_t"],
            "constraints": [
                "inventory/backlog balance with unmet demand variable B_t",
                "service-level or fill-rate constraint limiting total unmet demand",
                "nonnegative order, inventory, and unmet-demand variables",
            ],
            "solver_type": "linear_programming",
        }
    elif problem_type == "single_item_multi_period_moq_batch":
        periods = list(range(params["periods"]))
        frame = {
            "sets": {"periods": periods, "item": "single_sku"},
            "parameters": {
                "initial_inventory": params["initial_inventory"],
                "demand_by_period": params["demand"],
                "unit_order_cost": params["unit_order_cost"],
                "holding_cost": params["holding_cost"],
                "minimum_order_quantity": params["minimum_order_quantity"],
                "batch_size": params["batch_size"],
                "big_m": params["big_m"],
            },
            "decision_variables": {
                "order_quantity": "Q_t: replenishment quantity in each period",
                "inventory_level": "I_t: ending inventory after period t",
                "order_trigger": "Y_t: binary variable indicating whether an order is placed",
                "batch_multiplier": "Z_t: integer number of order batches",
            },
            "objective_terms": ["unit ordering cost for Q_t", "holding cost for I_t"],
            "constraints": [
                "inventory balance in every period",
                "MOQ is conditional: Q_t >= MOQ * Y_t and Q_t <= M * Y_t",
                "batch linking constraint Q_t = batch_size * Z_t with integer Z_t",
            ],
            "solver_type": "mixed_integer_linear_programming",
        }
    else:
        raise ValueError(f"Unknown problem_type: {problem_type}")

    frame["replenishment_structures"] = structures
    frame["required_structures"] = required
    frame["optional_structures"] = optional
    return frame


def replenishment_entities(problem_type, params):
    """Extract replenishment-domain entities from sampled parameters."""
    entities = {}
    if "demand" in params:
        entities["demand"] = params["demand"]
    if "initial_inventory" in params:
        entities["initial_inventory"] = params["initial_inventory"]
    if "periods" in params:
        entities["periods"] = list(range(params["periods"]))
    if "items" in params:
        entities["items"] = list(range(params["items"]))
    if "unit_order_cost" in params:
        entities["unit_order_cost"] = params["unit_order_cost"]
    if "holding_cost" in params:
        entities["holding_cost"] = params["holding_cost"]
    if "shortage_cost" in params:
        entities["shortage_cost"] = params["shortage_cost"]
    if "fixed_order_cost" in params:
        entities["fixed_order_cost"] = params["fixed_order_cost"]
    if "storage_capacity" in params:
        entities["storage_capacity"] = params["storage_capacity"]
    if "volume" in params:
        entities["item_volume"] = params["volume"]
        entities["volume"] = params["volume"]
    if "big_m" in params:
        entities["big_m"] = params["big_m"]
    if "lead_time" in params:
        entities["lead_time"] = params["lead_time"]
    if "scheduled_arrivals" in params:
        entities["scheduled_arrivals"] = params["scheduled_arrivals"]
    if "service_level" in params:
        entities["service_level"] = params["service_level"]
    if "minimum_order_quantity" in params:
        entities["minimum_order_quantity"] = params["minimum_order_quantity"]
    if "batch_size" in params:
        entities["batch_size"] = params["batch_size"]

    if problem_type in {
        "single_period_newsvendor",
        "single_item_multi_period",
        "single_item_multi_period_shortage",
        "multi_item_capacity",
        "fixed_order_cost_big_m",
        "single_item_multi_period_lead_time",
        "single_item_multi_period_service_level",
        "single_item_multi_period_moq_batch",
    }:
        entities["order_quantity"] = "Q"
        entities["inventory_level"] = "I"
    if problem_type in {"single_period_newsvendor", "single_item_multi_period_shortage", "single_item_multi_period_service_level"}:
        entities["shortage_or_backlog"] = "B"
    if problem_type == "single_item_multi_period_moq_batch":
        entities["order_trigger"] = "Y"
        entities["batch_multiplier"] = "Z"
    return entities


def modeling_steps(problem_type, params):
    """Deterministic LP-structure-grounded modeling steps for labeled data."""
    if problem_type == "single_period_newsvendor":
        return [
            "Define order quantity Q_0, ending inventory I_0, and shortage variable B_0.",
            "Add the single-period demand satisfaction constraint Q_0 + B_0 - I_0 = demand.",
            "Minimize unit ordering, holding, and shortage costs over Q_0, I_0, and B_0.",
            "Require all replenishment quantities, inventory, and shortage variables to be nonnegative.",
        ]
    if problem_type == "single_item_multi_period":
        return [
            "Define period-indexed order variables Q_t and inventory variables I_t.",
            "Establish inventory balance constraints for every period using initial or previous inventory, order quantity, and demand.",
            "Minimize total ordering cost and holding cost across all periods.",
            "Require order and inventory variables to be nonnegative.",
        ]
    if problem_type == "single_item_multi_period_shortage":
        return [
            "Define period-indexed order variables Q_t, inventory variables I_t, and shortage/backlog variables B_t.",
            "Establish net inventory balance constraints that carry both inventory and backlog across periods.",
            "Add shortage/backlog penalties to the objective together with ordering and holding costs.",
            "Require order, inventory, and backlog variables to be nonnegative.",
        ]
    if problem_type == "multi_item_capacity":
        return [
            "Define item-period order variables Q_i_t and inventory variables I_i_t.",
            "Establish inventory balance constraints for every item and period.",
            "Add a per-period warehouse capacity constraint using item volumes and ending inventories.",
            "Minimize item-specific ordering and holding costs subject to shared storage capacity.",
        ]
    if problem_type == "fixed_order_cost_big_m":
        return [
            "Define period-indexed order variables Q_t and inventory variables I_t.",
            "Define binary order trigger variables Y_t for whether an order is placed in each period.",
            "Establish inventory balance constraints for every period.",
            "Add Big-M linking constraints Q_t <= M * Y_t so positive orders activate the binary trigger.",
            "Minimize unit ordering, holding, and fixed ordering costs.",
        ]
    if problem_type == "single_item_multi_period_lead_time":
        return [
            "Define period-indexed order variables Q_t and inventory variables I_t.",
            "Use delayed arrivals in inventory balance: arrivals_t = Q_{t-L} when t-L >= 0 and scheduled arrivals otherwise.",
            "Minimize ordering and holding costs over the planning horizon.",
            "Require order and inventory variables to be nonnegative.",
        ]
    if problem_type == "single_item_multi_period_service_level":
        return [
            "Define Q_t, I_t, and unmet-demand variables B_t.",
            "Use inventory/backlog balance constraints to account for unmet demand.",
            "Add a service-level or fill-rate constraint limiting total unmet demand.",
            "Minimize ordering and holding costs while satisfying the service-level requirement.",
        ]
    if problem_type == "single_item_multi_period_moq_batch":
        return [
            "Define Q_t, I_t, binary order-trigger Y_t, and integer batch multiplier Z_t.",
            "Use inventory balance constraints in every period.",
            "Add conditional MOQ constraints Q_t >= MOQ * Y_t and Q_t <= M * Y_t so MOQ applies only when ordering.",
            "Add batch linking constraints Q_t = batch_size * Z_t with integer Z_t.",
            "Minimize ordering and holding costs.",
        ]
    raise ValueError(f"Unknown problem_type: {problem_type}")


def validate_replenishment_instance(row, include_labels=True):
    """Validate generated replenishment benchmark metadata with lightweight rules."""
    problem_type = row.get("problem_type")
    row_id = row.get("id", "<unknown>")
    prefix = f"Invalid replenishment instance id={row_id!r} problem_type={problem_type!r}"

    if not str(row.get("natural_language") or "").strip():
        raise ValueError(f"{prefix}: natural_language must be non-empty")
    try:
        required, _, _ = _structure_lists(problem_type)
    except Exception as exc:
        raise ValueError(f"{prefix}: unknown problem_type") from exc

    if not row.get("semantic_frame"):
        raise ValueError(f"{prefix}: semantic_frame is required")
    if not row.get("replenishment_entities"):
        raise ValueError(f"{prefix}: replenishment_entities is required")

    if include_labels:
        missing_labels = [
            key for key in ["expected_structures", "reference_code", "reference_objective", "reference_status"]
            if key not in row
        ]
        if missing_labels:
            raise ValueError(f"{prefix}: missing labeled fields {missing_labels}")
    else:
        leaked = [key for key in ["expected_structures", "reference_code", "reference_objective"] if key in row]
        if leaked:
            raise ValueError(f"{prefix}: unlabeled row contains label fields {leaked}")

    entities = row.get("replenishment_entities") or {}
    required_entities = {
        "single_period_newsvendor": ["demand", "unit_order_cost", "holding_cost", "shortage_cost"],
        "single_item_multi_period": ["periods", "initial_inventory", "demand", "unit_order_cost", "holding_cost"],
        "single_item_multi_period_shortage": ["periods", "initial_inventory", "demand", "unit_order_cost", "holding_cost", "shortage_cost"],
        "multi_item_capacity": ["items", "volume", "storage_capacity"],
        "fixed_order_cost_big_m": ["fixed_order_cost", "big_m"],
        "single_item_multi_period_lead_time": ["periods", "initial_inventory", "demand", "lead_time", "scheduled_arrivals"],
        "single_item_multi_period_service_level": ["periods", "initial_inventory", "demand", "service_level", "shortage_or_backlog"],
        "single_item_multi_period_moq_batch": ["periods", "initial_inventory", "demand", "minimum_order_quantity", "batch_size", "order_trigger", "batch_multiplier"],
    }[problem_type]
    missing_entities = [key for key in required_entities if key not in entities]
    if missing_entities:
        raise ValueError(f"{prefix}: missing replenishment entities {missing_entities}")

    frame_required = set((row.get("semantic_frame") or {}).get("required_structures") or [])
    missing_structures = sorted(set(required) - frame_required)
    if missing_structures:
        raise ValueError(f"{prefix}: semantic_frame missing required structures {missing_structures}")
    return True


def sample_params(problem_type, rng=None):
    rng = rng or random.Random()

    if problem_type == "single_period_newsvendor":
        return {
            "demand": rng.randint(30, 120),
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
            "shortage_cost": rng.randint(5, 15),
        }

    if problem_type == "single_item_multi_period":
        t_count = rng.randint(3, 6)
        return {
            "periods": t_count,
            "initial_inventory": rng.randint(0, 30),
            "demand": [rng.randint(15, 60) for _ in range(t_count)],
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
        }

    if problem_type == "single_item_multi_period_shortage":
        t_count = rng.randint(3, 6)
        return {
            "periods": t_count,
            "initial_inventory": rng.randint(0, 20),
            "demand": [rng.randint(20, 70) for _ in range(t_count)],
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
            "shortage_cost": rng.randint(8, 20),
        }

    if problem_type == "multi_item_capacity":
        t_count = rng.randint(3, 5)
        n_items = rng.randint(2, 4)
        demand = [[rng.randint(10, 50) for _ in range(t_count)] for _ in range(n_items)]
        volume = [rng.randint(1, 4) for _ in range(n_items)]
        initial_inventory = [rng.randint(0, 20) for _ in range(n_items)]
        return {
            "items": n_items,
            "periods": t_count,
            "initial_inventory": initial_inventory,
            "demand": demand,
            "volume": volume,
            "storage_capacity": rng.randint(80, 160),
            "unit_order_cost": [rng.randint(1, 5) for _ in range(n_items)],
            "holding_cost": [rng.randint(1, 4) for _ in range(n_items)],
        }

    if problem_type == "fixed_order_cost_big_m":
        t_count = rng.randint(3, 6)
        demand = [rng.randint(15, 60) for _ in range(t_count)]
        return {
            "periods": t_count,
            "initial_inventory": rng.randint(0, 20),
            "demand": demand,
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
            "fixed_order_cost": rng.randint(20, 80),
            "big_m": max(sum(demand), max(demand) * 2),
        }

    if problem_type == "single_item_multi_period_lead_time":
        t_count = rng.randint(4, 6)
        lead_time = rng.randint(1, 2)
        demand = [rng.randint(10, 45) for _ in range(t_count)]
        scheduled_arrivals = [rng.randint(0, 20) for _ in range(lead_time)]
        early_gap = max(0, sum(demand[:lead_time]) - sum(scheduled_arrivals))
        return {
            "periods": t_count,
            "initial_inventory": early_gap + rng.randint(5, 25),
            "demand": demand,
            "lead_time": lead_time,
            "scheduled_arrivals": scheduled_arrivals,
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
        }

    if problem_type == "single_item_multi_period_service_level":
        t_count = rng.randint(3, 6)
        demand = [rng.randint(15, 55) for _ in range(t_count)]
        service_level = rng.choice([0.85, 0.9, 0.95])
        return {
            "periods": t_count,
            "initial_inventory": rng.randint(0, 25),
            "demand": demand,
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
            "service_level": service_level,
            "max_unmet": int((1.0 - service_level) * sum(demand)),
        }

    if problem_type == "single_item_multi_period_moq_batch":
        t_count = rng.randint(3, 6)
        demand = [rng.randint(15, 55) for _ in range(t_count)]
        batch_size = rng.choice([5, 10, 12])
        moq = batch_size * rng.randint(1, 2)
        return {
            "periods": t_count,
            "initial_inventory": rng.randint(0, 25),
            "demand": demand,
            "unit_order_cost": rng.randint(1, 5),
            "holding_cost": rng.randint(1, 4),
            "minimum_order_quantity": moq,
            "batch_size": batch_size,
            "big_m": max(sum(demand) + moq, max(demand) * 3),
        }

    raise ValueError(f"Unknown problem_type: {problem_type}")


def _variant(style, text, template_id):
    return {"style": style, "text": text, "template_id": template_id}


def natural_language_variants(problem_type, params):
    if problem_type == "single_period_newsvendor":
        return [
            _variant("math", f"Single-period newsvendor: choose order Q, leftover inventory I, and shortage B for demand {params['demand']}. Minimize {params['unit_order_cost']}Q + {params['holding_cost']}I + {params['shortage_cost']}B subject to demand satisfaction.", "single_period_newsvendor_math"),
            _variant("business", f"A retailer is buying one product for a one-day selling season. Demand is {params['demand']}; each unit ordered costs {params['unit_order_cost']}, leftovers cost {params['holding_cost']}, and unmet demand costs {params['shortage_cost']}. Build a linear optimization model for the order decision.", "single_period_newsvendor_business"),
            _variant("verbose", f"Consider a single item with one ordering opportunity and uncertain demand represented by the realized demand value {params['demand']}. The formulation should account for the order quantity, any ending inventory, and any shortage. Ordering, holding, and shortage costs are {params['unit_order_cost']}, {params['holding_cost']}, and {params['shortage_cost']}, respectively. Formulate and solve the corresponding linear program.", "single_period_newsvendor_verbose"),
            _variant("table", f"Problem data:\n- Type: single-period newsvendor\n- Demand: {params['demand']}\n- Unit order cost: {params['unit_order_cost']}\n- Holding cost: {params['holding_cost']}\n- Shortage penalty: {params['shortage_cost']}\nTask: formulate a linear minimization model with order, inventory, and shortage variables.", "single_period_newsvendor_table"),
        ]

    if problem_type == "single_item_multi_period":
        return [
            _variant("math", f"Plan one-item replenishment over T={params['periods']} periods with initial inventory {params['initial_inventory']} and demands {params['demand']}. Minimize order cost {params['unit_order_cost']} and holding cost {params['holding_cost']} using inventory-balance constraints.", "single_item_multi_period_math"),
            _variant("business", f"A store replenishes a single SKU across {params['periods']} periods. It starts with {params['initial_inventory']} units and faces period demands {params['demand']}. Ordering costs {params['unit_order_cost']} per unit and holding costs {params['holding_cost']} per unit. Build the cost-minimizing replenishment LP.", "single_item_multi_period_business"),
            _variant("verbose", f"The planner must decide how much to order in each period for one item. Initial stock is {params['initial_inventory']}; demand by period is {params['demand']}. The model should carry inventory forward with standard balance equations and minimize the sum of ordering and inventory holding costs, with unit costs {params['unit_order_cost']} and {params['holding_cost']}.", "single_item_multi_period_verbose"),
            _variant("table", f"Problem data:\n- Type: single-item multi-period replenishment\n- Periods: {params['periods']}\n- Initial inventory: {params['initial_inventory']}\n- Demands: {params['demand']}\n- Unit order cost: {params['unit_order_cost']}\n- Holding cost: {params['holding_cost']}\nTask: formulate and solve a linear inventory-balance model.", "single_item_multi_period_table"),
        ]

    if problem_type == "single_item_multi_period_shortage":
        return [
            _variant("math", f"For T={params['periods']} periods, choose order Q_t, inventory I_t, and backlog B_t. Initial inventory is {params['initial_inventory']}, demand is {params['demand']}, and unit order/holding/shortage costs are {params['unit_order_cost']}/{params['holding_cost']}/{params['shortage_cost']}. Minimize total cost with net-inventory balance.", "single_item_multi_period_shortage_math"),
            _variant("business", f"A firm replenishes one product over {params['periods']} periods and allows backorders. Starting inventory is {params['initial_inventory']}; demands are {params['demand']}. Ordering costs {params['unit_order_cost']}, holding costs {params['holding_cost']}, and backlog penalties are {params['shortage_cost']}. Build a linear model.", "single_item_multi_period_shortage_business"),
            _variant("verbose", f"The replenishment plan may leave demand temporarily unmet, so the LP should include shortage or backlog variables as well as inventory and order variables. Use the initial inventory {params['initial_inventory']} and demand sequence {params['demand']}; minimize ordering, holding, and shortage costs with coefficients {params['unit_order_cost']}, {params['holding_cost']}, and {params['shortage_cost']}.", "single_item_multi_period_shortage_verbose"),
            _variant("table", f"Problem data:\n- Type: multi-period replenishment with shortages\n- Periods: {params['periods']}\n- Initial inventory: {params['initial_inventory']}\n- Demands: {params['demand']}\n- Unit order cost: {params['unit_order_cost']}\n- Holding cost: {params['holding_cost']}\n- Shortage penalty: {params['shortage_cost']}\nTask: formulate a linear backorder model.", "single_item_multi_period_shortage_table"),
        ]

    if problem_type == "multi_item_capacity":
        return [
            _variant("math", f"Plan replenishment for {params['items']} items and {params['periods']} periods. Initial inventories are {params['initial_inventory']}, demands are {params['demand']}, item volumes are {params['volume']}, and storage capacity is {params['storage_capacity']} per period. Minimize order and holding costs subject to inventory balance and capacity.", "multi_item_capacity_math"),
            _variant("business", f"A warehouse manages {params['items']} products over {params['periods']} periods with limited storage. It begins with inventories {params['initial_inventory']} and demand matrix {params['demand']}. Item volumes are {params['volume']} and capacity is {params['storage_capacity']}. Build the replenishment LP minimizing order and holding costs.", "multi_item_capacity_business"),
            _variant("verbose", f"The planner must coordinate multiple items that share a finite warehouse capacity in every period. For each item and period, use the demand data {params['demand']} and starting inventories {params['initial_inventory']}. The model should include item-level inventory balances and aggregate volume limits using volumes {params['volume']} and capacity {params['storage_capacity']}, with order costs {params['unit_order_cost']} and holding costs {params['holding_cost']}.", "multi_item_capacity_verbose"),
            _variant("table", f"Problem data:\n- Type: multi-item capacity-constrained replenishment\n- Items: {params['items']}\n- Periods: {params['periods']}\n- Initial inventories: {params['initial_inventory']}\n- Demand matrix: {params['demand']}\n- Volumes: {params['volume']}\n- Capacity: {params['storage_capacity']}\n- Unit order costs: {params['unit_order_cost']}\n- Holding costs: {params['holding_cost']}\nTask: formulate and solve the LP.", "multi_item_capacity_table"),
        ]

    if problem_type == "fixed_order_cost_big_m":
        return [
            _variant("math", f"Plan T={params['periods']} periods with fixed ordering costs. Initial inventory is {params['initial_inventory']} and demands are {params['demand']}. Use order Q_t, inventory I_t, binary order trigger Y_t, and Big-M links with M={params['big_m']}; minimize unit order cost {params['unit_order_cost']}, holding cost {params['holding_cost']}, and fixed cost {params['fixed_order_cost']}.", "fixed_order_cost_big_m_math"),
            _variant("business", f"A firm pays a setup cost whenever it places an order during a {params['periods']}-period horizon. It starts with {params['initial_inventory']} units and faces demands {params['demand']}. Unit ordering, holding, and fixed order costs are {params['unit_order_cost']}, {params['holding_cost']}, and {params['fixed_order_cost']}. Build a Big-M mixed-integer replenishment model with M={params['big_m']}.", "fixed_order_cost_big_m_business"),
            _variant("verbose", f"In this replenishment problem, ordering in a period incurs both a variable unit cost and a fixed activation cost. The formulation should include binary variables that indicate whether an order is placed and constraints linking order quantities to those binaries. Use initial inventory {params['initial_inventory']}, demands {params['demand']}, unit cost {params['unit_order_cost']}, holding cost {params['holding_cost']}, fixed cost {params['fixed_order_cost']}, and Big-M value {params['big_m']}.", "fixed_order_cost_big_m_verbose"),
            _variant("table", f"Problem data:\n- Type: fixed-order-cost replenishment\n- Periods: {params['periods']}\n- Initial inventory: {params['initial_inventory']}\n- Demands: {params['demand']}\n- Unit order cost: {params['unit_order_cost']}\n- Holding cost: {params['holding_cost']}\n- Fixed order cost: {params['fixed_order_cost']}\n- Big-M: {params['big_m']}\nTask: formulate a mixed-integer linear model with binary order triggers.", "fixed_order_cost_big_m_table"),
        ]

    if problem_type == "single_item_multi_period_lead_time":
        return [
            _variant("math", f"Plan T={params['periods']} periods with lead time L={params['lead_time']}. Orders Q_t arrive after L periods; early arrivals are {params['scheduled_arrivals']}. Initial inventory is {params['initial_inventory']} and demand is {params['demand']}. Minimize order cost {params['unit_order_cost']} and holding cost {params['holding_cost']}.", "single_item_multi_period_lead_time_math"),
            _variant("business", f"A supplier delivers replenishment orders after a {params['lead_time']}-period lead time. The firm starts with {params['initial_inventory']} units, has scheduled arrivals {params['scheduled_arrivals']}, and faces demands {params['demand']}. Build the delayed-arrival inventory LP.", "single_item_multi_period_lead_time_business"),
            _variant("verbose", f"The inventory balance must use arrivals from orders placed {params['lead_time']} periods earlier, not the current-period order. Use demands {params['demand']} and scheduled arrivals {params['scheduled_arrivals']} while minimizing ordering and holding costs.", "single_item_multi_period_lead_time_verbose"),
            _variant("table", f"Problem data:\n- Type: lead-time replenishment\n- Periods: {params['periods']}\n- Lead time: {params['lead_time']}\n- Scheduled arrivals: {params['scheduled_arrivals']}\n- Initial inventory: {params['initial_inventory']}\n- Demands: {params['demand']}\nTask: formulate a lead-time inventory-balance LP.", "single_item_multi_period_lead_time_table"),
        ]

    if problem_type == "single_item_multi_period_service_level":
        return [
            _variant("math", f"Plan T={params['periods']} periods with a fill-rate/service-level requirement {params['service_level']}. Demand is {params['demand']} and initial inventory is {params['initial_inventory']}. Use unmet-demand variables and limit total unmet demand to {params['max_unmet']}.", "single_item_multi_period_service_level_math"),
            _variant("business", f"A store must maintain a service level of {params['service_level']} over {params['periods']} periods. It starts with {params['initial_inventory']} units and faces demands {params['demand']}. Build a replenishment LP with explicit service-level constraints.", "single_item_multi_period_service_level_business"),
            _variant("verbose", f"The model may track unmet demand, but simply adding a shortage penalty is not enough: it must enforce a service-level or fill-rate constraint. Use max unmet demand {params['max_unmet']} and minimize ordering/holding costs.", "single_item_multi_period_service_level_verbose"),
            _variant("table", f"Problem data:\n- Type: service-level replenishment\n- Periods: {params['periods']}\n- Service level: {params['service_level']}\n- Max unmet demand: {params['max_unmet']}\n- Demands: {params['demand']}\nTask: formulate a service-constrained LP.", "single_item_multi_period_service_level_table"),
        ]

    if problem_type == "single_item_multi_period_moq_batch":
        return [
            _variant("math", f"Plan T={params['periods']} periods with MOQ {params['minimum_order_quantity']} and batch size {params['batch_size']}. Use binary order trigger Y_t and integer batch multiplier Z_t; Q_t must be a batch multiple and MOQ applies only if Y_t=1.", "single_item_multi_period_moq_batch_math"),
            _variant("business", f"A supplier accepts orders only in batches of {params['batch_size']} units, with minimum order quantity {params['minimum_order_quantity']} whenever an order is placed. Build a mixed-integer replenishment model for demands {params['demand']}.", "single_item_multi_period_moq_batch_business"),
            _variant("verbose", f"Do not force every period to order. Instead, introduce an order trigger and condition the MOQ on the trigger, with Q_t = batch_size * Z_t and integer Z_t. Use Big-M {params['big_m']} to link Q_t and Y_t.", "single_item_multi_period_moq_batch_verbose"),
            _variant("table", f"Problem data:\n- Type: MOQ/batch replenishment\n- Periods: {params['periods']}\n- MOQ: {params['minimum_order_quantity']}\n- Batch size: {params['batch_size']}\n- Big-M: {params['big_m']}\n- Demands: {params['demand']}\nTask: formulate a mixed-integer batch-ordering replenishment model.", "single_item_multi_period_moq_batch_table"),
        ]

    raise ValueError(f"Unknown problem_type: {problem_type}")


def choose_natural_language_variant(problem_type, params, rng=None, style=None):
    variants = natural_language_variants(problem_type, params)
    if style is not None:
        for variant in variants:
            if variant["style"] == style or variant["template_id"] == style:
                return variant
        raise ValueError(f"Unknown language style/template for {problem_type}: {style}")
    if rng is None:
        return variants[0]
    return rng.choice(variants)


def natural_language(problem_type, params, rng=None, style=None):
    return choose_natural_language_variant(problem_type, params, rng=rng, style=style)["text"]


def build_model(problem_type, params):
    if problem_type == "single_period_newsvendor":
        model = pulp.LpProblem("single_period_newsvendor", pulp.LpMinimize)
        q = pulp.LpVariable("Q_0", lowBound=0)
        inv = pulp.LpVariable("I_0", lowBound=0)
        back = pulp.LpVariable("B_0", lowBound=0)
        model += params["unit_order_cost"] * q + params["holding_cost"] * inv + params["shortage_cost"] * back, "total_cost"
        model += q + back - inv == params["demand"], "demand_satisfaction_0"
        return model

    if problem_type == "single_item_multi_period":
        t_count = params["periods"]
        model = pulp.LpProblem("single_item_multi_period", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", range(t_count), lowBound=0)
        inv = pulp.LpVariable.dicts("I", range(t_count), lowBound=0)
        model += pulp.lpSum(params["unit_order_cost"] * q[t] + params["holding_cost"] * inv[t] for t in range(t_count)), "total_cost"
        for t in range(t_count):
            prev = params["initial_inventory"] if t == 0 else inv[t - 1]
            model += inv[t] == prev + q[t] - params["demand"][t], f"inventory_balance_{t}"
        return model

    if problem_type == "single_item_multi_period_shortage":
        t_count = params["periods"]
        model = pulp.LpProblem("single_item_multi_period_shortage", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", range(t_count), lowBound=0)
        inv = pulp.LpVariable.dicts("I", range(t_count), lowBound=0)
        back = pulp.LpVariable.dicts("B", range(t_count), lowBound=0)
        model += pulp.lpSum(
            params["unit_order_cost"] * q[t] + params["holding_cost"] * inv[t] + params["shortage_cost"] * back[t]
            for t in range(t_count)
        ), "total_cost"
        for t in range(t_count):
            prev_net = params["initial_inventory"] if t == 0 else inv[t - 1] - back[t - 1]
            model += inv[t] - back[t] == prev_net + q[t] - params["demand"][t], f"inventory_balance_{t}"
        return model

    if problem_type == "multi_item_capacity":
        n_items, t_count = params["items"], params["periods"]
        model = pulp.LpProblem("multi_item_capacity", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", ((i, t) for i in range(n_items) for t in range(t_count)), lowBound=0)
        inv = pulp.LpVariable.dicts("I", ((i, t) for i in range(n_items) for t in range(t_count)), lowBound=0)
        model += pulp.lpSum(
            params["unit_order_cost"][i] * q[(i, t)] + params["holding_cost"][i] * inv[(i, t)]
            for i in range(n_items) for t in range(t_count)
        ), "total_cost"
        for i in range(n_items):
            for t in range(t_count):
                prev = params["initial_inventory"][i] if t == 0 else inv[(i, t - 1)]
                model += inv[(i, t)] == prev + q[(i, t)] - params["demand"][i][t], f"inventory_balance_{i}_{t}"
        for t in range(t_count):
            model += pulp.lpSum(params["volume"][i] * inv[(i, t)] for i in range(n_items)) <= params["storage_capacity"], f"capacity_{t}"
        return model

    if problem_type == "fixed_order_cost_big_m":
        t_count = params["periods"]
        model = pulp.LpProblem("fixed_order_cost_big_m", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", range(t_count), lowBound=0)
        inv = pulp.LpVariable.dicts("I", range(t_count), lowBound=0)
        y = pulp.LpVariable.dicts("Y", range(t_count), lowBound=0, upBound=1, cat="Binary")
        model += pulp.lpSum(
            params["unit_order_cost"] * q[t] + params["holding_cost"] * inv[t] + params["fixed_order_cost"] * y[t]
            for t in range(t_count)
        ), "total_cost"
        for t in range(t_count):
            prev = params["initial_inventory"] if t == 0 else inv[t - 1]
            model += inv[t] == prev + q[t] - params["demand"][t], f"inventory_balance_{t}"
            model += q[t] <= params["big_m"] * y[t], f"big_m_{t}"
        return model

    if problem_type == "single_item_multi_period_lead_time":
        t_count = params["periods"]
        lead_time = params["lead_time"]
        scheduled = list(params.get("scheduled_arrivals") or [])
        model = pulp.LpProblem("single_item_multi_period_lead_time", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", range(t_count), lowBound=0)
        inv = pulp.LpVariable.dicts("I", range(t_count), lowBound=0)
        model += pulp.lpSum(params["unit_order_cost"] * q[t] + params["holding_cost"] * inv[t] for t in range(t_count)), "total_cost"
        for t in range(t_count):
            prev = params["initial_inventory"] if t == 0 else inv[t - 1]
            arrival = q[t - lead_time] if t - lead_time >= 0 else (scheduled[t] if t < len(scheduled) else 0)
            model += inv[t] == prev + arrival - params["demand"][t], f"lead_time_inventory_balance_{t}"
        return model

    if problem_type == "single_item_multi_period_service_level":
        t_count = params["periods"]
        model = pulp.LpProblem("single_item_multi_period_service_level", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", range(t_count), lowBound=0)
        inv = pulp.LpVariable.dicts("I", range(t_count), lowBound=0)
        back = pulp.LpVariable.dicts("B", range(t_count), lowBound=0)
        model += pulp.lpSum(params["unit_order_cost"] * q[t] + params["holding_cost"] * inv[t] for t in range(t_count)), "total_cost"
        for t in range(t_count):
            prev_net = params["initial_inventory"] if t == 0 else inv[t - 1] - back[t - 1]
            model += inv[t] - back[t] == prev_net + q[t] - params["demand"][t], f"inventory_balance_{t}"
        model += pulp.lpSum(back[t] for t in range(t_count)) <= params["max_unmet"], "service_level_unmet_limit"
        return model

    if problem_type == "single_item_multi_period_moq_batch":
        t_count = params["periods"]
        model = pulp.LpProblem("single_item_multi_period_moq_batch", pulp.LpMinimize)
        q = pulp.LpVariable.dicts("Q", range(t_count), lowBound=0)
        inv = pulp.LpVariable.dicts("I", range(t_count), lowBound=0)
        y = pulp.LpVariable.dicts("Y", range(t_count), lowBound=0, upBound=1, cat="Binary")
        z = pulp.LpVariable.dicts("Z", range(t_count), lowBound=0, cat="Integer")
        model += pulp.lpSum(params["unit_order_cost"] * q[t] + params["holding_cost"] * inv[t] for t in range(t_count)), "total_cost"
        for t in range(t_count):
            prev = params["initial_inventory"] if t == 0 else inv[t - 1]
            model += inv[t] == prev + q[t] - params["demand"][t], f"inventory_balance_{t}"
            model += q[t] >= params["minimum_order_quantity"] * y[t], f"moq_conditional_{t}"
            model += q[t] <= params["big_m"] * y[t], f"big_m_order_trigger_{t}"
            model += q[t] == params["batch_size"] * z[t], f"batch_linking_{t}"
        return model

    raise ValueError(f"Unknown problem_type: {problem_type}")


def reference_code(problem_type, params):
    params_repr = repr(deepcopy(params))
    return f'''
import pulp

PROBLEM_TYPE = {problem_type!r}
PARAMS = {params_repr}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
'''.strip() + "\n"
