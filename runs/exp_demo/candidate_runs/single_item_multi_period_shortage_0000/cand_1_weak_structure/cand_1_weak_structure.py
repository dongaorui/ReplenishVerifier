import pulp


def build_model():
    model = pulp.LpProblem('weak_candidate', pulp.LpMinimize)
    X_0 = pulp.LpVariable('X_0', lowBound=0)
    model += X_0, 'total_cost'
    model += X_0 >= 0, 'dummy_constraint_0'
    return model
