import pulp and os.

Then, define the build_model function. Inside, create the problem.

Variables:

We need to create variables for x[i][t] and inv[i][t]. But maybe inv can be derived from x and demand, but since we need to track inventory levels for constraints, it's better to have them as variables.

But perhaps we can model inv as a variable. Let's proceed.

In PuLP, variables can be created with loops. For example, for each item and period, create x[i][t] and inv[i][t].

But since the periods are 3, and items are 4, we can loop through them.

So, in code:

items = 4

periods = 3

Then, for each item i in 0..3, and period t in 0..2:

x = LpVariable.dicts("order", ((i, t) for i in range(items) for t in range(periods)), lowBound=0)

Similarly for inv:

inv = LpVariable.dicts("inventory", ((i, t) for i in range(items) for t in range(periods)), lowBound=
