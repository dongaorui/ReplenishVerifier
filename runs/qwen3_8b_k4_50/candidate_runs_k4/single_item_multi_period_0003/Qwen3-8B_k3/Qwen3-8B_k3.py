import pulp and os.

Then, define the build_model function. Inside, create the problem.

The problem is a minimization problem. The objective is the sum of order costs and holding costs.

So, for each period, the order cost is unit_order_cost * order[t], and the holding cost is holding_cost * inventory[t]. Summing over all periods.

Now, the variables:

order = [pulp.LpVariable(f"order_{t}", lowBound=0) for t in range(periods)]

inventory = [pulp.LpVariable(f"inventory_{t}", lowBound=0) for t in range(periods)]

Wait, but the inventory after period t is the variable. So for t=0, inventory[0] = initial_inventory + order[0] - demand[0]. For t=1, inventory[1] = inventory[0] + order[1] - demand[1], etc.

So, the constraints are:

For t=0:

inventory[0] = initial_inventory + order[0] - demand[0]

For t >=1:

inventory[t] = inventory[t-1] + order[t] - demand[t]

But in PuLP, we can model these as equality constraints.

So, for each t in 0 to 5:

if t == 0:

prob += inventory[t] == initial_inventory + order[t] - demand[t]

else:

prob += inventory[t] == inventory[t-1] + order[t] - demand[t]

But in code, how to loop through the periods?

Also
