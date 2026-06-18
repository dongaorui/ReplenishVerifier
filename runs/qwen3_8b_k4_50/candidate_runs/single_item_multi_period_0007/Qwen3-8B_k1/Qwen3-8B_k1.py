import pulp

def build_model():
    periods = 6
    initial_inventory = 4
    demand = [31, 23, 30, 50, 49, 31]
    unit_order_cost = 5
    holding_cost = 4

    # Create the problem
    prob = pulp.LpProblem("Inventory_Replenishment", pulp.LpMinimize)

    # Decision variables
    x = [pulp.LpVariable(f"x_{t}", lowBound=0, cat='Integer') for t in range(periods)]
    inv = [pulp.LpVariable(f"inv_{t}", lowBound=0, cat='Integer') for t in range(periods)]

    # Objective function: sum(order cost) + sum(holding cost)
    prob += pulp.lpSum([unit_order_cost * x[t] for t in range(periods)]) + pulp.lpSum([holding_cost * inv[t] for t in range(periods)])

    # Constraints
    # For each period t (1-based?), but in code, the indices are 0-based. So for t in 0 to 5 (periods 1 to 6)
    # inv[t] = initial_inventory + x[0] - demand[0] for t=0 (period 1)
    # Wait, the initial inventory is 4. So for t=0 (first period), inv[0] = initial_inventory + x[0] - demand[0]
    # Then for t=1 (second period), inv[1] = inv[0] + x[1] - demand[1], etc.

    # So for each t in 0 to 5 (periods 1 to 6):
    # inv[t] = inv_prev + x[t] - demand[t]
    # where inv_prev is initial_inventory for t=0, and inv[t-1] for t>0.

    # So for t=0:
    prob += inv[0] == initial_inventory + x[0] - demand[0], "Inv_0_Constraint"

    # For t from 1 to 5:
    for t in range(1, periods):
        prob += inv[t] == inv[t-1] + x[t] - demand[t], f"Inv_{t}_Constraint"

    # Also, ensure that inv[t] >= 0. But since the variables are set to lowBound=0, that's already handled.

    # Wait, the variables inv are set to lowBound=0, so inv[t] >= 0 is automatically satisfied. So no need to add constraints for that.

    return prob

Wait, but in the code above, the variables inv are created with lowBound=0. So inv[t] can't be negative. So the constraints inv[t] = ... will automatically ensure that inv[t] is non-negative. But what if the equation results in a negative value? Because the variables
