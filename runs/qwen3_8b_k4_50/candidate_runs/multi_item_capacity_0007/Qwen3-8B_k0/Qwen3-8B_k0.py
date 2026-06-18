<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has 4 items over 3 periods. Each period, we need to decide how much to order for each item, considering initial inventory, demand, storage capacity, and costs. The goal is to minimize the total order and holding costs while respecting inventory balance and storage limits.

First, I'll outline the steps. The main components are:

1. **Decision Variables**: For each item and period, decide the order quantity. Also, maybe track inventory levels. But since inventory is a result of orders and demand, perhaps it's better to model the order variables and compute inventory as a function of those.

Wait, but in PuLP, we can model the inventory levels as variables too. However, since inventory is determined by previous inventory, orders, and demand, maybe it's better to model the order variables and compute inventory as a function. But for constraints, we need to ensure that inventory doesn't exceed capacity and that the balance is correct.

Alternatively, we can model the inventory levels as variables. Let me think. For each item and period, the inventory after meeting demand must be non-negative. Also, the storage capacity per period is 124. So, for each period, the sum of all items' inventory levels can't exceed 124.

But how to model the inventory balance? For each item, the inventory at the start of the period plus the order quantity minus the demand equals the inventory at the end of the period. Wait, but the initial inventory is given for each item. So for period 1, the initial inventory is the starting point. Then, for each period, the inventory after order and before demand is the previous inventory plus order. Then, subtract demand to get the ending inventory.

Wait, maybe the order is placed at the beginning of the period, so the inventory at the start of the period plus the order quantity minus the demand equals the inventory at the end of the period. But the storage capacity applies to the inventory at the end of the period, right? Because that's the inventory that's stored.

So for each item and period, the ending inventory (after order and demand) must be non-negative. Also, the sum of all items' ending inventories in each period must not exceed the storage capacity.

So the decision variables would be the order quantities for each item and period. Then, the inventory levels can be calculated based on previous inventory, order, and demand.

But how to model that in PuLP? Let's think.

Let me define variables:

For each item i (0-3) and period t (0-2), let's have order[i][t] as the quantity ordered in period t for item i.

Then, the inventory for item i at the end of period t is:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But inventory[i][-1] (previous period) would be the initial inventory. Wait, for period 0 (first period), the initial inventory is the starting point. So for t=0, inventory[i][t] = initial_inventory[i] + order[i][0] - demand[i][0]. Then, for t=1, inventory[i][1] = inventory[i][0] + order[i][1] - demand[i][1], and so on.

But since the inventory at the end of period t must be non-negative, and the sum of all inventory[i][t] across items must be <= storage_capacity.

So the constraints are:

For each item i and period t:

inventory[i][t] >= 0

And for each period t:

sum_{i=0 to 3} inventory[i][t] <= storage_capacity

But how to model the inventory[i][t] in terms of the order variables?

We can model inventory[i][t] as a variable, but that might complicate things. Alternatively, we can express inventory[i][t] in terms of previous inventory and order.

But since the initial inventory is known, perhaps we can model the inventory as a variable for each item and period, and then create constraints that link them.

Alternatively, since the inventory is determined by the order and previous inventory, maybe we can model it as a recursive relation.

Let me think about how to structure this in PuLP.

First, create variables for order[i][t], and then compute the inventory[i][t] as:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But for t=0, inventory[i][t-1] is the initial inventory.

So for each item i and period t:

inventory[i][t] = initial_inventory[i] + sum_{s=0 to t} order[i][s] - sum_{s=0 to t} demand[i][s]

Wait, no. Because for each period, the inventory after order and before demand is previous inventory plus order. Then, subtract demand to get the ending inventory. So for period t, the ending inventory is:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But for t=0, inventory[i][t-1] is the initial inventory.

So for each item i and period t, we can model the inventory[i][t] as a variable, and then create constraints that link them.

But how to handle that in PuLP? Let's think.

We can create variables for inventory[i][t], and then for each t and i, create a constraint that links inventory[i][t] to inventory[i][t-1], order[i][t], and demand[i][t].

But for t=0, the initial inventory is known. So for t=0, inventory[i][0] = initial_inventory[i] + order[i][0] - demand[i][0]

For t >=1, inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

So for each item i and period t, we can create a constraint that enforces this relationship.

But since the inventory[i][t] variables are part of the model, we can model them as variables and then create these constraints.

Additionally, the storage capacity constraint for each period t is sum_{i} inventory[i][t] <= storage_capacity.

Also, the order quantities must be non-negative, since you can't order a negative amount.

So the steps are:

1. Define variables for order[i][t] (non-negative) and inventory[i][t] (non-negative).

But wait, inventory[i][t] can be zero or positive. So the inventory variables are non-negative.

But the order variables are also non-negative.

So the model will have:

- Variables: order[i][t] for i in 0..3, t in 0..2

- Variables: inventory[i][t] for i in 0..3, t in 0..2

But maybe we can avoid having inventory variables by expressing them in terms of order variables. However, that might complicate the constraints. Alternatively, using inventory variables makes the constraints easier to model.

But let's proceed with the variables.

So, for each item i and period t:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But for t=0, inventory[i][t-1] is initial_inventory[i].

So for each t in 0 to 2:

For t=0:

inventory[i][0] = initial_inventory[i] + order[i][0] - demand[i][0]

For t >=1:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

So for each i and t, we can create a constraint that enforces this.

Additionally, for each period t, sum over all i of inventory[i][t] <= storage_capacity.

Also, the inventory[i][t] must be >= 0.

But wait, the inventory[i][t] can't be negative. So for each i and t, inventory[i][t] >= 0.

But since the order is chosen to meet demand, perhaps the inventory[i][t] will naturally be non-negative. However, to be safe, we can add constraints that inventory[i][t] >= 0.

But maybe the constraints from the inventory balance equations already ensure that. For example, if the order is sufficient to meet demand, then inventory[i][t] would be non-negative. However, if the order is not enough, then inventory[i][t] could be negative. So we need to add the constraints that inventory[i][t] >= 0.

So the steps for the model:

- Create variables for order[i][t] and inventory[i][t].

- For each i and t, create the inventory balance constraint.

- For each period t, create the storage capacity constraint.

- Add the non-negativity constraints for inventory[i][t].

- The objective is to minimize the sum of order costs and holding costs.

Order cost is sum over all i and t of unit_order_cost[i] * order[i][t]

Holding cost is sum over all i and t of holding_cost[i] * inventory[i][t]

Wait, but the holding cost is per unit of inventory at the end of the period. So yes, the holding cost is based on the ending inventory.

So the objective function is:

minimize sum_{i=0 to 3} sum_{t=0 to 2} (unit_order_cost[i] * order[i][t] + holding_cost[i] * inventory[i][t])

Now, let's think about how to implement this in PuLP.

First,
