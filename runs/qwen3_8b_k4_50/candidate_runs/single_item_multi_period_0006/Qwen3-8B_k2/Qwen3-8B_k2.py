<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem. Let me start by understanding the problem details.

The problem has 4 periods. The initial inventory is 29. Demands for each period are [51, 60, 35, 28]. The unit order cost is 4, and holding cost is 4. The task is to formulate a linear inventory-balance model.

First, I need to define the decision variables. The main variables here are the order quantities for each period. Let's denote them as Q1, Q2, Q3, Q4. Also, since inventory carries over, we need to track the inventory levels after each period. Let's call them I1, I2, I3, I4. Wait, but maybe it's better to model the inventory after each period. Let me think.

The inventory balance equation for each period should be: inventory at the start of the period plus the order quantity minus the demand equals the inventory at the end of the period. Wait, but the initial inventory is given. So for period 1, the starting inventory is initial_inventory. Then, after ordering Q1, the inventory after period 1 is initial_inventory + Q1 - demand[0]. Then for period 2, the starting inventory is the previous end inventory, so I1 = initial_inventory + Q1 - D1. Then, the inventory after period 2 is I1 + Q2 - D2, and so on.

But the problem is to minimize the total cost, which includes ordering costs and holding costs. The ordering cost is unit_order_cost multiplied by the sum of all Q's. The holding cost is holding_cost multiplied by the sum of the inventory levels at the end of each period. Wait, or is it the average inventory? Wait, the problem says "holding cost" which is typically per unit per period. So for each period, the holding cost is the ending inventory multiplied by the holding cost rate. So the total holding cost is sum over all periods of (ending inventory) * holding_cost.

So the objective function is to minimize total ordering cost plus total holding cost. The ordering cost is sum(Q_i * unit_order_cost) for each period. The holding cost is sum(I_i * holding_cost) for each period, where I_i is the ending inventory after period i.

Now, the constraints are the inventory balance equations for each period. Let's index periods from 1 to 4. For period 1:

I_0 (initial inventory) + Q1 - D1 = I1

For period 2:

I1 + Q2 - D2 = I2

Similarly for periods 3 and 4.

But since the initial inventory is given, I0 is 29. So the constraints are:

For each period t in 1 to 4:

I_{t-1} + Q_t - D_t = I_t

But I0 is 29. So for t=1, I0 is 29. For t=2, I1 is the ending inventory of period 1, etc.

So the variables are Q1, Q2, Q3, Q4 (order quantities) and I1, I2, I3, I4 (ending inventories). However, since the inventory levels are determined by the previous inventory and the order and demand, maybe we can express the I variables in terms of the Q variables. But for the model, it's easier to have them as variables and set up the constraints.

But wait, maybe we can avoid having I variables as decision variables. Let me think. For example, the ending inventory after period t is equal to the starting inventory (which is the ending inventory of period t-1) plus Q_t minus D_t. So if we model the ending inventory as variables, we can set up these equations.

So the decision variables are Q1, Q2, Q3, Q4 (orders) and I1, I2, I3, I4 (ending inventories). But maybe we can express the I variables in terms of the Q variables. However, for the model, it's easier to have them as variables and set up the constraints.

But perhaps it's better to model the ending inventory as variables. Let me proceed.

So the variables are:

Q1, Q2, Q3, Q4 (order quantities)

I1, I2, I3, I4 (ending inventories)

Constraints:

For period 1:

I0 + Q1 - D1 = I1

But I0 is 29, so:

29 + Q1 - D1 = I1

Similarly for period 2:

I1 + Q2 - D2 = I2

Period 3:

I2 + Q3 - D3 = I3

Period 4:

I3 + Q4 - D4 = I4

Additionally, all variables must be non-negative. Because you can't order negative quantities, and inventory can't be negative. Wait, but inventory can be negative? No, because if you have negative inventory, that's a shortage. But the problem doesn't mention backorders, so I assume that the inventory can't be negative. So the constraints are:

For each period t, the ending inventory I_t >= 0.

Wait, but the problem says "inventory-balance model", which typically assumes that inventory can't be negative. So we need to ensure that the ending inventory is non-negative for each period.

So the constraints are:

I0 + Q1 - D1 = I1 >= 0

I1 + Q2 - D2 = I2 >= 0

I2 + Q3 - D3 = I3 >= 0

I3 + Q4 - D4 = I4 >= 0

But since I0 is 29, which is fixed, the first constraint is 29 + Q1 - D1 = I1, and I1 >= 0.

So the model variables are Q1, Q2, Q3, Q4 (orders) and I1, I2, I3, I4 (ending inventories). However, perhaps we can eliminate the I variables by expressing them in terms of the Q variables. For example, I1 = 29 + Q1 - D1, I2 = I1 + Q2 - D2 = 29 + Q1 - D1 + Q2 - D2, etc. But in that case, the I variables are not needed as decision variables. However, the holding cost is based on the ending inventory, which would be the I variables. So if we can express the I variables in terms of the Q variables, then we can compute the holding cost as sum over (I_t) * holding_cost, where I_t is expressed in terms of Q variables.

But for the model, it's easier to have the I variables as variables and set up the constraints. However, since the I variables are determined by the Q variables, maybe we can model them as expressions. But in PuLP, variables are needed for the constraints. So perhaps it's better to model the I variables as variables and set up the constraints.

But let's think again. Let me try to model the problem with the Q variables and the I variables.

The objective function is:

Total cost = sum(Q_i * unit_order_cost) + sum(I_i * holding_cost)

So for each period, the order cost is Q_i * unit_order_cost, and the holding cost is I_i * holding_cost.

So the variables are Q1, Q2, Q3, Q4, I1, I2, I3, I4.

Constraints:

For each period t from 1 to 4:

I_{t-1} + Q_t - D_t = I_t

With I_0 = 29.

Additionally, I_t >= 0 for all t.

But since I_0 is fixed, the first constraint is:

29 + Q1 - D1 = I1

Then, for t=2:

I1 + Q2 - D2 = I2

And so on.

So in PuLP, we can model these equations as constraints.

Now, the variables need to be non-negative. So Q1, Q2, Q3, Q4 >= 0, and I1, I2, I3, I4 >= 0.

So the steps are:

1. Import pulp and os.

2. Define the problem as an LpProblem.

3. Define the decision variables: Q1, Q2, Q3, Q4, I1, I2, I3, I4.

But maybe we can model the I variables as expressions. Wait, but for the constraints, we need to have them as variables. So perhaps it's better to have them as variables.

Alternatively, since the I variables are determined by the Q variables and the previous I variables, maybe we can model them as expressions. For example, I1 = 29 + Q1 - D1. But then, the holding cost is based on I1, which is 29 + Q1 - D1. However, the problem is that for the next period, I2 = I1 + Q2 - D2. So if we model I1 as an expression, then I2 would be that expression plus Q2 - D2, etc. But in PuLP, variables can't be expressions unless we use the LpAffineExpression. However, for the constraints, we can model them as equations.

But perhaps it's easier to model the I variables as variables and set up the constraints. Let's proceed with that.

So, in code:

We'll have variables for each Q and I.

But let's think about the code structure.

First, the parameters
