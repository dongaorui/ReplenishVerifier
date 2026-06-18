<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem with fixed order costs and the Big-M method. Let me start by understanding the problem.

The firm has a 4-period horizon. They start with 20 units of inventory. Demands for each period are given as [55, 32, 48, 46]. The costs are unit_order_cost=2, holding_cost=3, fixed_order_cost=48, and Big-M is 181. The goal is to minimize total costs, which include ordering, holding, and fixed setup costs.

First, I need to model this as a mixed-integer linear program. The key here is to use binary variables to represent whether an order is placed in a period. The Big-M method is used to handle the fixed costs, so I'll need to create constraints that link the binary variables to the order quantities.

Let me think about the decision variables. For each period, I'll need:

- Order quantity (let's say o_t) which is a non-negative real variable.
- Binary variable y_t indicating if an order is placed in period t (1 if ordered, 0 otherwise).

But wait, since the order quantity can be any non-negative number, but the fixed cost is only incurred if there's an order. So the fixed cost is fixed_order_cost * y_t. However, the unit order cost is per unit ordered, so that's unit_order_cost * o_t. The holding cost is based on the ending inventory, which depends on the previous inventory and the order quantity minus demand.

The inventory balance for each period should be: inventory_t = inventory_{t-1} + o_t - demand_t. But since inventory can't be negative, we need to ensure that inventory_t >= 0. Wait, but the problem doesn't mention backorders, so I assume that the inventory can't be negative. So the constraints would be:

inventory_t >= 0 for all t.

But how to model the inventory? Let's think step by step.

The initial inventory is 20. For each period t from 1 to 4:

inventory_0 = 20

inventory_t = inventory_{t-1} + o_t - demand_t

But since inventory_t can't be negative, we need to ensure that inventory_{t-1} + o_t >= demand_t. Wait, no. Because if inventory_{t-1} + o_t is less than demand_t, then the inventory would be negative, which isn't allowed. So the constraint is inventory_{t-1} + o_t - demand_t >= 0. But since inventory_t is the ending inventory, which is the previous inventory plus order minus demand. So the constraint is inventory_t >= 0.

But how to model this with variables. Let me think. Let's define inventory_t as the ending inventory after period t. Then:

inventory_0 = 20

For t >= 1:

inventory_t = inventory_{t-1} + o_t - demand_t

But since inventory_t can't be negative, we have:

inventory_t >= 0

But how to express this in terms of variables. Since o_t is the order quantity, and we need to track inventory over time.

Now, the objective function is to minimize the sum of:

- Unit order cost * o_t for each period (unit_order_cost * o_t)
- Holding cost * inventory_t for each period (holding_cost * inventory_t)
- Fixed order cost * y_t for each period (fixed_order_cost * y_t)

So the total cost is sum over t of (unit_order_cost * o_t + holding_cost * inventory_t + fixed_order_cost * y_t)

But how to model the relationship between o_t and y_t. Since the fixed cost is only incurred if an order is placed. So y_t is 1 if o_t > 0, and 0 otherwise. However, in linear programming, we can't directly model this. So we use the Big-M method. The idea is to enforce that if y_t is 1, then o_t can be any non-negative value, but if y_t is 0, then o_t must be 0. To model this, we can use the constraint:

o_t <= M * y_t

where M is a sufficiently large number. But since the problem gives M=181, we can use that. Wait, but the problem says to use M=181. So the Big-M value is given as 181. So the constraint would be o_t <= M * y_t. But since M is 181, which is larger than the maximum possible order quantity. Wait, but what's the maximum possible order quantity? For example, in period 1, the demand is 55. The initial inventory is 20. So if we order 55, then inventory after period 1 would be 20 + 55 - 55 = 20. But maybe in some periods, the order quantity could be larger than the demand. However, the Big-M value should be chosen such that it's larger than the maximum possible order quantity. But the problem says to use M=181, so we can proceed with that.

So the constraints for the Big-M method are:

o_t <= M * y_t for each t.

But since o_t is non-negative, and y_t is binary, this ensures that if y_t is 0, then o_t must be 0. If y_t is 1, then o_t can be up to M.

But wait, the problem says to use the Big-M method. So the fixed cost is modeled as fixed_order_cost * y_t, and the constraints are:

o_t <= M * y_t

and

o_t >= 0

But also, since the order quantity can't be negative, we have o_t >= 0.

Now, the inventory constraints. Let's model the inventory for each period. Let me define inventory as a variable for each period. Let's say inventory is a list of variables, inventory[0] is the initial inventory, which is 20. Then for each period t (from 1 to 4), inventory[t] = inventory[t-1] + o_t - demand[t-1]. Wait, the demand is given as a list for periods 0 to 3 (since periods are 4). So for period 1 (t=1), the demand is demand[0] = 55.

But in the code, perhaps it's easier to index from 0 to 3 for the periods. Let me think. Let's say periods are 0 to 3 (since there are 4 periods). Then for each period t in 0 to 3:

inventory[t] = inventory[t-1] + o[t] - demand[t]

But for t=0, inventory[-1] is the initial inventory, which is 20. So for t=0, inventory[0] = initial_inventory + o[0] - demand[0]. Wait, no. Wait, the initial inventory is before any periods. So for period 0, the inventory starts at 20. Then, after placing an order in period 0, the inventory is updated. So perhaps the inventory variables are for after each period. Let me clarify:

Let me define inventory as a list where inventory[t] is the ending inventory after period t. Then:

inventory[0] = initial_inventory + o[0] - demand[0]

inventory[1] = inventory[0] + o[1] - demand[1]

and so on.

But for the first period, the initial inventory is 20. So for t=0, inventory[0] = 20 + o[0] - demand[0]. Then, for t=1, inventory[1] = inventory[0] + o[1] - demand[1], etc.

But the problem is that the inventory must be non-negative. So for each t, inventory[t] >= 0.

So the constraints are:

inventory[t] >= 0 for all t in 0 to 3.

But how to model this in PuLP. Let me think about the variables.

Variables:

- o_t: order quantity in period t. Non-negative real variables.

- y_t: binary variables indicating if an order is placed in period t (1 if ordered, 0 otherwise).

- inventory_t: non-negative real variables representing ending inventory after period t.

So the steps are:

1. Create variables for o_t, y_t, and inventory_t.

2. Set up the objective function as sum of unit_order_cost * o_t + holding_cost * inventory_t + fixed_order_cost * y_t for all t.

3. Set up the inventory constraints:

inventory[0] = initial_inventory + o[0] - demand[0]

inventory[1] = inventory[0] + o[1] - demand[1]

and so on.

But since inventory is a variable, we can model these as equations. For example, for each t in 0 to 3:

inventory[t] = inventory[t-1] + o[t] - demand[t]

But for t=0, inventory[-1] is the initial inventory, which is 20. So for t=0, inventory[0] = 20 + o[0] - demand[0].

But in PuLP, we can model this with constraints. For each t in 1 to 3 (since t starts from 0?), wait, the periods are 0 to 3 (4 periods). So for t in 0 to 3:

if t == 0:

inventory[0] = initial
