import pulp and os.

Then, define the periods as 4, initial inventory 17, demand as given.

The function build_model() should return the LpProblem.

Let me outline the steps:

1. Create the problem instance.

2. Define the variables:

   For each period t in 0 to 3:

   order[t] = LpVariable(f'order_{t}', lowBound=0, cat='Integer') ?

Wait, but the problem doesn't specify if the order quantity must be integer. The problem says "inventory replenishment", which could be continuous or integer. Since the problem doesn't specify, but the parameters are integers, perhaps the model can assume that
