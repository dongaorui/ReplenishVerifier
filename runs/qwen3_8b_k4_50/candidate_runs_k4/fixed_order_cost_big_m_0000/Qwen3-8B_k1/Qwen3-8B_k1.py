<think>
Okay, let's tackle this inventory replenishment problem. The user wants a Python program using PuLP. Let me start by understanding the problem.

So, the problem involves ordering over multiple periods. Each order has a variable unit cost and a fixed activation cost. The goal is to minimize the total cost, which includes ordering, holding, and fixed costs. The initial inventory is 7, and there are 5 periods with specific demands. The unit order cost is 4, holding cost is 1, fixed order cost is 49, and the Big-M value is 113.

First, I need to define the decision variables. The main ones are the order quantities and the binary variables indicating whether an order is placed in each period. Let me think: for each period, we need to decide how much to order (let's call it Q) and whether to place an order (binary variable Y). Also, the inventory level after each period is important.

Wait, the problem mentions that the fixed activation cost is incurred if an order is placed. So, the fixed cost is only added when Y is 1. The variable cost is unit_order_cost multiplied by the quantity ordered. The holding cost is per unit held in inventory, which depends on the ending inventory each period.

Let me outline the variables:

- For each period t (from 1 to 5), let Y_t be a binary variable (0 or 1) indicating if an order is placed in period t.
- Let Q_t be the quantity ordered in period t. Since we can't order negative, Q_t ≥ 0.
- Let I_t be the inventory at the end of period t. This must be non-negative.

The constraints would be:

1. Inventory balance: For each period t, the inventory at the start (I_{t-1}) minus demand (d_t) plus the order quantity (Q_t) equals the ending inventory I_t. But since initial inventory is given, for t=1, I_0 is initial_inventory. So, for each t, I_{t} = I_{t-1} - d_t + Q_t. But since I_t can't be negative, we need to ensure that I_t ≥ 0.

Wait, but the problem says that the order quantity is linked to the binary variables. So, the fixed cost is only incurred if Y_t is 1. So, the fixed cost is fixed_order_cost * Y_t. The variable cost is unit_order_cost * Q_t. The holding cost is holding_cost * I_t. So the total cost is sum over all periods of (fixed cost + variable cost + holding cost).

But how to link Q_t and Y_t? The fixed cost is only incurred if Y_t is 1. However, the problem says that the fixed activation cost is incurred when an order is placed. So, if Y_t is 1, then Q_t can be any non-negative value, but if Y_t is 0, then Q_t must be 0. Wait, no. Wait, the problem says that ordering in a period incurs both variable and fixed cost. So, if you place an order (Y_t=1), you have to pay the fixed cost and the variable cost based on Q_t. But if you don't place an order (Y_t=0), then Q_t must be 0. So the constraints are Q_t ≤ M * Y_t, where M is the Big-M value. But since the Big-M is given as 113, perhaps that's the maximum possible order quantity. Wait, but the Big-M is used in the constraints to model the binary variables. So, the standard approach is to have Q_t ≤ M * Y_t, ensuring that if Y_t is 0, Q_t must be 0. But the Big-M value here is 113. So, the maximum possible order quantity is 113? Or is it a value that's large enough to cover any possible order quantity?

In this problem, the Big-M is given as 113. So, the constraints would be Q_t ≤ big_m * Y_t. That way, when Y_t is 0, Q_t must be 0. But what's the maximum possible Q_t? Well, the demand for each period is up to 29, but since we can order in multiple periods, maybe the Big-M is set to a value that's larger than the maximum possible order quantity. However, the problem says to use the given Big-M value of 113. So, we'll use that.

So, the variables are:

- Y_t: binary variables for each period.
- Q_t: non-negative variables for each period.
- I_t: non-negative variables for each period.

Now, the objective function is to minimize the sum of:

- Fixed costs: sum over t (fixed_order_cost * Y_t)
- Variable costs: sum over t (unit_order_cost * Q_t)
- Holding costs: sum over t (holding_cost * I_t)

So, the total cost is fixed_order_cost * sum(Y_t) + unit_order_cost * sum(Q_t) + holding_cost * sum(I_t).

Now, the constraints:

For each period t:

1. Inventory balance: I_{t} = I_{t-1} - demand[t] + Q_t. But since I_t can't be negative, we need to ensure that I_{t} ≥ 0. However, since Q_t is non-negative, and I_{t-1} is the previous inventory, this equation should hold. But since we can't have negative inventory, we need to make sure that I_{t} ≥ 0. Wait, but the equation is I_{t} = I_{t-1} - demand[t] + Q_t. So, if I_{t-1} - demand[t] is negative, then Q_t must be sufficient to cover that. But since Q_t is non-negative, the equation would ensure that I_t is non-negative. Wait, no. Suppose I_{t-1} is 5, demand is 10, and Q_t is 0. Then I_t would be 5 -10 +0 = -5, which is invalid. So, we need to ensure that I_t ≥ 0. Therefore, the constraint is I_{t} ≥ 0. But how to model that?

Wait, the inventory balance equation is:

I_t = I_{t-1} - demand[t] + Q_t

But since I_t can't be negative, we need to have I_t ≥ 0. So, for each t, I_t ≥ 0.

But how to model that? Well, the equation is already part of the model. However, since I_t is a variable, we need to ensure that it's non-negative. So, the constraints are:

For each t in 1..T:

I_t = I_{t-1} - demand[t] + Q_t

But since I_0 is the initial inventory (7), we can model this with the variables.

So, for t=1:

I_1 = I_0 - demand[0] + Q_1

For t=2:

I_2 = I_1 - demand[1] + Q_2

And so on.

But in PuLP, we can model these as equations. However, since I_t is a variable, we need to express this as a constraint for each period.

So, for each period t (starting from 1 to periods), we have:

I_t = I_{t-1} - demand[t-1] + Q_t

Wait, the demand is given as a list, so for period 1, the demand is demand[0], etc.

So, the initial inventory is I_0 = 7.

Now, the constraints:

For each t in 1 to periods:

I_t = I_{t-1} - demand[t-1] + Q_t

But since I_0 is known, we can model this as:

For t=1:

I_1 = 7 - demand[0] + Q_1

For t=2:

I_2 = I_1 - demand[1] + Q_2

And so on.

But in PuLP, we can model these as equations. However, since I_t is a variable, we need to create variables for each I_t.

So, variables:

- Y: list of binary variables for each period.
- Q: list of non-negative variables for each period.
- I: list of non-negative variables for each period.

Now, the constraints:

1. For each period t, I_t = I_{t-1} - demand[t-1] + Q_t. But since I_0 is 7, we can model this as:

For t in 1 to periods:

I[t] = I[t-1] - demand[t-1] + Q[t]

But in PuLP, we can model this as:

for t in range(1, periods+1):

    prob += I[t] == I[t-1] - demand[t-1] + Q[t]

But wait, in Python, the indices need to be handled properly. Let's say periods is 5, then t ranges from 1 to 5. But in the code, the variables are probably indexed from 0 to 4. Wait, perhaps it's better to index from 0 to periods-1. Let me think.

Alternatively, perhaps the code can use 0-based indexing. Let me adjust.

Let me think of the periods as 0 to 4 (since there are 5 periods). Then, initial inventory is I_0 = 7. For each period t (0 to 4), the demand is demand[t]. Then,
