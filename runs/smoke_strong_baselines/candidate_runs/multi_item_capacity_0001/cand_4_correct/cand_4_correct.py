import pulp

PROBLEM_TYPE = 'multi_item_capacity'
PARAMS = {'items': 2, 'periods': 3, 'initial_inventory': [20, 15], 'demand': [[30, 35, 27], [14, 23, 46]], 'volume': [3, 2], 'storage_capacity': 130, 'unit_order_cost': [4, 2], 'holding_cost': [3, 2]}


def build_model():
    from replenishverifier.benchmark.templates import build_model as _build_model
    return _build_model(PROBLEM_TYPE, PARAMS)


if __name__ == "__main__":
    model = build_model()
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    print(pulp.LpStatus[model.status])
    print(pulp.value(model.objective))
