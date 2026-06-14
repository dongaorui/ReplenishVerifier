import pulp

PROBLEM_TYPE = 'fixed_order_cost_big_m'
PARAMS = {'periods': 5, 'initial_inventory': 7, 'demand': [51, 27, 60, 19, 17], 'unit_order_cost': 3, 'holding_cost': 1, 'fixed_order_cost': 74, 'big_m': 174}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
