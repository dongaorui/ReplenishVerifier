import pulp and os.

Then, create the problem. The function build_model() returns the LpProblem.

In the build_model function:

- Create the problem with a name, e.g., 'single_item_multi_period_0007'.

- Define the variables. For order, we can have a list of variables, each for each period. Similarly for inventory_after_demand.

But since the problem has 6 periods, we can loop through 0 to 5.

But in PuLP, variables can be created with LpVariable. So for order, perhaps:

orders = [pulp.LpVariable(f'order_{i}', lowBound=0, cat='Integer') for i in range(periods)]

Similarly for inventory_after_demand:

inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Integer') for i in range(periods)]

Wait, but the inventory_after_demand can be zero, but not negative. So the lower bound is 0.

But the problem says that the store starts with 4 units. So for the first period, the inventory after demand is 4 + order[0] - demand[0]. But since the inventory after demand can't be negative, that's why we have the constraint that inventory_after_demand[i] >= 0.

Now, the constraints:

For each period i in 0 to 5:

If i == 0:

inventory[i] + demand[i] = initial_inventory + order[i]

Else:

inventory[i] + demand[i] = inventory[i-1] + order[i]

So, for each i, we can create a constraint that:

inventory[i] + demand[i] == (initial_inventory if i == 0 else inventory[i-1]) + order[i]

But in PuLP, we can't directly write equations like that. So for each i, we need to add a constraint that:

inventory[i] + demand[i] == (initial_inventory if i == 0 else inventory[i-1]) + order[i]

But how to express that in code. Let's think:

for
