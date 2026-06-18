<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has 2 items and 3 periods. Each period has specific demands for each item. The initial inventory is given, and there's a storage capacity limit per period. The goal is to minimize order and holding costs while respecting inventory balance and capacity constraints.

First, I need to define the decision variables. The main variables here are the order quantities for each item in each period. Also, the inventory levels after each period must be tracked. Let me think about how to model that.

For each item and period, I'll have an order variable. Let's say orders[i][t] represents the quantity ordered for item i in period t. Then, the inventory after each period is calculated based on the previous inventory, minus demand, plus the order. But I also need to track the inventory levels to ensure they don't exceed the storage capacity.

Wait, the storage capacity is per period. So, for each period, the total inventory (after adding the order and subtracting demand) must be ≤ storage_capacity. Also, the inventory can't be negative, but since the problem doesn't mention that, maybe it's allowed? Wait, the problem says "inventory balance" which implies that inventory can't be negative. So I need to ensure that the inventory after each period is non-negative.

Wait, the problem says "inventory balance and capacity". So the constraints are:

For each period t and item i:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

And inventory[t][i] must be ≥ 0 (since you can't have negative inventory), and also inventory[t][i] ≤ storage_capacity.

But wait, the storage capacity is per period. So for each period, the total inventory for all items must be ≤ storage_capacity? Or per item? The problem says "storage capacity is 89 per period". Hmm, the wording is a bit ambiguous. But looking at the parameters, the storage_capacity is a single value. So perhaps the total inventory across all items in each period can't exceed 89. Or maybe per item? Wait, the problem says "storage capacity is 89 per period". So maybe for each period, the total inventory for all items combined must be ≤ 89. Or maybe per item? Let me check the problem statement again.

The problem says "storage capacity is 89 per period". So maybe for each period, the total inventory for all items must not exceed 89. But that's not clear. Wait, the problem says "storage capacity is 89 per period". So perhaps for each period, the sum of inventories for all items in that period must be ≤ 89. Or maybe each item has its own storage capacity? But the parameter is a single value. Hmm. Let me check the parameters again.

The parameters have "storage_capacity": 89. So it's a single value. So the problem is that for each period, the total inventory across all items must not exceed 89. Or maybe per item? But that's not clear. Wait, the problem says "storage capacity is 89 per period". So maybe for each period, the total inventory for all items in that period can't exceed 89. That's the only way to interpret it. So for each period t, sum over all items i of inventory[t][i] ≤ 89.

But I need to confirm. Let me think about the example. Suppose there are two items. If the storage capacity is 89 per period, then in each period, the sum of the inventories of both items can't exceed 89. So that's the constraint.

So the constraints are:

For each period t and item i:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

Also, inventory[t][i] ≥ 0 (non-negative inventory)

And for each period t, sum_{i} inventory[t][i] ≤ storage_capacity.

But wait, the problem says "storage capacity is 89 per period". So that's per period. So for each period, the total inventory across all items must be ≤ 89.

So that's the constraint.

Now, the objective is to minimize the sum of order costs and holding costs. The order cost is unit_order_cost[i] * order[t][i] for each order. The holding cost is holding_cost[i] * inventory[t][i] for each period.

So the objective function is sum over all t and i of (unit_order_cost[i] * order[t][i] + holding_cost[i] * inventory[t][i]).

Now, how to model this in PuLP.

First, I need to create the problem. Let's start by importing pulp and os.

Then, the build_model function will create the problem.

Let me outline the steps:

1. Define the problem as a minimization problem.

2. Create decision variables:

   For each item i (0 to items-1) and period t (0 to periods-1), order[i][t] is the quantity ordered in period t for item i.

   Also, inventory[t][i] is the inventory after period t for item i.

But wait, inventory can be derived from the previous inventory, order, and demand. However, since we need to track inventory levels for constraints, we need to model them as variables.

Alternatively, we can model the inventory as variables and express the constraints that relate them to the orders and demands.

So, for each item i and period t:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But for t=0, inventory[-1][i] is the initial inventory.

So, for t=0, inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]

But since initial inventory is given, we can model that.

So, the variables are:

order[i][t] for each i and t.

inventory[t][i] for each t and i.

But perhaps we can model the inventory as variables and express the constraints.

But in PuLP, variables can be created with loops.

So, first, create the problem.

Then, create the variables:

orders = [[pulp.LpVariable(f"order_{i}_{t}", lowBound=0) for t in range(periods)] for i in range(items)]

inventory = [[pulp.LpVariable(f"inventory_{i}_{t}", lowBound=0) for t in range(periods)] for i in range(items)]

Wait, but the inventory variables need to be connected via constraints.

Then, for each period t and item i, we need to set the constraint that inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But for t=0, inventory[-1][i] is the initial inventory. So for t=0, the equation is:

inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]

But since initial_inventory is given, we can model that.

So, for each item i and period t:

if t == 0:

   inventory[t][i] = initial_inventory[i] + order[t][i] - demand[t][i]

else:

   inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But in PuLP, we can't directly assign equations, but we can create constraints that enforce these relationships.

So for each t and i, we can create a constraint that:

inventory[t][i] - inventory[t-1][i] - order[t][i] + demand[t][i] = 0

But for t=0, inventory[-1][i] is initial_inventory[i], so the equation becomes:

inventory[0][i] - initial_inventory[i] - order[0][i] + demand[0][i] = 0

Wait, that's for t=0. So for each t, the constraint is:

inventory[t][i] - (inventory[t-1][i] if t>0 else initial_inventory[i]) - order[t][i] + demand[t][i] = 0

But how to model that in code.

Alternatively, for each t and i:

if t == 0:

   constraint: inventory[t][i] == initial_inventory[i] + order[t][i] - demand[t][i]

else:

   constraint: inventory[t][i] == inventory[t-1][i] + order[t][i] - demand[t][i]

So in code, for each t in 0 to periods-1:

for each i in 0 to items-1:

   if t == 0:

      prob += inventory[t][i] == initial_inventory[i] + order[t][i] - demand[t][i]

   else:

      prob += inventory[t][i] == inventory[t-1][i] + order[t][i] - demand[t][i]

But in PuLP, the equality is written as prob += inventory[t][i] == ... 

But since the variables are already defined, this should work.

Then, the storage capacity constraint: for each period t, sum over all items i of inventory[t][i] <= storage_capacity.

So for each t in 0 to periods-1:

prob += pulp.lpSum([inventory[t][i] for i in range(items)]) <= storage_capacity

Also, the objective function is the sum of order costs and holding costs.

Order cost: for each t and i, unit
