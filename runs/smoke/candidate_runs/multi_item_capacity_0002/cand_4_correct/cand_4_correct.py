import pulp

PROBLEM_TYPE = 'multi_item_capacity'
PARAMS = {'items': 4, 'periods': 3, 'initial_inventory': [20, 5, 13, 19], 'demand': [[45, 44, 26], [47, 37, 47], [35, 33, 24], [18, 42, 41]], 'volume': [1, 1, 1, 2], 'storage_capacity': 88, 'unit_order_cost': [4, 4, 5, 4], 'holding_cost': [3, 1, 1, 3]}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
