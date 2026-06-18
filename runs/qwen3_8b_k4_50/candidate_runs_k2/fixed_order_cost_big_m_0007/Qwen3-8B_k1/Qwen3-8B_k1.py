<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem. Let me start by understanding the problem statement.

The problem has 3 periods. Initial inventory is 12, and demands are 23, 24, 29. We need to decide the order quantity Q_t each period, inventory I_t, and a binary variable Y_t indicating if an order is placed. The fixed order cost is 24, unit order cost is 2, holding cost is 2. We have to use Big-M method with M=76. The goal is to minimize total cost, which includes ordering, holding, and fixed costs.

First, I need to set up the PuLP model. Let me recall how to structure this. The model will have variables for Q_t, I_t, and Y_t. The constraints will include inventory balance, non-negativity, and the Big-M links between Q and Y.

Let me think about the variables. For each period t (from 1 to T), Q_t is the quantity ordered, I_t is the inventory after meeting demand. Y_t is a binary variable indicating if an order is placed in period t. Since the problem mentions fixed ordering costs, Y_t will be 1 if Q_t > 0, and 0 otherwise. But since Q_t can be zero, we need to link Q_t and Y_t with the Big-M method.

The Big-M constraints would be: Q_t ≤ M * Y_t. Also, since Y_t is binary, we need to ensure that if Y_t is 1, Q_t can be up to M. But also, if Y_t is 0, Q_t must be 0. So the constraints would be Q_t ≤ M * Y_t and Q_t ≥ 0. Wait, but maybe we need to have Q_t ≥ 0 and Q_t ≤ M * Y_t. Also, since Y_t is binary, that would enforce that if Y_t is 0, Q_t must be 0. But maybe there's another constraint to ensure that if Q_t is positive, Y_t is 1. That's handled by Q_t ≥ ε * Y_t, but since we're using Big-M, perhaps the standard approach is to have Q_t ≤ M * Y_t and Q_t ≥ 0. Wait, but if Y_t is 0, then Q_t must be 0. So the first constraint Q_t ≤ M * Y_t ensures that. But also, we need to make sure that if Y_t is 1, Q_t can be positive. So the lower bound on Q_t is 0. But maybe there's a need for another constraint to ensure that if Y_t is 1, Q_t can be non-zero. However, since the problem allows for Q_t to be zero even when Y_t is 1 (but that's not allowed because the fixed cost is incurred when Y_t is 1). Wait, no. The fixed cost is incurred when an order is placed, which is when Y_t is 1. So even if Q_t is zero, if Y_t is 1, the fixed cost is added. But in reality, if Y_t is 1, you must have Q_t ≥ 0. But maybe the problem allows for ordering zero quantity but paying the fixed cost. However, in practice, that's not efficient. But the problem says to use the Big-M method, so perhaps the constraints are Q_t ≤ M * Y_t and Q_t ≥ 0. But then, if Y_t is 1, Q_t can be zero. However, the fixed cost is 24 per order. So the model should include the fixed cost as fixed_order_cost * Y_t.

Now, the inventory balance. For each period t, the inventory after order and before demand is I_{t-1} + Q_t. Then, after meeting demand, it's I_{t} = I_{t-1} + Q_t - demand[t]. But since the initial inventory is 12, I_0 = 12. So for t=1, I_1 = I_0 + Q_1 - demand[0]. For t=2, I_2 = I_1 + Q_2 - demand[1], etc. So the constraints would be I_t = I_{t-1} + Q_t - demand[t-1], for t from 1 to T. Wait, the demand array is [23,24,29], so for period 1, demand is 23, period 2 is 24, period 3 is 29. So for t in 1..3, the demand is demand[t-1].

But in PuLP, we need to model these as constraints. So for each t, I_t = I_{t-1} + Q_t - demand[t-1]. But since I_0 is initial_inventory, which is 12.

Now, the objective function is to minimize the sum of unit_order_cost * Q_t + holding_cost * I_t + fixed_order_cost * Y_t for all t. So the total cost is sum(2*Q_t) + sum(2*I_t) + sum(24*Y_t).

Now, the Big-M constraints. For each t, Q_t ≤ M * Y_t. Also, since Y_t is binary, we need to ensure that if Y_t is 1, Q_t can be up to M. But also, if Y_t is 0, Q_t must be 0. So the constraint Q_t ≤ M * Y_t and Q_t ≥ 0. But since Q_t can be zero even when Y_t is 1, but that's allowed. However, the fixed cost is incurred regardless of Q_t being zero. So the model should include that.

Now, the variables. Let's define:

- Q_t: quantity ordered in period t. Continuous variable ≥ 0.
- I_t: inventory after demand in period t. Continuous variable ≥ 0.
- Y_t: binary variable indicating if an order is placed in period t.

But wait, the problem says to use the Big-M links. So the constraints for Q_t and Y_t are:

For each t, Q_t ≤ M * Y_t. Also, since Y_t is binary, we can have Q_t ≥ 0. But also, perhaps we need to ensure that if Y_t is 1, Q_t can be non-zero. However, the constraint Q_t ≤ M * Y_t and Q_t ≥ 0 would allow Q_t to be zero when Y_t is 1. But that's acceptable because the fixed cost is incurred regardless of Q_t. However, in practice, if Y_t is 1, you might want to have Q_t ≥ some minimum, but the problem doesn't specify that. So we proceed with the given constraints.

Now, the code structure. The user wants a function build_model() that returns the LpProblem. Then, in the main block, call build_model(), solve, etc.

Let me outline the steps:

1. Import pulp and os.
2. Define the parameters from the JSON.
3. Create the problem.
4. Define variables for Q, I, Y.
5. Add constraints for inventory balance.
6. Add Big-M constraints for Q and Y.
7. Define the objective function.
8. Solve and print results.

Let me think about the variables. For periods 1 to T (3 periods), we need variables for each period. So for Q, I, Y, we can have lists.

In PuLP, variables can be created with loops. For example:

Q = [pulp.LpVariable(f'Q_{t}', lowBound=0, cat='Continuous') for t in range(periods)]
Similarly for I and Y.

But the initial inventory is 12. So for t=0, I_0 = 12. Then, for each t from 1 to T, the inventory after demand is I_t = I_{t-1} + Q_t - demand[t-1].

So the constraints for inventory:

for t in 1 to T:
    I[t] = I[t-1] + Q[t] - demand[t-1]

But in PuLP, we need to express this as a constraint. So for each t in 1..T, we can add:

prob += I[t] == I[t-1] + Q[t] - demand[t-1]

But since I is a list, we need to index properly. Let me think about the indices. Let's say periods are 0-based or 1-based? The problem says T=3 periods, so perhaps the periods are 0,1,2. But the code can be written with 0-based or 1-based. Let me use 0-based for easier indexing.

Wait, the problem says "plan T=3 periods with fixed ordering costs". So the periods are 1 to 3, but in code, perhaps 0 to 2. Let me check the demand array: [23,24,29], which is 3 elements. So for period 1, demand is 23, period 2 is 24, period 3 is 29. So in code, for t in 0 to 2 (periods 1-3), the demand is demand[t].

So the initial inventory is I_0 = 12. Then for each t in 0 to 2 (periods 1-3), the inventory after demand is I_{t} = I_{t-1} + Q_t - demand[t]. Wait, no. Wait, the initial inventory is I_0 = 1
