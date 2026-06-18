import pulp and os. Then, define the build_model function. Inside, create the problem.

The periods are 4. Let's index them from 0 to 3 or 1 to 4? Probably easier to use 0-based for Python. But the problem says T=4 periods, so maybe 1 to 4. Let me check the parameters. The demand is given as a list of 4 elements, so for t in 0 to 3 (if 0-based) or 1 to 4 (if 1-based). Let's use 0-based for the code.

Wait, the problem says "plan T=4 periods with fixed ordering costs". So the periods are 1 to 4. But in code, it's easier to loop through 0 to 3. Let me think. Let's use t in 0 to 3 (for 4 periods). Then, initial inventory is I_0 = 16. For each period t (0 to 3), the demand is demand[t].

The inventory balance equation for period t is:

I_{t} = I_{t-1} + Q_t - demand[t]

But for t=0, I_{-1} is initial inventory. So for t=0, I_0 = initial_inventory + Q_0 - demand[0]. Wait, no. Wait, initial inventory is before period 1. Let me think again.

Let me think of the periods as 1 to T. So for period 1, the initial inventory is I_0 = 16. Then, after ordering Q_1, the inventory becomes I_1 = I_0 + Q_1 - demand[0]. Then, for period 2, I_1 + Q_2 - demand[1] = I_2, etc. So the indices for the demand list would be 0-based, but the periods are 1-based. So for period t (1 to T), the demand is demand[t-1].

So in code, for each t in 1 to T:

I_{t} = I_{t-1} + Q_t - demand[t-1]

But in PuLP, variables are indexed. So perhaps we can create variables for Q, I, Y for each period.

So, variables:

Q = [pulp.LpVariable(f'Q_{t}', lowBound=0, cat='Continuous') for t in range(periods)]

I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(periods)]

Y = [pulp.LpVariable(f'Y_{t}', cat='Binary') for t in range(periods)]

Wait, but for the initial inventory, I_0 is 16. Then, for period 1 (t=0 in the list?), the inventory after meeting demand would be I_0 + Q_0 - demand[0] = I_1. Wait, maybe I need to adjust the indices.

Alternatively, perhaps the periods are 0 to 3 (for 4 periods), and the initial inventory is I_0 = 16. Then, for each period t (0 to 3), the inventory after the period is I_t. So the inventory balance equation is:

I_t = I_{t-1} + Q_t - demand[t]

But for t=0, I_{-1} is initial inventory. So for t=0, I_0 = initial_inventory + Q_0 - demand[0]. Wait, no. Wait, initial inventory is before any orders. So for period 0 (first period), the initial inventory is I_0 = 16. Then, after ordering Q_0, the inventory becomes I_0 + Q_0 - demand[0] = I_1. So the inventory after period 0 is I_1. So the variables I would be for the inventory after the period. So for t in 0 to 3 (4 periods), I_t is the inventory after period t. Then, the initial inventory is I_{-1} = 16. So for t=0, I_0 = I_{-1} + Q_0 - demand[0]. But since I_{-1} is 16, that's the initial inventory.

So the constraints for each period t (from 0 to 3) would be:

I_t = I_{t-1} + Q_t - demand[t]

But for t=0, I_{t-1} is the initial inventory, which is 16. So for t=0, the constraint is I_0 = 16 + Q_0 - demand[0]. For t >=1, I_t = I_{t-1} + Q_t - demand[t].

So in code, for each t in 0 to 3:

if t == 0:
    I_t = initial_inventory + Q_t - demand[t]
else:
    I_t = I_{t-1} + Q_t - demand[t]

But how to model this in PuLP. For each t, we can create a constraint that I_t - I_{t-1} - Q_t + demand[t] = 0. Except for t=0, where I_{t-1} is initial_inventory.

Wait, for t=0, the equation is I_0 - initial_inventory - Q_0 + demand[0] = 0. Because I_0 = initial_inventory + Q_0 - demand[0], rearranged as I_0 - initial_inventory - Q_0 + demand[0] = 0.

For t >=1, the equation is I_t - I_{t-1} - Q_t + demand[t] = 0.

So for each t in 0 to 3, we can create a constraint:

if t == 0:
    prob += I[t] - initial_inventory - Q[t] + demand[t] == 0
else:
    prob += I[t] - I[t-1] - Q[t] + demand[t] == 0

But in code, how to handle that. Let's think.

In the code, for each t in range(periods):

if t == 0:
    constraint = I[t] - initial_inventory - Q[t] + demand[t] == 0
else:
    constraint = I[t] - I[t-1] - Q[t] + demand[t] == 0

Then add that constraint to the problem.

So that's the inventory balance constraints.

Next, the Big-M constraints. For each t, Q[t] <= M * Y[t], and Q[t] >= 0. But since Q[t] is
