<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The firm has a 4-period horizon. They start with 20 units of inventory. Each period has a demand: 55, 32, 48, 46. The costs are unit order cost 2, holding cost 3, and fixed order cost 48. The Big-M value is 181. The goal is to model this with a mixed-integer program using the Big-M method.

First, I need to define the decision variables. The main variables here are the order quantity each period and whether an order is placed in that period. Since it's a Big-M model, I'll need binary variables to represent the order placement.

Let me think about the variables. For each period, there's an order quantity (let's say x_t) and a binary variable (y_t) indicating if an order is placed in period t. Also, the inventory level at the end of each period (s_t) is important.

The objective function includes the unit order cost multiplied by the order quantity, the holding cost multiplied by the ending inventory, and the fixed order cost multiplied by the binary variable. But since the Big-M method is used, the fixed cost is represented as a term that's only active when y_t is 1. The Big-M approach uses the binary variable multiplied by M to ensure that if an order is placed, the fixed cost is included, otherwise not.

Wait, the fixed order cost is 48. So for each period, if y_t is 1, we add 48 to the cost. But in the Big-M formulation, we can model this as fixed_order_cost * y_t. However, the Big-M method might involve constraints that link the order quantity to the binary variable. For example, x_t must be greater than or equal to 0, and if y_t is 1, then x_t can be positive. But since the problem allows ordering any quantity (including zero), maybe the binary variable y_t is 1 if x_t is positive, but that's not directly enforced. Wait, no. The fixed cost is incurred whenever an order is placed, regardless of the quantity. So even if you order zero, you might still have a fixed cost. Wait, but in practice, placing an order with zero quantity doesn't make sense. So perhaps the model should have y_t = 1 if x_t > 0, but that's a bit tricky. However, in the Big-M formulation, we can model this by ensuring that x_t is bounded by M*y_t. For example, x_t <= M*y_t. That way, if y_t is 0, x_t must be 0. But if y_t is 1, x_t can be up to M. However, in this problem, the fixed cost is incurred whenever an order is placed, which could be even if x_t is zero. But maybe the problem assumes that placing an order means ordering a positive quantity. So perhaps the model should have x_t >= 0, and y_t is 1 if x_t > 0. But how to model that with Big-M? Alternatively, the fixed cost is incurred whenever y_t is 1, regardless of x_t. So the fixed cost is fixed_order_cost * y_t. Then, the constraints would ensure that if y_t is 1, then x_t can be any value (but maybe with a minimum of zero). Wait, but the problem says "whenever it places an order". So placing an order could be even if the quantity is zero. But that's not practical. So perhaps the model should have y_t = 1 if x_t > 0. But how to model that with Big-M? Maybe using x_t >= 1 * y_t, but that would require that if y_t is 1, x_t is at least 1. But the problem allows ordering zero? Or is the order quantity required to be non-negative? The problem says "unit ordering cost" which is per unit ordered. So if you order zero, you pay zero unit cost, but the fixed cost is still incurred if you place an order. Wait, the problem says "setup cost whenever it places an order". So placing an order (even with zero quantity) incurs the fixed cost. But that's not typical. Usually, placing an order implies ordering a positive quantity. However, the problem's parameters might not specify that. So perhaps the model should have y_t as 1 if an order is placed (regardless of quantity), and the fixed cost is fixed_order_cost * y_t. But then, how to model that the order quantity is zero when y_t is 0. So the constraints would be x_t >= 0, and x_t <= M * y_t. Wait, but that would allow x_t to be zero even if y_t is 1. So maybe the model should have x_t >= 0, and the fixed cost is fixed_order_cost * y_t. Then, the constraints would be that x_t can be any non-negative value, but if y_t is 1, then the fixed cost is added. However, the problem might require that if you place an order (y_t=1), you must have x_t >= some minimum. But the problem doesn't specify that. So perhaps the model allows x_t to be zero even if y_t is 1. But that's not practical. However, given the problem's parameters, perhaps the model should have y_t as 1 if an order is placed (i.e., x_t > 0), but how to model that. Alternatively, the problem might not require that, and the fixed cost is incurred whenever y_t is 1, regardless of x_t. 

But given that the problem uses the Big-M method, the standard approach is to have x_t <= M * y_t, and x_t >= 0. Then, the fixed cost is fixed_order_cost * y_t. So the model would have:

Objective: sum over t (unit_order_cost * x_t + holding_cost * s_t + fixed_order_cost * y_t)

Constraints:

For each period t:

Inventory balance: s_{t-1} + x_t - demand[t] = s_t

With s_0 = initial_inventory.

But since the problem is over 4 periods, we need to model the inventory levels for each period.

Also, the Big-M constraints would be x_t <= M * y_t for each t. This ensures that if y_t is 0, x_t must be 0. If y_t is 1, x_t can be up to M. But since M is given as 181, which is larger than the maximum possible order quantity (since the total demand is 55+32+48+46=181, so maybe M is set to that). Wait, the problem says M=181. So perhaps the maximum possible order quantity is 181, but that's just the sum of all demands. So the Big-M is set to that value.

So the variables are:

x_t: order quantity in period t (non-negative)

y_t: binary variable indicating if an order is placed in period t (1 if placed, 0 otherwise)

s_t: inventory at the end of period t (non-negative)

Now, the constraints:

For each period t from 1 to 4:

s_{t-1} + x_t - demand[t] = s_t

With s_0 = initial_inventory (20)

Also, for each t, x_t <= M * y_t (Big-M constraint)

Additionally, since x_t can't be negative, x_t >= 0.

But wait, the problem says "unit ordering cost" which is per unit ordered. So if you order x_t units, you pay unit_order_cost * x_t. The fixed cost is fixed_order_cost * y_t. So the objective is to minimize the sum of these.

So the model is:

Minimize sum (unit_order_cost * x_t + holding_cost * s_t + fixed_order_cost * y_t) for all t.

Subject to:

s_0 = 20

For each t in 1..4:

s_{t-1} + x_t - demand[t] = s_t

x_t <= M * y_t for each t

x_t >= 0

y_t is binary for each t.

But wait, the holding cost is per unit held. So the holding cost is holding_cost * s_t for each period t.

Now, the problem is to model this in PuLP.

So, first, I need to create the variables. Let's think about the periods. The periods are 0 to 3 (assuming 0-based index), but the problem says periods are 4. Let me check the parameters: the demand is a list of 4 elements, so periods are 0 to 3 (assuming 0-based), but the problem says 4 periods. So for each period t in 1 to 4 (if 1-based), but in code, it's easier to use 0-based.

But in the code, I can loop through the periods. Let's say periods are 0 to 3 (since there are 4 periods). The initial inventory is s_0 = 20.

Then, for each period t (from 0 to 3), the demand is demand[t].

The variables:

x = [LpVariable(f"x_{t}", lowBound=0, cat='Continuous') for t in range(periods)]

y = [LpVariable(f"y_{t}", cat='Binary') for t in range(periods)]

s = [LpVariable(f"s_{
