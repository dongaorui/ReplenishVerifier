import pulp

PROBLEM_TYPE = 'single_item_multi_period_shortage'
PARAMS = {'periods': 4, 'initial_inventory': 9, 'demand': [25, 34, 26, 44], 'unit_order_cost': 3, 'holding_cost': 4, 'shortage_cost': 18}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
