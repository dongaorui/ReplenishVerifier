<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve a single-item multi-period inventory replenishment problem. Let me start by understanding the problem details.

First, the problem has 4 periods. The initial inventory is 29. Demands for each period are given as [51, 60, 35, 28]. The unit order cost is 4, and the holding cost is 4. The task is to formulate a linear inventory-balance model.

So, the goal is to determine the order quantities for each period such that the total cost (ordering + holding) is minimized, while meeting the demand each period and not letting inventory go negative.

Let me think about the decision variables. For each period, we need to decide how much to order. Let's denote the order quantity in period t as x_t. Also, the inventory after meeting demand in period t would be the previous inventory plus the order minus the demand. But we need to track the inventory levels over time.

Wait, the initial inventory is 29. So, for each period, the inventory before meeting demand is the previous inventory plus the order. Then, subtract the demand. But we need to ensure that the inventory after meeting demand is non-negative. Wait, no, the inventory after meeting demand can't be negative. So, the inventory after demand is the previous inventory plus order minus demand, and this must be ≥ 0. Or is it that the inventory before demand is the previous inventory plus order, and then after subtracting demand, it's the ending inventory. So, the ending inventory for period t is (previous ending inventory + order t) - demand t. But the ending inventory can't be negative. Wait, no, the demand must be met, so the order plus previous inventory must be at least the demand. So, the ending inventory is (previous inventory + order) - demand. But that can't be negative. Wait, no. Let me think again.

Actually, the inventory at the start of period t is the ending inventory from period t-1. Then, during period t, you order x_t, so the inventory before meeting demand is ending inventory from t-1 + x_t. Then, you subtract the demand d_t. The ending inventory for period t is (ending inventory t-1 + x_t) - d_t. This must be ≥ 0. Because you can't have negative inventory. So, the constraints are that for each period t, ending inventory t-1 + x_t ≥ d_t. Wait, no. Wait, the ending inventory after meeting demand is (ending inventory t-1 + x_t) - d_t. This must be ≥ 0. So, the constraint is ending inventory t-1 + x_t - d_t ≥ 0. But how do we model this?

Alternatively, the inventory after order but before demand is (ending inventory t-1 + x_t). Then, after meeting demand, it's (ending inventory t-1 + x_t) - d_t. So, this must be ≥ 0. Therefore, the constraint is ending inventory t-1 + x_t ≥ d_t. But how do we track the ending inventory?

Let me think about variables. Let's define:

- x_t: order quantity in period t (t=1 to 4)
- i_t: inventory at the end of period t (after meeting demand)

Then, the inventory at the end of period t is i_t = i_{t-1} + x_t - d_t. For t=1, i_0 is the initial inventory, which is 29.

So, the constraints are:

For each t from 1 to 4:

i_{t} = i_{t-1} + x_t - d_t

But since i_t must be ≥ 0, we have:

i_{t-1} + x_t - d_t ≥ 0 → i_{t-1} + x_t ≥ d_t

But since i_t is the ending inventory, which is non-negative, we can model this as:

i_t ≥ 0 for all t.

But how do we model this in PuLP? Well, the variables i_t and x_t are decision variables. However, since i_t is dependent on previous variables, we need to express this as constraints.

So, for each period t (from 1 to 4), the constraint is:

i_{t-1} + x_t - d_t = i_t

But since i_0 is given as 29, we can start with that.

So, the variables are x_t (for t=1 to 4) and i_t (for t=0 to 4). Wait, but i_0 is fixed as 29. So, maybe we can model i_0 as a fixed variable, and then for each t from 1 to 4, we have the equation i_t = i_{t-1} + x_t - d_t.

But in PuLP, we can model this with constraints. Let me think about how to structure this.

The objective function is to minimize the total cost, which includes ordering costs and holding costs. The ordering cost is unit_order_cost * sum(x_t for t in 1..4). The holding cost is holding_cost * sum(i_t for t in 1..4). Wait, because the holding cost is per unit of inventory at the end of each period. So, the total cost is (unit_order_cost * sum(x_t)) + (holding_cost * sum(i_t)).

So, the objective is to minimize that.

Now, the constraints:

For each t in 1..4:

i_t = i_{t-1} + x_t - d_t

But since i_0 is 29, we can model this as:

i_0 = 29

Then, for t=1:

i_1 = i_0 + x_1 - d_1

t=2:

i_2 = i_1 + x_2 - d_2

and so on.

But in PuLP, we can model these as equality constraints. However, since i_t is a variable, we need to define them.

So, the variables are x_1, x_2, x_3, x_4, and i_0, i_1, i_2, i_3, i_4. Wait, but i_0 is fixed. So, maybe we can fix i_0 as 29, and then model the other i_t variables.

Alternatively, since i_0 is known, we can express the constraints for i_1, i_2, etc., in terms of previous i's.

So, the steps for the code:

1. Import pulp and os.

2. Define the periods, initial inventory, demands, etc.

3. Create the problem.

4. Define variables:

   - x_t for each period (t from 1 to 4)
   - i_t for each period (t from 0 to 4). But i_0 is fixed as 29.

Wait, but in PuLP, variables can be created with indices. Let me think about how to structure this.

Alternatively, since the problem is small, we can create variables for each x and i.

So, for x, we can have x = [x1, x2, x3, x4]

For i, we can have i = [i0, i1, i2, i3, i4], where i0 is fixed at 29.

But in PuLP, variables can be created as a list. So, perhaps:

x = [pulp.LpVariable(f'x_{t}', lowBound=0) for t in range(1, periods+1)]

i = [pulp.LpVariable(f'i_{t}', lowBound=0) for t in range(0, periods+1)]

But then, for i[0], we need to set its value to 29. Wait, but in PuLP, variables can't be fixed unless we set their value. Alternatively, we can model the constraints that i_0 = 29. But since i_0 is not a decision variable, maybe we can just fix it.

Wait, but in PuLP, variables are created with lower and upper bounds. So, perhaps we can create i_0 as a variable with a fixed value. But that's not necessary. Since i_0 is known, we can model the constraints for i_1, i_2, etc., in terms of i_0.

So, for each t from 1 to 4:

i[t] = i[t-1] + x[t] - demand[t-1]

Wait, the demand for period 1 is 51, which is the first element in the demand list. So, for t in 1..4, the demand is demand[t-1].

So, the constraints would be:

for t in 1 to 4:

i[t] = i[t-1] + x[t] - demand[t-1]

But since i[t] must be ≥ 0, we can add that as a constraint.

Wait, but the equation i[t] = i[t-1] + x[t] - demand[t-1] is an equality constraint. However, since i[t] can't be negative, we need to ensure that i[t] ≥ 0. So, the constraints are:

i[t] = i[t-1] + x[t] - demand[t-1] for each t in 1..4

and i[t] ≥ 0 for each t in 0..4.

Wait, but i[0] is fixed at 29, so that's already
