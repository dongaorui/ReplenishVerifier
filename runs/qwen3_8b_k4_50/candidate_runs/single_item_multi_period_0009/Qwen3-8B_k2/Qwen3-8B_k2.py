<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has 4 periods. The initial inventory is 25. Demand for each period is given as [58, 42, 53, 19]. The goal is to decide how much to order each period to minimize the total cost, which includes ordering and holding costs. Both unit costs are 4. 

First, I need to define the decision variables. For each period, the amount ordered. Let's call that variable 'order' for each period. Also, since inventory carries over, I need to track the inventory level after each period. But maybe I can model the inventory balance equations.

Wait, the problem says to use standard balance equations. So for each period, the inventory at the start plus the order minus the demand equals the inventory at the end. But the initial inventory is given. So for period 1, starting inventory is 25. Then, after ordering and meeting demand, the ending inventory becomes the starting inventory for the next period.

So the constraints would be for each period, the inventory balance. Also, the order quantity can't be negative. And the inventory can't be negative either, I assume. Wait, the problem doesn't mention backorders, so inventory can't be negative. So the ending inventory must be >=0.

Let me outline the steps:

1. Define the periods (4 in total).
2. Create decision variables for order quantity in each period. Let's say order[i] for period i (i from 0 to 3, since Python is 0-indexed).
3. The initial inventory is 25. Let's track the inventory after each period. Let's say inv[i] represents the inventory after period i. But maybe we can compute it based on the previous inventory and the order and demand.

Wait, for each period, the inventory after the period is equal to the inventory before the period plus the order minus the demand. So for period 1 (assuming periods are 0-based), inv[0] = initial_inventory. Then, for each period i (from 0 to 3), inv[i+1] = inv[i] + order[i] - demand[i]. But we need to ensure that inv[i] >= 0 for all periods. Wait, no. The inventory after the period (inv[i+1]) must be >=0. Because if you have negative inventory, that's not allowed. So for each period, the ending inventory must be non-negative.

So the constraints would be:

For each period i in 0 to 3:
inv[i+1] = inv[i] + order[i] - demand[i]
and inv[i+1] >= 0

But how to model this in PuLP? Since inv is a variable, but we can't have variables for inv. Wait, maybe we can model the inventory as a variable, but perhaps it's easier to express the constraints in terms of the order variables and the demand.

Alternatively, since the inventory after each period depends on the previous inventory and the order, we can model this with constraints. Let me think.

Let me define the initial inventory as inv_0 = 25. Then, for each period i (from 0 to 3), the inventory after the period is inv_{i} = inv_{i-1} + order_i - demand_i. But inv_0 is given. So for each period, the constraint would be:

inv_i = inv_{i-1} + order_i - demand_i

But since inv_i must be >=0, we can add that as a constraint.

But how to represent inv_i in PuLP? Well, perhaps we can create variables for the inventory after each period. Let's say inv = [inv_0, inv_1, inv_2, inv_3, inv_4], but since there are 4 periods, inv_0 is initial, and inv_4 is the ending inventory. Wait, but the problem doesn't have a period 4, so maybe the periods are 0 to 3, and inv_0 is initial, inv_1 after period 0, inv_2 after period 1, etc. So for each period i (0 to 3), inv_{i+1} = inv_i + order_i - demand_i. And inv_0 is 25.

So the variables are order_0, order_1, order_2, order_3. And the inv variables are inv_0, inv_1, inv_2, inv_3, inv_4. But inv_0 is fixed at 25. Then, for each i from 0 to 3:

inv_{i+1} = inv_i + order_i - demand_i

And inv_{i+1} >= 0.

So in PuLP, I can create variables for inv_0 to inv_4, but inv_0 is fixed. Wait, but maybe it's easier to model the inventory as a variable that depends on the previous period's inventory and the order. But how to handle that in PuLP?

Alternatively, since inv_0 is fixed, I can model the constraints for each period. For example:

For period 0:

inv_1 = inv_0 + order_0 - demand_0

Which is inv_1 = 25 + order_0 - 58

Similarly for period 1:

inv_2 = inv_1 + order_1 - demand_1

But inv_1 is 25 + order_0 - 58.

So, in PuLP, I can create variables for order and inv. Let me think about how to structure this.

Let me proceed step by step.

First, create the problem.

Import pulp and os.

Then, define the periods (4), initial inventory (25), demand list, unit order cost (4), holding cost (4).

The objective is to minimize the sum of ordering costs and holding costs.

Ordering cost is sum over all periods of (order_i * unit_order_cost).

Holding cost is sum over all periods of (inv_i * holding_cost), where inv_i is the inventory after the period. Wait, no. Wait, the holding cost is for the inventory at the end of the period. Because the inventory is carried forward. So for each period, the holding cost is the ending inventory of that period multiplied by the holding cost per unit.

Wait, the problem says "minimize the sum of ordering and inventory holding costs". So the holding cost is for the inventory that is held at the end of each period. So for each period, the holding cost is the ending inventory multiplied by the holding cost per unit.

So the objective function is:

sum(order_i * unit_order_cost for all i) + sum(inv_i * holding_cost for all i from 1 to 4?)

Wait, inv_0 is the initial inventory, but there's no holding cost for that. Because the holding cost is for the inventory that is carried over. So the holding cost is for the inventory after each period. So for each period, the ending inventory (inv_1, inv_2, inv_3, inv_4) would have holding cost. Wait, but inv_0 is the initial inventory. So the holding cost would be for inv_1, inv_2, inv_3, inv_4. Because those are the inventories at the end of each period. So the total holding cost is sum of inv_1 to inv_4 multiplied by holding cost.

But how to model that. So the objective is:

sum(order_i * unit_order_cost) + sum(inv_i * holding_cost for i in 1..4)

But inv_0 is fixed, so no cost for that.

So the variables are order_0, order_1, order_2, order_3 (for each period), and inv_0, inv_1, inv_2, inv_3, inv_4 (the inventory after each period).

But inv_0 is fixed at 25. So in PuLP, inv_0 is a constant, not a variable. Then, the other inv variables are variables.

So, the steps:

1. Create variables for order in each period (order_0 to order_3).

2. Create variables for inv_0 to inv_4. inv_0 is fixed at 25.

3. For each period i from 0 to 3:

   inv_{i+1} = inv_i + order_i - demand_i

   Also, inv_{i+1} >= 0

So, for each i in 0 to 3:

   inv[i+1] = inv[i] + order[i] - demand[i]

But in PuLP, how to model this? For each i, create a constraint that inv[i+1] - inv[i] - order[i] + demand[i] == 0.

So for each i in 0 to 3:

   prob += inv[i+1] - inv[i] - order[i] + demand[i] == 0

And also, inv[i+1] >= 0 for each i in 0 to 3.

So, the constraints are:

- For each period, the inventory balance equation.

- For each period, the ending inventory is non-negative.

Additionally, the order quantities must be non-negative, since you can't order negative.

So, for each order variable, add a constraint that order[i] >= 0.

Now, the objective function is:

sum(order[i] * unit_order_cost for all i) + sum(inv[i] * holding_cost for i in 1 to 4)

Wait, inv_0 is fixed, so the holding cost is for inv_1
