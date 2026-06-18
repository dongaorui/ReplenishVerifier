<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem. Let me start by understanding the problem details.

The problem has 3 periods. Initial inventory is 12, and demands are 23, 24, 29. We need to decide on order quantities Q_t each period, track inventory I_t, and use binary variables Y_t to indicate if an order is placed. The fixed order cost is 24, unit order cost is 2, holding cost is 2. The Big-M method is used with M=76.

First, I need to set up the PuLP model. Let me recall how to structure this. The model will have variables for Q_t, I_t, and Y_t. The objective is to minimize the sum of unit order costs, holding costs, and fixed order costs. 

Wait, the fixed order cost is incurred if Y_t is 1. So the fixed cost is fixed_order_cost * Y_t for each period. The unit order cost is unit_order_cost * Q_t. Holding cost is holding_cost * (I_t - demand_t) if I_t is positive? Or maybe it's holding_cost * I_t? Wait, the problem says "holding cost 2", so probably it's the inventory at the end of the period. Let me check the problem statement again.

The problem says "minimize unit order cost 2, holding cost 2, and fixed cost 24." So the objective is sum over all periods of (unit_order_cost * Q_t) + (holding_cost * I_t) + (fixed_order_cost * Y_t). Wait, but the fixed cost is per order, so if you order in period t, you pay fixed_order_cost. So Y_t is 1 if you order in period t, else 0. So the fixed cost is fixed_order_cost * Y_t for each t.

Now, the constraints. The inventory at the beginning of period t is initial_inventory if t=1, else I_{t-1} (inventory from previous period). Then, inventory after order and before demand is I_{t-1} + Q_t. Then subtract demand to get I_t. So the constraint is I_t = I_{t-1} + Q_t - demand_t. But since I_t can't be negative, we need to ensure that I_t >= 0. Wait, but the problem says "inventory I_t", so maybe I_t is the inventory after demand is met. So the constraint is I_t = I_{t-1} + Q_t - demand_t. But since inventory can't be negative, we need to have I_t >= 0. However, the problem might allow for negative inventory if there's a shortage, but the problem statement doesn't mention that. So I think we need to ensure that I_t >= 0 for all t.

But how to model this with the variables. Also, the Big-M method is used to link Q_t and Y_t. The Big-M method is used to enforce that if Y_t is 1, then Q_t >= 0 (but since Q_t is an order quantity, it's non-negative anyway). Wait, maybe the Big-M is used to link the fixed cost with the order quantity. For example, the fixed cost is only incurred if Q_t > 0. But since Y_t is a binary variable, perhaps the model uses Y_t to indicate whether an order is placed. So the Big-M constraints would be Q_t <= M * Y_t, and Q_t >= 0. Wait, but if Y_t is 1, then Q_t can be any value, but if Y_t is 0, then Q_t must be 0. So the constraints would be Q_t <= M * Y_t and Q_t >= 0. But since M is given as 76, which is larger than the maximum possible order quantity. Wait, the maximum possible order quantity would be the sum of demands, but maybe the M is chosen to be large enough. So the Big-M constraints would be Q_t <= M * Y_t and Q_t >= 0. But since Q_t is non-negative, maybe the first constraint is Q_t <= M * Y_t. Also, we need to ensure that if Y_t is 1, then Q_t can be positive. But since Y_t is binary, the constraints would be Q_t >= 0 and Q_t <= M * Y_t. So that if Y_t is 0, Q_t must be 0. But maybe the problem requires that if you order (Y_t=1), then Q_t can be any non-negative value, but if Y_t=0, then Q_t must be 0. So the constraints are Q_t >= 0, Q_t <= M * Y_t. 

So the variables are:

- Q_t: order quantity in period t, non-negative integer? Or real? The problem doesn't specify, but since it's an optimization problem, maybe they can be real numbers. But the problem says "order Q_t", which could be any non-negative value. However, the problem might require integer values, but the parameters don't specify. Since the problem doesn't mention integer variables, I'll assume they are continuous.

But the problem says "fixed_order_cost_big_m_0007" and the parameters include M=76. So the Big-M method is used to link Q_t and Y_t. So the constraints would be:

Q_t <= M * Y_t

and 

Q_t >= 0

But since Y_t is binary, this ensures that if Y_t is 1, Q_t can be up to M, but if Y_t is 0, Q_t must be 0. Wait, but if Y_t is 0, then Q_t must be 0. So the constraints are:

Q_t >= 0

Q_t <= M * Y_t

But since Y_t is binary, this would force Q_t to be zero when Y_t is zero. However, if Y_t is 1, Q_t can be any value up to M. But the problem may require that if Y_t is 1, then Q_t can be positive. So the constraints are correct.

Now, the inventory constraints. For each period t, the inventory after order and before demand is I_{t-1} + Q_t. Then, after subtracting demand, it's I_t. So:

I_t = I_{t-1} + Q_t - demand_t

But since I_t can't be negative, we need to have I_t >= 0. Wait, but the problem says "inventory I_t", which is the inventory after demand is met. So if I_{t-1} + Q_t < demand_t, then I_t would be negative, which is not allowed. Therefore, we need to ensure that I_{t-1} + Q_t >= demand_t. Wait, no. Because the inventory after order and before demand is I_{t-1} + Q_t. Then, after meeting demand, the inventory is I_{t-1} + Q_t - demand_t. But if this is negative, that would imply that the demand is not met. However, the problem doesn't mention shortages, so perhaps we need to ensure that I_{t-1} + Q_t >= demand_t. Therefore, the constraint is:

I_{t-1} + Q_t >= demand_t

But then, I_t = I_{t-1} + Q_t - demand_t >= 0.

Wait, but the problem may not require that. Maybe the problem allows for negative inventory, but that's not typical. So perhaps the correct constraint is that I_t >= 0. But how to model that. Let me think again.

The inventory after demand is I_t = I_{t-1} + Q_t - demand_t. So for this to be non-negative, we need I_{t-1} + Q_t >= demand_t. Therefore, the constraint is I_{t-1} + Q_t >= demand_t. But since I_t is the inventory after demand, it's possible that I_t is negative if the demand is not met. However, the problem may not allow that. So perhaps the correct constraint is I_t >= 0. But how to model that. Let me check the problem statement again.

The problem says "inventory I_t", but doesn't specify whether it's the inventory before or after demand. However, in typical inventory models, the inventory after demand is considered. So the constraint would be I_t = I_{t-1} + Q_t - demand_t, and I_t >= 0. Therefore, the constraint is I_{t-1} + Q_t - demand_t >= 0. Which can be written as I_{t-1} + Q_t >= demand_t. So that's the constraint.

So for each period t, we have:

I_t = I_{t-1} + Q_t - demand_t

and 

I_t >= 0

But since I_t is the inventory after demand, it's possible that I_t is zero or positive. Therefore, the constraint is I_t >= 0.

But how to model this in PuLP. Let me think about the variables. The initial inventory is 12, so for t=1, I_0 = 12. Then, for t=1, I_1 = I_0 + Q_1 - demand_1. For t=2, I_2 = I_1 + Q_2 - demand_2. And so on.

So the variables are:

- Q_t for t in 1..T (periods)
- I_t for t in 0..T (since I_0
