<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem. Let me start by understanding the problem details.

The problem has 3 periods. Initial inventory is 0, and demands are [51, 39, 45]. We need to decide the order quantity Q_t each period, inventory I_t, and a binary variable Y_t indicating if an order is placed. The fixed order cost is 68, unit order cost is 3, holding cost is 3. We have to use Big-M method with M=135.

First, I need to set up the PuLP model. Let me recall the steps. The model will have variables for Q_t, I_t, and Y_t. The objective is to minimize the sum of unit order costs, holding costs, and fixed order costs. 

Wait, the fixed order cost is only incurred if an order is placed. So for each period, if Y_t is 1, we pay the fixed cost. The Big-M method is used to link Q_t and Y_t. The constraints would be:

For each period t:
1. Inventory balance: I_{t-1} + Q_t - demand_t = I_t. But since initial inventory is 0, for t=1, I_0 is 0.
2. Q_t must be >= demand_t - I_{t-1} if Y_t is 1? Or maybe the other way around. Wait, the Big-M constraints are usually used to enforce that if Y_t is 1, then Q_t >= some value. Let me think. The standard approach is to have Q_t >= demand_t - I_{t-1} + (something) to ensure that if Y_t is 1, then Q_t is sufficient. Wait, maybe the constraints are:

For each period t:
- I_{t} = I_{t-1} + Q_t - demand_t
- Q_t >= 0
- Y_t is binary
- The Big-M constraints to link Q_t and Y_t. For example, Q_t >= demand_t - I_{t-1} - M*(1 - Y_t). Wait, maybe I need to ensure that if Y_t is 0, then Q_t is zero. But since the problem allows for ordering, perhaps the Big-M is used to enforce that if Y_t is 1, then Q_t is at least the required amount to meet demand and any previous inventory. Wait, maybe the constraints are:

Q_t >= demand_t - I_{t-1} - M*(1 - Y_t). Wait, no. Let me think again. The standard Big-M approach for linking a binary variable Y_t to a continuous variable Q_t is to have:

Q_t >= M * Y_t. But that would mean that if Y_t is 1, Q_t must be at least M. But that's not right. Wait, maybe the constraints are:

Q_t >= demand_t - I_{t-1} - M*(1 - Y_t). Wait, perhaps the correct way is to ensure that if Y_t is 1, then Q_t can be anything (but must be non-negative), but if Y_t is 0, then Q_t must be zero. Wait, but that's not correct. Because if Y_t is 0, you can't order. So the constraints would be:

Q_t <= M * Y_t (so if Y_t is 0, Q_t must be zero)
and Q_t >= 0.

But then, how to ensure that when Y_t is 1, Q_t can be any value. But in the problem, the order quantity Q_t is the amount ordered, which can be zero even if Y_t is 1? Wait, no. The Y_t is a binary variable indicating whether an order is placed. So if Y_t is 1, then an order is placed, but the quantity can be zero? Or is Q_t required to be non-zero when Y_t is 1? The problem statement says "Use order Q_t, inventory I_t, binary order trigger Y_t". So perhaps Y_t is 1 if an order is placed (regardless of quantity), but Q_t can be zero. But that might not make sense. Alternatively, maybe Y_t is 1 if Q_t > 0. But the problem says to use Big-M links, so perhaps the constraints are:

Q_t >= M * (1 - Y_t). Wait, no. Let me think again. The standard approach for Big-M is to model the relationship between Y_t and Q_t. For example, if Y_t is 1, then Q_t must be at least some value. But in this case, the fixed cost is incurred if Y_t is 1, regardless of Q_t. So the fixed cost is 68 per period if Y_t is 1. So the Big-M constraints are probably to ensure that if Y_t is 1, then Q_t is non-negative (which it already is), but maybe to link the order quantity with the binary variable. Wait, perhaps the problem requires that when Y_t is 1, Q_t must be at least the required amount to meet the demand. But that's not clear. Wait, the problem says "Use order Q_t, inventory I_t, binary order trigger Y_t, and Big-M links with M=135". So the Big-M is used to link Y_t and Q_t. 

Let me check the standard approach for such models. Typically, the Big-M method is used to enforce that if Y_t is 1, then Q_t must be at least the required amount. For example, in the case of a fixed order cost, you might have constraints that ensure that if you order (Y_t=1), then Q_t is at least the amount needed to meet the demand. But in this problem, the demand is given, and the inventory balance must be maintained. So perhaps the constraints are:

For each period t:

I_{t} = I_{t-1} + Q_t - demand_t

And for the Big-M constraints, we need to ensure that if Y_t is 1, then Q_t is at least the amount needed to cover the demand minus the previous inventory. Wait, but that's part of the inventory balance. Alternatively, the Big-M constraints are used to model the fixed cost. For example, the fixed cost is 68 * Y_t. So the objective function includes sum over t of (unit_order_cost * Q_t + holding_cost * I_t + fixed_order_cost * Y_t). 

But how to model the relationship between Y_t and Q_t? Because if Y_t is 1, then you can have Q_t being any value (including zero?), but that's not correct. Wait, perhaps the problem requires that if Y_t is 1, then Q_t must be non-zero. But that's not stated. Alternatively, maybe the Big-M is used to model the fact that if Y_t is 1, then Q_t can be anything, but if Y_t is 0, then Q_t must be zero. That would make sense. So the constraints would be:

Q_t <= M * Y_t (so if Y_t is 0, Q_t must be zero)

and Q_t >= 0.

But then, the Big-M is used here. So for each period t, we have:

Q_t <= M * Y_t

But since M is given as 135, which is larger than the maximum possible demand (the maximum demand is 51, 39, 45, so 51). So if Y_t is 1, Q_t can be up to 135. But the problem says to use Big-M links. So perhaps that's the way to model it. 

So the constraints would be:

For each t:

I_t = I_{t-1} + Q_t - demand_t

Q_t <= M * Y_t

Q_t >= 0

Y_t is binary.

But then, the fixed cost is 68 * Y_t. 

So the objective function is:

sum (unit_order_cost * Q_t) + sum (holding_cost * I_t) + sum (fixed_order_cost * Y_t)

So the variables are Q_t, I_t, Y_t.

Now, let's think about the initial inventory. The initial inventory is 0, so I_0 = 0. Then, for t=1, I_1 = I_0 + Q_1 - demand_1. For t=2, I_2 = I_1 + Q_2 - demand_2, etc.

Now, the problem is to model this in PuLP.

So, steps:

1. Import pulp and os.

2. Define the parameters: periods=3, initial_inventory=0, demand=[51,39,45], unit_order_cost=3, holding_cost=3, fixed_order_cost=68, big_m=135.

3. Create the PuLP problem. The problem is a minimization problem.

4. Define the variables:

For each period t (1 to 3):

- Q_t: continuous variable >=0

- I_t: continuous variable >=0

- Y_t: binary variable

But in PuLP, variables can be created with loops.

So, for t in 1 to periods:

Q = LpVariable.dicts("Q", t, lowBound=0)

Similarly for I and Y.

Wait, but in PuLP, variables are created as dictionaries. So perhaps:

variables:

Q = LpVariable.dicts("Q", range(periods), lowBound=0)

I = LpVariable.dicts("I", range(periods), lowBound
