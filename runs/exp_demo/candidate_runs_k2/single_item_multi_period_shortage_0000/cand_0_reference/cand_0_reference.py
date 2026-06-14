import pulp

PROBLEM_TYPE = 'single_item_multi_period_shortage'
PARAMS = {'periods': 3, 'initial_inventory': 0, 'demand': [25, 33, 34], 'unit_order_cost': 5, 'holding_cost': 1, 'shortage_cost': 16}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
