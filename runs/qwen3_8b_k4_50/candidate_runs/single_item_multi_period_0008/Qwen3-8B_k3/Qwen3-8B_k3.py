import pulp and os.

Then, define the problem as a minimization problem.

Variables:

For each period i in 1..6, x_i is a continuous variable >=0.

For each period i in 0..6, I_i is a continuous variable >=0.

But I_0 is fixed at 11. So, in the model, we can set I_0 = 11.

Then, for each i from 1 to 6:

I_i = I_{i-1} + x_i - demand_i

So, the constraints are:

For i in 1..6:

I_i - I_{i-1} - x_i + demand_i = 0

Also, I_0 = 11.

But in PuLP, we can model this as:

prob += I_0 == 11

But since I_0 is a variable, perhaps we need to set it as a constant. Wait, no. Because in PuLP, variables are defined with their bounds. So, if I_0 is a variable, but we know it's fixed at 11
