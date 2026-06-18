<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has 6 periods. We have initial inventory of 15, and demands for each period. The goal is to decide when to place orders (Q_t) and track inventory (I_t), with a binary variable Y_t indicating if an order is placed in period t. The fixed order cost is 68, unit order cost is 4, holding cost is 3. We need to use Big-M method with M=261 to link the order quantity and the binary variable.

First, I need to define the decision variables. Let's think:

- Q_t: the quantity ordered in period t. This should be a non-negative variable.
- I_t: the inventory at the end of period t. Also non-negative.
- Y_t: binary variable indicating if an order is placed in period t (1 if ordered, 0 otherwise).

The objective is to minimize the total cost, which includes fixed order costs (sum over Y_t * fixed_order_cost), unit order costs (sum over Q_t * unit_order_cost), and holding costs (sum over I_t * holding_cost).

Constraints:

1. Inventory balance: For each period t, the inventory at the end of the period is equal to the previous inventory minus the demand plus the order quantity. But since the initial inventory is given, we need to handle the first period correctly. Let me think: For period 1, initial inventory is 15. Then, after meeting demand, inventory is 15 - demand[0] + Q_1. Wait, but the inventory after period t is I_t. So for each period t from 1 to T:

I_0 = initial_inventory (15)
For t in 1 to T:
I_{t} = I_{t-1} - demand[t-1] + Q_t

But since the problem uses 0-based or 1-based indexing? The demand is given as a list of 6 elements, and periods are 6. So for period 1 to 6, the demand is demand[0] to demand[5].

So the inventory balance constraint for each period t (from 1 to 6) would be:

I_t = I_{t-1} - demand[t-1] + Q_t

But since I_t must be non-negative, we need to ensure that I_t >= 0.

But how to model this in PuLP? Let's think about the variables. Let's index the periods from 0 to 5 (since Python is 0-based). Wait, the problem says T=6 periods. So maybe the periods are 0 to 5. Let me adjust.

Let me define the periods as 0 to 5 (since the demand list is 6 elements). Then, initial inventory is I_0 = 15. Then, for each period t in 0 to 5:

I_{t} = I_{t-1} - demand[t] + Q_t ?

Wait, no. Wait, the initial inventory is before period 1. Let me think again. Let's say the periods are 1 to T. For period 1, the initial inventory is 15. Then, after meeting the demand of period 1, the inventory is I_1 = initial_inventory - demand[0] + Q_1. Then for period 2, I_2 = I_1 - demand[1] + Q_2, etc.

But in code, it's easier to index from 0. Let me adjust. Let's say periods are 0 to 5 (total 6 periods). The initial inventory is I_prev = 15. For each period t in 0 to 5:

I_t = I_prev - demand[t] + Q_t

But I_t must be >= 0. Then, I_prev for the next period is I_t.

So the constraints would be:

For each t in 0 to 5:

I_t = I_prev - demand[t] + Q_t

But I_prev is the inventory before period t. Wait, maybe I should model the inventory after the order is placed. Let me think again.

The inventory at the end of period t (I_t) is equal to the inventory at the start of the period (I_prev) minus the demand for the period plus the order quantity Q_t. So:

I_t = I_prev - demand[t] + Q_t

But I_prev is the inventory at the start of period t. For the first period, I_prev is the initial inventory (15). For subsequent periods, I_prev is I_{t-1}.

So the constraints are:

For t in 0 to 5:

I_t = I_prev - demand[t] + Q_t

But how to model this in PuLP? Since I_prev for period t is I_{t-1} for t >=1, and for t=0, it's initial_inventory.

So for each t in 0 to 5:

I_t = (initial_inventory if t == 0 else I_{t-1}) - demand[t] + Q_t

But in PuLP, we can model this as:

For each t in 0 to 5:

I_t + demand[t] - Q_t = I_prev

But I_prev is I_{t-1} for t >=1, and initial_inventory for t=0.

So for t=0:

I_0 + demand[0] - Q_0 = initial_inventory ?

Wait, no. Let me re-express the equation. The inventory after the order is placed (I_t) is equal to the inventory before the order (I_prev) minus the demand plus the order quantity. So:

I_t = I_prev - demand[t] + Q_t

Rearranged:

I_t + demand[t] - Q_t = I_prev

So for t=0, I_prev is initial_inventory. So:

I_0 + demand[0] - Q_0 = initial_inventory ?

Wait, that would be:

I_0 = initial_inventory - demand[0] + Q_0 ?

No, that's not right. Let me re-derive:

Original equation:

I_t = I_prev - demand[t] + Q_t

So rearranged:

I_t + demand[t] - Q_t = I_prev

So for t=0, I_prev is initial_inventory. So:

I_0 + demand[0] - Q_0 = initial_inventory ?

Wait, that would mean:

I_0 = initial_inventory - demand[0] + Q_0 ?

No, that's not correct. Let me think again. Let's take t=0:

I_0 = initial_inventory - demand[0] + Q_0 ?

Yes. Because the initial inventory is before the first period. Then, during period 0, the demand is met by subtracting from the initial inventory, and adding the order quantity. So the inventory after period 0 is I_0 = initial_inventory - demand[0] + Q_0.

But according to the equation I_t + demand[t] - Q_t = I_prev, for t=0, I_prev is initial_inventory. So:

I_0 + demand[0] - Q_0 = initial_inventory

Which rearranged gives:

I_0 = initial_inventory - demand[0] + Q_0

Which is correct. So that's the equation for t=0.

For t >=1, I_prev is I_{t-1}.

So for each t in 0 to 5:

I_t + demand[t] - Q_t = I_prev, where I_prev is initial_inventory if t=0, else I_{t-1}.

So in PuLP, for each t, we can write:

I_t + demand[t] - Q_t == I_prev

But how to model this in code? Let's think about the variables. Let's create variables for I_t and Q_t for each period t in 0 to 5.

So for each t in 0 to 5:

I_t = inventory after period t.

Q_t = quantity ordered in period t.

Y_t = binary variable indicating if an order is placed in period t (1 if ordered, 0 otherwise).

Now, the Big-M method is used to link Q_t and Y_t. The idea is that if Y_t is 1, then Q_t can be any non-negative value (but we need to have Q_t >=0). However, if Y_t is 0, then Q_t must be 0. So the constraints would be:

Q_t >= 0

Q_t <= M * Y_t

But since M is given as 261, which is the maximum possible order quantity. Wait, but the problem says to use Big-M links with M=261. So the constraints are:

Q_t >= 0

Q_t <= M * Y_t

But since M is 261, which is larger than the maximum possible order quantity (since the maximum demand is 54, and the initial inventory is 15, but maybe the maximum order is higher? Well, the problem says to use M=261, so we can proceed with that.

So the constraints for Q_t and Y_t are:

Q_t >= 0

Q_t <= big_m * Y_t

But since Y_t is binary, this ensures that if Y_t is 0, Q_t must be 0. If Y_t is 1, Q_t can be any value up to big_m.

Now, the objective function is to minimize:

sum (fixed_order_cost * Y_t) + sum (unit_order_cost * Q_t) + sum (holding
