<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem is a single-item, multi-period replenishment. There are 6 periods. The initial inventory is 11. Demands for each period are given as [29, 23, 47, 46, 20, 18]. The unit order cost is 1, and holding cost is 2. The task is to formulate and solve a linear inventory-balance model.

First, I need to define the decision variables. The main variables here are the order quantities for each period and the inventory levels at the end of each period. Let me think: for each period, we decide how much to order (let's call it order[t]), and the inventory after meeting demand (inventory[t]).

The objective is to minimize the total cost, which includes ordering costs and holding costs. So the objective function will be sum of (unit_order_cost * order[t]) for all periods plus sum of (holding_cost * inventory[t]) for all periods.

Constraints: For each period, the inventory at the start plus the order must meet the demand and the inventory after. Wait, the inventory at the start of period t is inventory[t-1], right? Because inventory[t] is the end of period t. So the balance equation is:

inventory[t-1] + order[t] - demand[t] = inventory[t]

But for the first period, the initial inventory is 11. So for t=1, inventory[0] is 11. Then for t=1 to 6, the equation holds.

Wait, the periods are 6, so maybe the indices are from 0 to 5? Or 1 to 6? Let me check the problem data. The periods are 6, and the demand is a list of 6 elements. So probably, the periods are indexed from 0 to 5. Let me adjust.

So for each period t in 0 to 5:

inventory[t] = inventory[t-1] + order[t] - demand[t]

But for t=0, inventory[-1] would be the initial inventory, which is 11. So the initial inventory is inventory[-1] = 11. Then for t=0, inventory[0] = 11 + order[0] - demand[0].

Wait, maybe it's better to index periods from 1 to 6. Let me think again. Let's say periods are 1 to 6. Then initial inventory is at period 0. So for period 1, the inventory at the start is initial_inventory. Then for each period t (1 to 6), the inventory after meeting demand is inventory[t] = inventory[t-1] + order[t] - demand[t]. But since the problem has 6 periods, the last period is 6. So the inventory after period 6 is inventory[6], which might be zero or not, but the problem doesn't specify any end inventory constraints. So the model doesn't need to have a constraint on the final inventory. So the constraints are for each period t from 1 to 6, the inventory balance equation.

But in terms of code, how to model this? Let's think of the periods as 0 to 5 (since there are 6 periods). Then initial inventory is 11. For each period t in 0 to 5:

inventory[t] = inventory[t-1] + order[t] - demand[t]

But for t=0, inventory[-1] is the initial inventory. So perhaps, the initial inventory is a variable? No, it's a given value. So the initial inventory is 11, which is the inventory before period 0. So for period 0, the equation is:

inventory[0] = initial_inventory + order[0] - demand[0]

Then for period 1:

inventory[1] = inventory[0] + order[1] - demand[1]

And so on up to period 5.

So the variables are order[t] for t in 0 to 5, and inventory[t] for t in 0 to 5.

But the problem is that inventory[t] can't be negative. Wait, the problem doesn't specify any constraints on inventory levels, but in reality, inventory can't be negative. However, the problem says it's a linear model. So maybe we need to assume that the model ensures non-negative inventory. But the problem statement doesn't mention that. Wait, the problem says "formulate and solve a linear inventory-balance model". So perhaps the model allows for negative inventory? Or maybe the constraints are that inventory[t] >= 0. But the problem doesn't specify. Hmm. Let me check the problem statement again.

The problem says "linear inventory-balance model". Typically, in such models, inventory can't be negative. So we need to add constraints that inventory[t] >= 0 for all t. But the problem doesn't mention this. However, the problem might not require it. Wait, but if the model allows negative inventory, then the solution might not be feasible. So perhaps the model should include non-negativity constraints on inventory and order variables.

But the problem says "formulate and solve a linear inventory-balance model". So the standard approach is to have non-negativity constraints on orders and inventory. So I need to include that.

So the variables are order[t] >= 0 and inventory[t] >= 0 for all t.

Now, the objective function is to minimize the total cost, which is sum over all periods of (unit_order_cost * order[t]) + sum over all periods of (holding_cost * inventory[t]).

So the steps are:

1. Create the PuLP problem.

2. Define the decision variables: order and inventory for each period.

3. Define the objective function.

4. Add the constraints for inventory balance.

5. Add non-negativity constraints.

Now, let's think about the code structure.

First, the parameters are given as JSON. The code needs to read them, but in the problem, the parameters are provided as a JSON structure. However, the code is supposed to be self-contained. So the code will have the parameters hard-coded, as per the JSON given.

So the code will have:

periods = 6

initial_inventory = 11

demand = [29, 23, 47, 46, 20, 18]

unit_order_cost = 1

holding_cost = 2

Then, the code will create variables for order and inventory.

In PuLP, variables can be created with LpVariable. For each period, we can have order[t] and inventory[t].

But since the periods are 6, and the code is in Python, perhaps we can loop through the periods.

So, for t in 0 to 5 (since there are 6 periods), create order[t] and inventory[t].

But in PuLP, variables can be created as a list. So:

orders = [pulp.LpVariable(f"order_{t}", lowBound=0) for t in range(periods)]

inventories = [pulp.LpVariable(f"inventory_{t}", lowBound=0) for t in range(periods)]

Wait, but the initial inventory is 11. So for the first period (t=0), the inventory after the order is:

inventory[0] = initial_inventory + order[0] - demand[0]

But the initial_inventory is a constant. So the constraint for t=0 is:

inventories[0] == initial_inventory + orders[0] - demand[0]

For t >=1, the constraint is:

inventories[t] == inventories[t-1] + orders[t] - demand[t]

So for each t in 1 to 5 (since periods are 0 to 5), we have that constraint.

So the code will need to add these constraints.

So the code steps:

- Create the problem.

- Create variables for orders and inventories.

- Add constraints for each period.

- Add the objective function.

Now, the objective function is sum(orders[t] * unit_order_cost for t in 0..5) + sum(inventories[t] * holding_cost for t in 0..5).

So the code will have:

prob += pulp.lpSum([unit_order_cost * orders[t] for t in range(periods)]) + pulp.lpSum([holding_cost * inventories[t] for t in range(periods)])

Then, the constraints:

For t=0:

prob += inventories[0] == initial_inventory + orders[0] - demand[0]

For t in 1 to 5:

prob += inventories[t] == inventories[t-1] + orders[t] - demand[t]

But in PuLP, the constraints need to be added with names. So for each constraint, we need to give a name.

So for the first constraint (t=0), name it "inventory_balance_period_0".

For t=1 to 5, name them "inventory_balance_period_t".

So in code:

for t in range(periods):

    if t == 0:

        constraint_name = f"inventory_balance_period_0"

    else:

        constraint_name = f"inventory_balance_period_{t}"

    prob += inventories[t] == initial_inventory + orders[t] - demand[t] if t == 0 else inventories[t] == inventories[t-1] + orders[t] - demand[t]

Wait, but for t=0, the initial_inventory is 11. So the equation is inventories[0] = 11 + orders[0] - demand[
