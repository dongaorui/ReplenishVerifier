import pulp and os.

Then, create the problem.

The function build_model() should return the LpProblem object.

Inside build_model(), we need to create the variables.

Let me think about the variables. For each period t in 0 to 4 (since T=5), we have order[t] and inventory[t].

But in PuLP, variables can be created as a list. So:

orders = [pulp.LpVariable(f"order_{t}", lowBound=0) for t in range(periods)]

inventories = [pulp.LpVariable(f"inventory_{t}", lowBound=0) for t in range(periods)]

But wait, the inventory for period 0 is initial_inventory + order[0] - demand[0]. So the first constraint is:

inventories[0] = initial_inventory + orders[0] - demand[0]

For t >=1, inventories[t] = inventories[t-1] + orders[t] - demand[t]

So for each t in 1 to T-1:
