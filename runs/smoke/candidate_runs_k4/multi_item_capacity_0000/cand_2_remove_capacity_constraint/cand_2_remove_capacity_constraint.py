import pulp

PARAMS = {'items': 2, 'periods': 4, 'initial_inventory': [14, 12], 'demand': [[33, 32, 23, 27], [14, 48, 50, 20]], 'volume': [2, 2], 'storage_capacity': 114, 'unit_order_cost': [5, 2], 'holding_cost': [3, 1]}


def build_model():
    params = PARAMS
    N, T = params['items'], params['periods']
    model = pulp.LpProblem('remove_capacity_constraint', pulp.LpMinimize)
    Q = pulp.LpVariable.dicts('Q', ((i, t) for i in range(N) for t in range(T)), lowBound=0)
    I = pulp.LpVariable.dicts('I', ((i, t) for i in range(N) for t in range(T)), lowBound=0)
    model += pulp.lpSum(params['unit_order_cost'][i] * Q[(i, t)] + params['holding_cost'][i] * I[(i, t)] for i in range(N) for t in range(T)), 'total_cost'
    for i in range(N):
        for t in range(T):
            prev = params['initial_inventory'][i] if t == 0 else I[(i, t - 1)]
            model += I[(i, t)] == prev + Q[(i, t)] - params['demand'][i][t], f'inventory_balance_{i}_{t}'
    return model
