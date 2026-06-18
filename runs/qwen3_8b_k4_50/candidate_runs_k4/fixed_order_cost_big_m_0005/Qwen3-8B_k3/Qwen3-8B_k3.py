<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The firm has a 4-period horizon. They start with 20 units of inventory. Each period, there's a demand, and they need to decide how much to order. There's a setup cost each time they place an order, and also unit ordering and holding costs. The goal is to minimize the total cost, which includes ordering, holding, and fixed setup costs.

The problem mentions using a Big-M method. So, I need to model this as a mixed-integer linear program. The Big-M method is used to handle the fixed order costs, which are only incurred if an order is placed in a period. 

Let me think about the decision variables. For each period, I need to decide how much to order (let's call that x_t) and whether an order is placed (a binary variable y_t). The fixed cost is 48, and the Big-M value is given as 181. 

The constraints would include inventory balance for each period. The inventory at the start of period t is the previous inventory plus the order placed in the previous period, minus the demand. Also, the order quantity can't be negative. 

Wait, the initial inventory is 20. So for period 1, the inventory before ordering is 20. Then, after ordering x_1, the inventory becomes 20 + x_1 - demand_1. Then, for period 2, the inventory before ordering is the previous inventory (after period 1's demand), and so on.

So, for each period t (from 1 to 4), the inventory at the start of the period is the previous inventory plus the order from the previous period, minus the demand. Wait, maybe I should model the inventory after ordering and before demand. Or maybe the inventory after demand is met. Let me clarify.

Let me think of the inventory at the end of period t. Let's say I_t is the inventory at the end of period t. Then, for each period t:

I_0 = initial_inventory = 20.

For each t from 1 to 4:

I_{t} = I_{t-1} + x_t - demand_t.

But x_t is the order placed in period t. However, the order is placed before the demand is met. So, the inventory before demand is I_{t-1} + x_t, and then after meeting demand, it's I_{t-1} + x_t - demand_t = I_t.

So, the constraints would be:

For each period t in 1..4:

I_{t} = I_{t-1} + x_t - demand_t.

But since I_0 is known, we can model this recursively.

Now, the fixed order cost is incurred if x_t > 0. But since x_t can be zero, we need to model this with a binary variable y_t, which is 1 if an order is placed in period t (i.e., x_t > 0), and 0 otherwise. However, since x_t can be zero even if y_t is 1 (but that's not allowed), we need to ensure that y_t is 1 if x_t > 0. 

To model this, we can use the Big-M method. The idea is to link x_t and y_t with constraints. For example:

x_t <= M * y_t

This ensures that if y_t is 0, x_t must be 0. But since M is given as 181, which is larger than the maximum possible order quantity, this should work. Also, we need to make sure that if x_t is positive, y_t is 1. 

But wait, the maximum possible order quantity in any period would be the sum of all demands, but since the Big-M is 181, which is larger than the maximum possible order (since the total demand is 55+32+48+46 = 181, so M is exactly equal to the total demand. Hmm, but maybe the M is chosen as a value that's larger than the maximum possible order quantity. However, in this case, the M is 181, which is exactly the total demand. So, perhaps the model is designed such that if an order is placed in a period, the quantity can't exceed M. But since the total demand is 181, maybe the M is set to that. 

But regardless, the Big-M approach is to model the fixed cost as fixed_order_cost * y_t, and then link x_t with y_t via constraints. 

So, the total cost is:

Total cost = sum over t (unit_order_cost * x_t) + sum over t (holding_cost * I_t) + sum over t (fixed_order_cost * y_t)

But the holding cost is based on the inventory at the end of the period. Wait, the problem says "holding cost" is 3 per unit. So, for each period, the holding cost is 3 multiplied by the inventory at the end of the period. 

So, the objective is to minimize the sum of:

- unit_order_cost * x_t for each period (cost of ordering)
- holding_cost * I_t for each period (cost of holding inventory)
- fixed_order_cost * y_t for each period (setup cost if order is placed)

Now, the variables:

x_t: quantity ordered in period t. Must be >=0, integer? Or can be real? The problem doesn't specify, but since it's an optimization problem, maybe x_t can be real. However, in some cases, orders are in integer quantities. But the problem doesn't specify, so I'll assume x_t can be real numbers. But since the Big-M method is used, and the problem allows for real variables, perhaps the model is continuous. 

But the fixed_order_cost is only incurred if an order is placed. So, the binary variable y_t is 1 if x_t > 0, and 0 otherwise. 

But how to model that? The standard approach is to use the constraints:

x_t <= M * y_t

and 

x_t >= 0 (since you can't order negative)

But since y_t is binary, this ensures that if y_t is 1, x_t can be up to M. If y_t is 0, x_t must be 0. 

But in this case, the problem says that the fixed order cost is 48, and the Big-M is 181. So, the M is 181. 

So, the constraints for each period t:

x_t <= M * y_t

But also, since the holding cost is based on the inventory at the end of the period, which is I_t = I_{t-1} + x_t - demand_t. 

So, the variables:

I_t: inventory at the end of period t. 

But since I_0 is known, we can model this recursively. 

So, for each period t from 1 to 4:

I_t = I_{t-1} + x_t - demand_t

But since I_t can't be negative, we need to ensure that I_t >= 0. Wait, the problem doesn't mention any constraints on inventory being non-negative. But in reality, you can't have negative inventory. So, perhaps we need to add constraints that I_t >= 0 for all t. 

But the problem statement doesn't specify that, but in practice, it's necessary. So, I'll include that. 

So, the constraints are:

For each t in 1..4:

I_t = I_{t-1} + x_t - demand_t

I_t >= 0

But since I_0 is 20, we can model this as:

I_0 = 20

For t=1:

I_1 = I_0 + x_1 - demand_1

For t=2:

I_2 = I_1 + x_2 - demand_2

and so on.

Now, the variables:

x_t: real numbers >=0

y_t: binary variables (0 or 1)

I_t: real numbers >=0

But in PuLP, variables can be declared with bounds. 

So, the steps to model this:

1. Create the problem.

2. Define variables:

   - x_t for each period t (continuous, >=0)

   - y_t for each period t (binary)

   - I_t for each period t (continuous, >=0)

But since I_0 is known, we can compute I_1, I_2, etc., based on the previous I and x_t.

But in PuLP, we need to model the constraints for each period.

So, for each period t (1 to 4):

   I_t = I_{t-1} + x_t - demand[t-1]

But since I_0 is 20, we can model this as:

For t=1:

I_1 = I_0 + x_1 - demand[0]

For t=2:

I_2 = I_1 + x_2 - demand[1]

and so on.

So, in code, for each t in 1..4, we can create a constraint that I_t - I_{t-1} - x_t + demand[t-1] = 0.

But in PuLP, we can loop through each period and create these constraints.

Now, the objective function is:

sum (unit_order_cost * x_t) + sum (holding_cost * I_t) + sum (fixed_order_cost * y_t)

So
