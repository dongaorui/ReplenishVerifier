import pulp

PARAMS = {'items': 4, 'periods': 3, 'initial_inventory': [20, 5, 13, 19], 'demand': [[45, 44, 26], [47, 37, 47], [35, 33, 24], [18, 42, 41]], 'volume': [1, 1, 1, 2], 'storage_capacity': 88, 'unit_order_cost': [4, 4, 5, 4], 'holding_cost': [3, 1, 1, 3]}


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
