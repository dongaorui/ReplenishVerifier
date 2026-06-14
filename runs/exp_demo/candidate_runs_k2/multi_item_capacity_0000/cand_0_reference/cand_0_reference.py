import pulp

PROBLEM_TYPE = 'multi_item_capacity'
PARAMS = {'items': 4, 'periods': 3, 'initial_inventory': [12, 3, 11, 11], 'demand': [[44, 36, 24], [38, 47, 27], [10, 20, 37], [31, 27, 19]], 'volume': [2, 3, 1, 1], 'storage_capacity': 157, 'unit_order_cost': [3, 1, 4, 5], 'holding_cost': [1, 4, 1, 3]}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
