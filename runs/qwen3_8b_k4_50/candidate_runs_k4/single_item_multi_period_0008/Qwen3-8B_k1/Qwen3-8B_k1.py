import pulp and os.

Then, define the build_model function. Inside, create the problem.

Let me outline the steps:

1. Define the periods (6).

2. Define the initial inventory (11).

3. Define the demand list.

4. Define the unit_order_cost and holding_cost.

Then, create the variables:

order = [pulp.LpVariable(f"order_{t}", lowBound=0) for t in range(periods)]

inventory = [pulp.LpVariable(f"inventory_{t}", lowBound=0) for t in range(periods)]

Then, create the problem.

prob = pulp.LpProblem("Inventory_Replenishment", pulp.LpMinimize)

Set the objective function:

prob += pulp.lpSum([order[t] * unit_order_cost for t in range(periods)]) + pulp.lpSum([inventory[t] * holding_cost for t in range(periods)])

Then, add the constraints for each period.

For each t in 0 to 5:

if t == 0:

    prob += inventory[t] - initial_inventory - order[t] + demand[t] == 0

else:

    prob += inventory[t] - inventory[t-1] - order[t] + demand[t] == 0

Wait, but in the equation, it's inventory[t] = previous_inventory + order[t] - demand[t]. So rearranged, inventory[t] - previous_inventory - order[t] + demand[t] = 0.

Yes.

So for each t, the constraint is:

inventory[t] - previous_inventory - order[t] + demand[t] == 0

Where previous_inventory is initial_inventory if t=0, else inventory[t-1].

Then, also, the inventory variables must be >=0, but since we set lowBound=0 when creating them, that's already handled.

Now, the code.

But in the problem statement, the parameters are given as JSON. So the code should use the parameters from the JSON. Let me check the parameters again:

periods: 6

initial_inventory: 11

demand: [29, 23, 47, 46, 20, 18]

unit_order_cost: 1

holding_cost: 2

So in the code, the parameters are:

periods = 6

initial_inventory = 11

demand = [29, 23, 47, 46, 20, 18]

unit_order_cost = 1

holding_cost = 2

So the code would have these variables.

Now, the function build_model() returns the prob.

Then, in the main block, call build_model(), check for the environment variable OUTPUT_LP_PATH, write the LP if exists, solve, and print the status and objective.

Now, putting all together.

But need to make sure that the code is correct.

Wait, in the code, the demand is a list of 6 elements, and the periods are 6. So for t in 0 to 5, the demand[t] is correct.

Now, code steps:

Import pulp and os.

Define the parameters.

Build the model.

Then, in the main block, call build_model(), solve, etc.

Now, code:

import pulp
import os

def build_model
