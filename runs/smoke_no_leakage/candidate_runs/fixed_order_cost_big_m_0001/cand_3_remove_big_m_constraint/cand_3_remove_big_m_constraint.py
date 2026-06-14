import pulp

PARAMS = {'periods': 3, 'initial_inventory': 16, 'demand': [55, 34, 55], 'unit_order_cost': 5, 'holding_cost': 2, 'fixed_order_cost': 29, 'big_m': 144}


def build_model():
    params = PARAMS
    T = params['periods']
    model = pulp.LpProblem('remove_big_m_constraint', pulp.LpMinimize)
    Q = pulp.LpVariable.dicts('Q', range(T), lowBound=0)
    I = pulp.LpVariable.dicts('I', range(T), lowBound=0)
    Y = pulp.LpVariable.dicts('Y', range(T), lowBound=0, upBound=1, cat='Binary')
    model += pulp.lpSum(params['unit_order_cost'] * Q[t] + params['holding_cost'] * I[t] + params['fixed_order_cost'] * Y[t] for t in range(T)), 'total_cost'
    for t in range(T):
        prev = params['initial_inventory'] if t == 0 else I[t - 1]
        model += I[t] == prev + Q[t] - params['demand'][t], f'inventory_balance_{t}'
    return model
