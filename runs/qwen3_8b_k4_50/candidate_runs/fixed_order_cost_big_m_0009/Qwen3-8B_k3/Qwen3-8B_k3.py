import pulp and os.

Then, create the problem. The function build_model() should return the LpProblem.

In the main block, call build_model(), check for the environment variable OUTPUT_LP_PATH, write the LP if present, solve, and print the status and objective.

Now, the variables:

We need to create variables for Q_t, I_t, Y_t for each period t from 1 to T (T=3).

In PuLP, variables can be created with loops. Let's say periods = 3.

So for each t in 1..3:

Q = LpVariable.dicts("Q", range(1, periods+1), lowBound=0, cat='Continuous')

Similarly for I and Y.

But since Y is binary, we need to set cat='Binary'.

Then, the constraints:

First, initial inventory is 0. So I_0 = 0. Then, for each period t:

I_t = I_{t-1} + Q_t - D_t.

But since I_t must be >= 0, we can write:

For each t in 1..T:

I_t >= I_{t-1} + Q_t - D_t

Wait, no. The equation is I_t = I_{t-1} + Q_t - D_t. But since I_t can't be negative, we have I_t >= 0. So the constraint is I_t >= I_{t-1} + Q_t - D_t, but also I_t >= 0. Wait, but the equation is I_t = I_{t-1} + Q_t - D_t. However, if I_{t-1} + Q_t - D_t is negative, then I_t would be negative, which is not allowed. Therefore, we need to ensure that I_{t-1} + Q_t >= D_t. So the constraint is I_t >= 0, which is equivalent to I_{t-1} + Q_t - D_t >= 0. Wait, no. Because I_t is the inventory after meeting demand. So if I_{t-1} + Q_t is less than D_t, then the inventory would be negative, which is not allowed. Therefore, the constraint is I_{t-1} + Q_t >= D_t. But since I_t = I_{t-1} + Q_t - D_t, and I_t >= 0, that implies I_{t-1} + Q_t - D_t >= 0. So the constraint is I_{t} >= 0, which is equivalent to I_{t-1} + Q_t >= D_t. Therefore, the constraint is I_t >= 0.

But how to model this in PuLP. For each t, we can write:

I_t = I_{t-1} + Q_t - D_t

But since I_t can't be negative, we have I_t >= 0.

But in PuLP, we can't directly write equations, but we can write inequalities. Wait, but the equation is I_t = I_{t-1} + Q_t - D_t. However, since I_t can't be negative, we have to ensure that I_{t-1} + Q_t - D_t >= 0. So the constraint is I_t >= 0, which is equivalent to I_{t-1} + Q_t - D_t >= 0. Therefore, for each t, we can write:

I_t >= I_{t-1} + Q_t - D_t

But since I_t is the variable, and I_{t-1} is the previous inventory. Wait, but how to model this. For example, for t=1:

I_1 = I_0 + Q_1 - D_1. Since I_0 is 0, I_1 = Q_1 - D_1. But since I_1 >= 0, we have Q_1 >= D_1. So the constraint is I_1 >= 0.

But in PuLP, we can model this as:

For each t in 1..T:

prob += I[t] >= I[t-1] + Q[t] - demand[t-1]

Wait, but the demand is given as a list. Let's index the demand as D[0], D[1], D[2] for periods 1, 2, 3. So for period t (1-based), the demand is D[t-1].

So for each t in 1..T:

I[t] = I[t-1] + Q[t] - D[t-1]

But since I[t] can't be negative, we have I[t] >= 0. So the constraint is I[t] >= 0.

But how to model this in PuLP. For each t, we can add the constraint that I[t] >= I[t-1] + Q[t] - D[t-1], and also I[t] >= 0. Wait, but the first constraint already ensures that I[t] is at least I[t-1] + Q[t] - D[t-1], which could be negative. So we need to add I[t] >= 0. Wait, no. Because if I[t] is equal to I[t-1] + Q[t] - D[t-1], then if that value is negative, I[t] would be negative, which is not allowed. Therefore, we need to have I[t] >= 0. So for each t, we have two constraints:

I[t] >= I[t-1]
