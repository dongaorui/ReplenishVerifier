import pulp and os.

Then, define the build_model function. Inside, create the problem.

The problem will have variables for order and inventory. Let's think about the indices. For periods, 0 to periods-1 (since periods is 5, 0-4). For items, 0-3.

So, for each item i in 0..3 and period t in 0..4:

order[t][i] = quantity ordered in period t for item i.

inventory[t][i] = inventory level at the end of period t for item i.

But for the first period (t=0), inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]. Wait, no. Wait, the initial inventory is the starting inventory before period 1. So, for period 1 (t=0?), maybe the indexing is a bit confusing. Let me check the problem statement.

The problem says "for each item and period", and the demand is given as a list of lists. The initial inventories are given as [1, 18, 17, 1]. So, for period 1 (assuming periods are 1-based?), but in the code, perhaps the periods are 0-based. Let me think: the problem has 5 periods, so t ranges from 0 to 4 (assuming 0-based). The initial inventory is the inventory at the start of period 0. Then, for each period t, the inventory after ordering and meeting demand is inventory[t][i].

So, for each item i and period t:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But for t=0, inventory[-1][i] is not defined. So, for t=0, inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]. Wait, no. Wait, the initial inventory is the starting inventory before any orders in period 0. So, the initial inventory is the inventory at the start of period 0. Then, during period 0, you order order[0][i], which is added to the initial inventory, then subtract demand[0][i], resulting in inventory[0][i]. Then, for period 1, the inventory starts with inventory[0][i], and so on.

So, the equation for inventory[t][i] is:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But for t=0, inventory[-1][i] is not defined. So, the initial inventory is the starting point. Therefore, for t=0, inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]. Wait, no. Wait, the initial inventory is the inventory before any orders in period 0. So, during period 0, you order order[0][i], which is added to the initial inventory, then subtract demand[0][i], resulting in inventory[0][i]. So, the equation for t=0 is:

inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]

But for t >=1, inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

So, the constraints for inventory balance are:

For each item i and period t:

if t == 0:
   inventory[t][i] = initial_inventory[i] + order[t][i] - demand[t][i]
else:
   inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But in PuLP, we can model this with constraints. So, for each t and i, we can create a constraint that inventory[t][i] - inventory[t-1][i] - order[t][i] + demand[t][i] = 0, but for t=0, the inventory[t-1][i] is initial_inventory[i]. Wait, no. For t=0, the equation is inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]. So, rearranged: inventory[0][i] - order[0][i] + demand[0][i] = initial_inventory[i]. So, for t=0, the constraint is inventory[0][i] - order[0][i] + demand[0][i] = initial_inventory[i]. For t >=1, the constraint is inventory[t][i] - inventory[t-1][i] - order[t][i] + demand[t][i] = 0.

So, in code, for each item i and period t:

if t == 0:
   prob += inventory[t][i] - order[t][i] + demand[t][i] == initial_inventory[i]
else:
   prob += inventory[t][i] - inventory[t-1][i] - order[t][i] + demand[t][i] == 0

But in PuLP, we can loop through each t and i, and create these constraints.

Another thing: the inventory levels must be non-negative. So, for each t and i, inventory[t][i] >= 0.

Then, the aggregate volume constraint: for each period t, sum over all items (inventory[t][i] * volume[i]) <= storage_capacity.

So, the steps for the code:

1. Import pulp and os.

2. Define the build_model function.

3. In build_model, create the problem.

4. Define the variables: order and inventory.
