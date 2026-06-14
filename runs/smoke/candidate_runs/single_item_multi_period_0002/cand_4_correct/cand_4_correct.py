import pulp

PROBLEM_TYPE = 'single_item_multi_period'
PARAMS = {'periods': 5, 'initial_inventory': 4, 'demand': [28, 36, 21, 20, 39], 'unit_order_cost': 1, 'holding_cost': 3}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
