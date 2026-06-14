import pulp

PROBLEM_TYPE = 'multi_item_capacity'
PARAMS = {'items': 2, 'periods': 4, 'initial_inventory': [14, 12], 'demand': [[33, 32, 23, 27], [14, 48, 50, 20]], 'volume': [2, 2], 'storage_capacity': 114, 'unit_order_cost': [5, 2], 'holding_cost': [3, 1]}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
