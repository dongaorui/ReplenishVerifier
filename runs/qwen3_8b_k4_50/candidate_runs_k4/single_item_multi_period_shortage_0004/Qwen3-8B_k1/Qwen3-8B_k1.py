import pulp and os.

Then, define the build_model function. Inside, create the LpProblem.

Parameters: periods=3, initial_inventory=11, demand=[39,35,23], unit_order_cost=2, holding_cost=1, shortage_cost=9.

Variables:

For each period t (1-based?), create order, inventory, shortage variables.

In PuLP, variables can be created with LpVariable. Let's index them by period.

So, for t in 0 to periods-1 (assuming 0-based), but maybe easier to use 1-based.

But in code, perhaps using a list of variables for each period.

So:

periods = 3

for t in range(periods):

    order[t] = LpVariable(f'order_{t}', lowBound=0)

    inventory[t] = LpVariable(f'inventory_{t}', lowBound=0)

    shortage[t] = LpVariable(f'shortage_{t}', lowBound=0)

Wait, but for the first period, the previous inventory is initial_inventory. So for t=0 (assuming 0-based), the constraint is:

inventory[0] + shortage[0] = initial_inventory + order[0] - demand[0]

For t=1:

inventory[1] + shortage[1] = inventory[0] + order[1] - demand[1]

And for t=2:

inventory[2] + shortage[2] = inventory[1] + order[2] - demand[2]

So, in code, for each t in 0 to periods-1:

if t == 0:

    prev_inventory = initial_inventory

else:

    prev_inventory = inventory[t-1]

Then, the constraint is:

inventory[t] + shortage[t] == prev_inventory + order[t] - demand[t]

But in PuLP, the constraints are added as equations.

So, for each period, create a constraint.

Then, the objective function is sum over all periods of (unit_order_cost * order[t] + holding_cost * inventory[t] + shortage_cost * shortage[t])

Now, the code structure:

def build_model():

    periods = 3

    initial_inventory = 11

    demand = [39, 35, 23]

    unit_order_cost = 2

    holding_cost = 1

    shortage_cost = 9

    prob = pulp.LpProblem("InventoryReplenishment", pulp.LpMinimize)

    # Create variables

    order = [pulp.LpVariable(f'order_{t}', lowBound=0) for t in range(periods)]

    inventory = [pulp.LpVariable(f'inventory_{t}', lowBound=0) for t in range(periods)]

    shortage = [pulp.LpVariable(f'shortage_{t}', lowBound=0) for t in range(periods)]

    # Objective function

    prob += pulp.lpSum([unit_order_cost * order[t] + holding_cost * inventory[t] + shortage_cost * shortage[t] for t in range(periods)])

    # Constraints

    for t in range(periods):

        if t == 0:

            prev_inv = initial_inventory

        else:

            prev_inv = inventory[t-1]

        prob += inventory[t] + shortage[t] == prev_inv + order[t] - demand[t], f'Balance_{t}'

    return prob

Wait, but in the problem statement, the initial inventory is 11. So for the first period, the previous inventory is 11. Then, the equation is inventory[0] + shortage[0] = 11 + order[0] - demand[0]

Yes.

But wait, the initial inventory is the starting point. So for
