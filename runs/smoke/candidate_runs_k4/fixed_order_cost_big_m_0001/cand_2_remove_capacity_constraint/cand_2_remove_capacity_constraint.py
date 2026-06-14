import pulp


def build_model():
    model = pulp.LpProblem('remove_inventory_balance', pulp.LpMinimize)
    Q_0 = pulp.LpVariable('Q_0', lowBound=0)
    I_0 = pulp.LpVariable('I_0', lowBound=0)
    model += Q_0 + I_0, 'total_cost'
    model += Q_0 + I_0 >= 0, 'dummy_nonnegative_0'
    return model
