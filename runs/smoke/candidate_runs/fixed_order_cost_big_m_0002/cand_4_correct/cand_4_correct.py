import pulp

PROBLEM_TYPE = 'fixed_order_cost_big_m'
PARAMS = {'periods': 5, 'initial_inventory': 10, 'demand': [25, 49, 48, 15, 53], 'unit_order_cost': 4, 'holding_cost': 1, 'fixed_order_cost': 27, 'big_m': 190}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
