<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has 4 items over 5 periods. Each period, we need to decide how much to order for each item, considering initial inventory, demand, storage capacity, and costs. The goal is to minimize the total order and holding costs while respecting inventory balance and storage constraints.

First, I'll outline the steps:

1. **Define Decision Variables**: For each item and period, decide the order quantity. Also, maybe track the inventory level after each period. But since inventory is determined by previous inventory, orders, and demand, perhaps I can model the inventory levels as variables too. Wait, but maybe it's better to model the order quantities and compute inventory levels based on that.

Wait, the inventory balance equation is: inventory[t] = inventory[t-1] + order[t] - demand[t]. So for each item and period, the inventory after the period must be non-negative and not exceed the storage capacity.

But how to model this? Let me think. For each item i and period t, the inventory after the period is initial_inventory[i] + sum of orders from previous periods up to t, minus the sum of demands up to t. Wait, no. Actually, the inventory at the start of period t is initial_inventory[i] plus any orders placed in previous periods, minus the demands up to period t-1. Then, during period t, we place an order, which is added to the inventory, and then subtract the demand of period t. So the inventory after period t is inventory_before + order[t] - demand[t].

But maybe it's easier to model the inventory after each period. Let me think: for each item i and period t, the inventory after period t is equal to the inventory after period t-1 plus the order quantity for period t minus the demand for period t. Also, this inventory must be between 0 and the storage capacity.

So, the decision variables would be the order quantities for each item and period. Then, the inventory levels can be derived from these variables.

But how to model the inventory levels? Let me think. For each item i and period t, the inventory after period t is:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But since inventory[i][t] must be >= 0 and <= storage_capacity.

But since the initial inventory is given, for t=0 (before the first period), inventory[i][0] = initial_inventory[i]. Then, for t >=1, the inventory[i][t] is computed as above.

But how to model this in PuLP? Because the inventory levels depend on previous periods. So, for each item and period, we need to track the inventory level. However, since the order variables are the only variables we need to decide, perhaps we can model the inventory levels as variables as well.

Alternatively, we can model the inventory levels as variables and express the constraints based on the order variables. Let me think.

Let me define:

For each item i (0 to 3), and period t (0 to 4), inventory[i][t] is the inventory after period t.

But for t=0, inventory[i][0] = initial_inventory[i].

For t >=1, inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But since the order[i][t] is the quantity ordered in period t, which is added to the inventory before the demand of period t is subtracted.

Wait, the order is placed at the beginning of the period, so the inventory before demand is inventory[i][t-1] + order[i][t], then subtract the demand[i][t] to get inventory[i][t].

So the constraint is:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But since inventory[i][t] must be >=0 and <= storage_capacity.

So, for each item and period, we have:

inventory[i][t] >= 0

inventory[i][t] <= storage_capacity

But how to model this in PuLP? Because the inventory[i][t] depends on previous inventory and order variables.

So, the approach would be:

- Create variables for order[i][t] for each item and period.

- Create variables for inventory[i][t] for each item and period.

But since inventory[i][t] is determined by previous inventory and order, we can model the constraints as:

For each item i and period t >=1:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But since inventory[i][t] is a variable, we can express this as a constraint.

But for t=0, inventory[i][0] is fixed as initial_inventory[i].

So, the steps are:

1. Define the problem as a minimization problem.

2. Define the decision variables: order[i][t] for each item and period.

3. Define the inventory variables for each item and period.

4. Add constraints for the inventory balance equations.

5. Add constraints for the storage capacity (inventory[i][t] <= storage_capacity for all i and t).

6. Add constraints for inventory[i][t] >= 0.

7. The objective function is the sum of order costs (unit_order_cost[i] * order[i][t] for all i and t) plus the sum of holding costs (holding_cost[i] * inventory[i][t] for all i and t).

Wait, but the holding cost is per unit held in inventory. So for each period, the holding cost is holding_cost[i] multiplied by the inventory after the period, right? Because the inventory after the period is the amount held during the next period. Or is it the inventory before the demand is subtracted? Wait, the problem says "holding cost" is per unit held. So if the inventory after the period is the amount that is held during the next period, then the holding cost for period t is based on the inventory after the period. But maybe the problem defines the holding cost as the cost for the inventory at the end of the period. So the holding cost for each period is holding_cost[i] * inventory[i][t].

So the objective function is sum over all items and periods of (unit_order_cost[i] * order[i][t] + holding_cost[i] * inventory[i][t]).

But wait, the problem says "Minimize order and holding costs subject to inventory balance and capacity." So the order cost is for each order placed, and the holding cost is for the inventory held at the end of each period.

So the objective function is:

Total cost = sum_{i=0 to 3} sum_{t=0 to 4} (unit_order_cost[i] * order[i][t] + holding_cost[i] * inventory[i][t])

Wait, but for t=0, the inventory is initial, but there's no order in period 0. Wait, the periods are 5, so maybe the periods are 0 to 4 (since 5 periods). But the initial inventory is before any periods. So for t=0, the inventory is initial, and the first order is in period 0? Or is the first period t=1?

Wait, the problem says "plan replenishment for 4 items and 5 periods". The demand is given as a list of 5 elements for each item. So the periods are 0 to 4 (assuming 0-based index). So for each period t (0 to 4), there is a demand. The initial inventory is before any periods. So the first order is in period 0, which would affect the inventory after period 0.

So the order variables are for each period t (0 to 4). So for each item i and period t, order[i][t] is the quantity ordered in period t.

Then, the inventory after period t is:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But for t=0, inventory[i][t-1] is the initial inventory. So for t=0, the equation is:

inventory[i][0] = initial_inventory[i] + order[i][0] - demand[i][0]

Wait, no. Wait, the initial inventory is before any periods. So during period 0, the order is placed, which is added to the initial inventory, then the demand for period 0 is subtracted. So the inventory after period 0 is initial_inventory[i] + order[i][0] - demand[i][0].

But for t=0, the inventory after the period is inventory[i][0], which is computed as initial_inventory[i] + order[i][0] - demand[i][0].

But for t >=1, inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t].

So the constraints for inventory are:

For each item i and period t:

if t == 0:

inventory[i][t] = initial_inventory[i] + order[i][t] - demand[i][t]

else:

inventory[i][t] = inventory[i][t-1] + order[i][t] - demand[i][t]

But since inventory[i][t] must be >=0 and <= storage_capacity.

So, in PuLP, I need to model these constraints.

Now, the variables:

order[i][t] is the quantity ordered for item i in period t.

inventory[i][t] is the inventory after period t.

But since inventory[i][t] is determined by previous variables, we can model the constraints as:
