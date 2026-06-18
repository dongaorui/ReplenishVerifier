<think>
Okay, let's tackle this inventory replenishment problem. The user wants a Python program using PuLP. Let me start by understanding the problem.

The problem involves ordering in each period with both a variable unit cost and a fixed activation cost. The goal is to minimize total costs, which include ordering, holding, and fixed costs. The initial inventory is 15, and there are 6 periods with specific demands. The unit order cost is 4, holding cost is 2, fixed order cost is 29, and the Big-M value is 291.

First, I need to define the decision variables. The main ones are the order quantities and the binary variables indicating whether an order is placed in each period. Let me think: for each period, we need to decide how much to order (let's call it Q) and whether to place an order (binary variable Y). Also, we need to track the inventory levels over time.

So, variables:
- Q_t: quantity ordered in period t (continuous, non-negative)
- Y_t: binary variable indicating if an order is placed in period t (1 if ordered, 0 otherwise)
- I_t: inventory at the end of period t (continuous, non-negative)

Constraints:
1. Inventory balance: For each period t, the inventory at the end of the period is the previous inventory minus demand plus the order quantity. So I_0 = initial_inventory. For t >=1, I_t = I_{t-1} - demand[t] + Q_t. But since demand is given as a list, maybe index from 0 to 5 for 6 periods. Wait, the problem says periods are 6, so indexes 0-5.

But wait, the initial inventory is 15. So I_0 = 15. Then for each period t (from 1 to 6?), but the problem has 6 periods. Wait, the demand list has 6 elements, so periods are 0 to 5. So for t in 0 to 5, but initial inventory is before period 0. Let me clarify:

Let me index periods from 0 to 5 (since there are 6 periods). The initial inventory is before period 0. So for each period t (0 to 5), the inventory after meeting demand is I_t. Wait, maybe the inventory after period t is I_t. So the initial inventory is I_{-1} = 15. Then for each period t (0 to 5), the inventory after meeting demand is I_t = I_{t-1} - demand[t] + Q_t. But Q_t can't be negative, so Q_t >= 0. Also, the order quantity can't be negative. Also, the fixed cost is incurred only if Y_t is 1. So the fixed cost is fixed_order_cost * Y_t for each period.

The objective is to minimize total cost: sum over all periods of (unit_order_cost * Q_t + holding_cost * I_t) + sum over all periods of fixed_order_cost * Y_t.

But wait, the holding cost is applied to the inventory at the end of the period. So for each period, the holding cost is holding_cost * I_t. Also, the unit order cost is per unit ordered, so unit_order_cost * Q_t.

But there's a fixed cost if an order is placed. So the total cost is sum (unit_order_cost * Q_t) + sum (holding_cost * I_t) + sum (fixed_order_cost * Y_t).

Now, the constraints:

For each period t (0 to 5), the inventory after the period must be >=0. Wait, no. The inventory after the period is I_t, which is the ending inventory. But if the demand is not met, that would be negative. So we need to ensure that I_t >= 0. Wait, but the problem says that ordering is done to meet demand. So perhaps the order quantity Q_t must be such that I_{t-1} - demand[t] + Q_t >= 0. Wait, no. Because the inventory after the period is I_t = I_{t-1} - demand[t] + Q_t. But if I_t is negative, that would imply that the demand wasn't met. So we need to ensure that I_t >= 0. Wait, but maybe the problem allows for backorders? The problem statement doesn't mention backorders, so I think we need to assume that the inventory after the period is non-negative. So for each t, I_t >= 0.

But how to model that. So the constraints are:

For t in 0 to 5:

I_t = I_{t-1} - demand[t] + Q_t

But I_0 is initial_inventory, which is 15. Wait, no. Let me think again. Let's index the periods as 0 to 5. The initial inventory is before period 0. So for period 0, the inventory after meeting demand is I_0 = initial_inventory - demand[0] + Q_0. Then for period 1, I_1 = I_0 - demand[1] + Q_1, etc. So the initial inventory is I_{-1} = 15. Then for t=0 to 5:

I_t = I_{t-1} - demand[t] + Q_t

But I_{t} must be >=0 for all t. Wait, but if the demand is not met, then I_t would be negative. So we need to ensure that I_t >= 0 for all t. So that's a constraint.

But how to model this. So for each t, I_t >= 0.

Now, the binary variables Y_t indicate whether an order is placed in period t. But how does that relate to Q_t? The problem says that ordering in a period incurs both variable unit cost and fixed activation cost. So the fixed cost is only incurred if an order is placed. So Y_t is 1 if Q_t > 0, but maybe the model allows for Q_t to be zero even if Y_t is 1? Or is Y_t linked to Q_t such that if Y_t is 1, then Q_t can be any non-negative value, but if Y_t is 0, then Q_t must be zero?

Wait, the problem says "ordering in a period incurs both a variable unit cost and a fixed activation cost". So the fixed cost is incurred if an order is placed, regardless of the quantity. So the fixed cost is fixed_order_cost * Y_t, where Y_t is 1 if an order is placed. But how to link Y_t to Q_t. Because if you place an order (Y_t=1), you can have Q_t >=0. But if you don't place an order (Y_t=0), then Q_t must be zero. So the constraint is Q_t <= M * Y_t, where M is a big enough number. But the problem gives a Big-M value of 291. So the Big-M is 291. So for each period t, Q_t <= big_m * Y_t. Also, since Q_t can't be negative, we have Q_t >= 0. So that's the link between Q_t and Y_t.

So the constraints are:

For each t in 0 to 5:

Q_t >= 0

Q_t <= big_m * Y_t

Y_t is binary.

Now, the inventory balance equations:

I_0 = initial_inventory - demand[0] + Q_0

Wait, no. Let me think again. The initial inventory is before period 0. So for period 0, the inventory after the period is I_0 = initial_inventory - demand[0] + Q_0. Then for period 1, I_1 = I_0 - demand[1] + Q_1. And so on.

So the inventory balance equations are:

For t in 0 to 5:

I_t = I_{t-1} - demand[t] + Q_t

But I_{-1} = initial_inventory.

So for t=0:

I_0 = initial_inventory - demand[0] + Q_0

For t=1:

I_1 = I_0 - demand[1] + Q_1

and so on.

But how to model this in PuLP. We can create variables for I_t for each t from 0 to 5. Then, for each t, the equation is I_t = I_{t-1} - demand[t] + Q_t. But since I_{t} is a variable, we can express this as:

I_t - I_{t-1} + demand[t] - Q_t = 0

But for t=0, I_{-1} is initial_inventory. So for t=0, the equation is I_0 = initial_inventory - demand[0] + Q_0. Which can be written as I_0 - initial_inventory + demand[0] - Q_0 = 0.

So for each t in 0 to 5, we have:

If t == 0:

I_0 - initial_inventory + demand[0] - Q_0 = 0

Else:

I_t - I_{t-1} + demand[t] - Q_t = 0

But in PuLP, we can model this with constraints. So for each t, we can create a constraint that links I_t, I_{t-1}, demand[t], and Q_t.

Additionally, we need to ensure that I_t >= 0 for all t.

Now, the objective function is:

Total cost = sum (unit_order_cost * Q_t) + sum (holding
