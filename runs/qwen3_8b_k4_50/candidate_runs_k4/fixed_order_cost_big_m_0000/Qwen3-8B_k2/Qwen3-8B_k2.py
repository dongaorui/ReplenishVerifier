import pulp and os.

Then, define the parameters as given.

Then, create the problem.

The function build_model() will create the LpProblem.

Variables:

For each period, create O_i, Q_i, I_i.

But in PuLP, variables can be created with loops.

Let me think about the code structure.

First, the parameters:

periods = 5

initial_inventory = 7

demand = [29, 27, 24, 16, 17]

unit_order_cost = 4

holding_cost = 1

fixed_order_cost = 49

big_m = 113

Then, create the problem.

prob = pulp.LpProblem("Inventory_Replenishment", pulp.LpMinimize)
