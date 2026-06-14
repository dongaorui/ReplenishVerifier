import pulp

PROBLEM_TYPE = 'single_item_multi_period'
PARAMS = {'periods': 6, 'initial_inventory': 1, 'demand': [16, 20, 28, 29, 47, 53], 'unit_order_cost': 1, 'holding_cost': 2}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
