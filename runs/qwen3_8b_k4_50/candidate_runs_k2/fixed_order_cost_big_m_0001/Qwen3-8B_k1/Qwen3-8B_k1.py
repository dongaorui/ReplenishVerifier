<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem involves ordering in each period with both a variable unit cost and a fixed activation cost. The goal is to minimize the total cost, which includes ordering costs, holding costs, and fixed costs. The model needs binary variables to indicate if an order is placed in a period. Also, there's a Big-M value provided, which I should use in the constraints.

First, I'll outline the parameters given. The initial inventory is 15. There are 6 periods with specific demands. The unit order cost is 4, holding cost is 2, fixed order cost is 29, and Big-M is 291.

The decision variables I need are:
- Order quantity variables (let's say Q_t for each period t)
- Binary variables (let's say Y_t) indicating if an order is placed in period t.

The constraints will include:
1. Inventory balance for each period. The inventory at the start of the period plus the order quantity minus demand equals the inventory at the end of the period.
2. The order quantity must be non-negative and linked to the binary variable via the Big-M method. For example, Q_t <= M * Y_t, and Q_t >= 0. Since Y_t is binary, this ensures that if Y_t is 0, Q_t must be 0, and if Y_t is 1, Q_t can be any value up to M.
3. The initial inventory is given, so the first period's inventory starts at 15.
4. Non-negativity of all variables.

The objective function is the sum of:
- Unit order costs for each period (unit_order_cost * Q_t)
- Fixed order costs for each period (fixed_order_cost * Y_t)
- Holding costs for each period (holding_cost * ending_inventory_t)

Wait, the holding cost is based on the ending inventory. So for each period, the ending inventory is the previous ending inventory plus Q_t minus demand. So I need to track the inventory over time.

Let me think about how to model the inventory. Let's define I_t as the inventory at the end of period t. Then, for each period t:

I_0 = initial_inventory (15)
For t >= 1:
I_t = I_{t-1} + Q_t - demand[t-1] (since demand is for period t, maybe indexes need to be adjusted)

Wait, the demand array is given as [55, 51, 27, 60, 59, 39], which are for periods 1 to 6. So for period 1, demand is 55. So the inventory balance equation for period t (starting from 1 to 6) would be:

I_{t} = I_{t-1} + Q_t - demand[t-1]

But I need to make sure that the inventory can't be negative. Wait, the problem doesn't mention any constraints on negative inventory, but in practice, it's possible. However, the problem might assume that the inventory is non-negative. Wait, the problem statement doesn't specify, but since it's an optimization problem, maybe we need to ensure that the inventory doesn't go negative. Wait, the problem says "replenishment", so perhaps the inventory can't be negative. So I need to add constraints that I_t >= 0 for all t.

Wait, but the problem doesn't mention that. Let me check the problem statement again. The problem says "ordering in a period incurs both a variable unit cost and a fixed activation cost." It doesn't mention any constraints on inventory levels. However, in real-world scenarios, you can't have negative inventory. But since the problem doesn't specify, maybe we don't need to include that. However, the problem might have that as an implicit constraint. Hmm. But the problem's parameters include a Big-M value, which is used for the constraints linking order quantities to the binary variables. So maybe the inventory can be negative, but that's not specified. Wait, but the problem says "replenishment", so perhaps the model should ensure that the inventory is non-negative. Let me check the problem again.

The problem says "the formulation should include binary variables that indicate whether an order is placed and constraints linking order quantities to those binaries." So the main constraints are the ones linking Q_t and Y_t. The inventory balance is part of the model. However, the problem doesn't mention inventory constraints. So perhaps the model allows negative inventory, but that's not typical. However, since the problem doesn't specify, maybe we can proceed without that constraint. But I need to make sure that the model is correct. Alternatively, maybe the problem expects that the inventory is non-negative. Let me think. If the model allows negative inventory, then the problem might have a different solution. But since the problem doesn't mention it, perhaps it's not required. However, in practice, it's better to include that. But since the problem doesn't specify, maybe it's not necessary. Hmm. Well, the problem's parameters include a Big-M value, which is 291. So perhaps the constraints are designed to handle the order quantities properly.

So, moving forward, the main constraints are:

For each period t (from 1 to 6):

I_t = I_{t-1} + Q_t - demand[t-1]

But I_0 is initial_inventory (15). So for t=1, I_1 = 15 + Q_1 - demand[0] (which is 55). Then for t=2, I_2 = I_1 + Q_2 - demand[1], etc.

But how to model this in PuLP? We can create variables for I_t. However, since the problem is over 6 periods, we can model this with variables for each period's ending inventory.

But since the problem is about minimizing cost, the objective function is:

Total cost = sum over all periods (unit_order_cost * Q_t) + sum over all periods (fixed_order_cost * Y_t) + sum over all periods (holding_cost * I_t)

Wait, the holding cost is per unit of inventory at the end of the period. So yes, that's correct.

Now, the constraints:

For each period t (from 1 to 6):

I_t = I_{t-1} + Q_t - demand[t-1]

But since I_0 is given as 15, we can model this as:

I_0 = 15

For t in 1 to 6:

I_t = I_{t-1} + Q_t - demand[t-1]

But in PuLP, we need to express these as constraints. So for each t, we can create a constraint that I_t - I_{t-1} - Q_t + demand[t-1] = 0.

But how to model the variables. Let's think about the variables:

- Q_t: order quantity in period t. This is a continuous variable >=0.

- Y_t: binary variable indicating if an order is placed in period t (1 if ordered, 0 otherwise).

- I_t: inventory at the end of period t. This is a continuous variable >=0 (assuming we need to prevent negative inventory).

Wait, but the problem doesn't specify that. However, if we don't include that, then the model might allow negative inventory, which could lead to lower costs. But since the problem is about replenishment, it's more realistic to assume that inventory can't be negative. So perhaps we should add constraints that I_t >= 0 for all t.

But again, the problem doesn't mention this. However, given that the problem includes a Big-M value, which is used for the constraints linking Q_t and Y_t, perhaps the model is designed to handle that. Let me proceed with the assumption that inventory can't be negative. So I'll add constraints that I_t >= 0 for all t.

Now, the constraints linking Q_t and Y_t. For each period t:

Q_t <= M * Y_t (where M is the Big-M value given as 291)

Also, since Q_t can't be negative, we have Q_t >= 0.

But since Y_t is binary, this ensures that if Y_t is 0, Q_t must be 0. If Y_t is 1, Q_t can be any value up to M. However, since the Big-M is 291, which is larger than the maximum possible order quantity (since the maximum demand is 60, and with 6 periods, the maximum order could be up to 60*6=360, but the Big-M is 291, which is less than that. Wait, that's a problem. Wait, the Big-M value is given as 291. But if the maximum possible order quantity is higher than that, then the constraint Q_t <= M * Y_t would not be sufficient. Wait, but the problem says to use the given Big-M value. So perhaps the Big-M is chosen as a value that is sufficiently large to cover all possible order quantities. However, in this case, the maximum possible order quantity could be up to the sum of all demands, but that's not clear. Alternatively, maybe the Big-M is set to a value that is larger than the maximum possible order quantity. Let me check the parameters again.

The Big-M is given as 291. Let's see the demands: the maximum demand is 60. So if the order quantity in a period can be up to the sum of all demands, but that's not necessarily the case. However,
