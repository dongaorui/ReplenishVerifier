import pulp and os.

Then, define the periods, initial inventory, demand, etc.

Then, create the problem.

Now, the function build_model() should return the LpProblem object.

Inside build_model(), we need to:

- Create the problem.

- Define variables: order[t] for t in 0 to periods-1, and inventory[t] for t in 0 to periods-1.

Wait, but the periods are 5, so t ranges from 0 to 4.

So, for each period t in 0 to 4:

order[t] is the order quantity in period t.

inventory[t] is the inventory at the end of period t.

So, the initial inventory is 26. For t=0, inventory[0] = initial_inventory + order[0] - demand[0].

For t >=1, inventory[t] = inventory[t-1] + order[t] - demand[t].

So, the constraints are:

For t=0:

inventory[0] = initial_inventory + order[0] - demand[0]

For t >=1:

inventory[t] = inventory[t-1] + order[t] - demand[t]

Additionally, inventory[t] >= 0 for all t.

So, in PuLP, we can model these as constraints.

So, in code:

prob = pulp.LpProblem("Inventory_Replenishment", pulp.LpMinimize)

Then, create variables:

orders = [pulp.LpVariable(f"order_{t}", lowBound=0, cat='Integer') for t in range(periods)]

inventories = [pulp.LpVariable(f"inventory_{t}", lowBound=0, cat='Integer') for t in range(periods)]

Wait, but the inventory can be zero or positive. So, the variables for inventory are non-negative.

But the order variables are also non-negative, since you can't order negative units.

So, the variables are all non-negative.

Then, the objective function is sum over
