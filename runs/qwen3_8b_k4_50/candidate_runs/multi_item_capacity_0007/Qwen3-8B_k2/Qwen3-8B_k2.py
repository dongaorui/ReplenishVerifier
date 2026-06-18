import pulp and os.

Then, define the parameters from the JSON. The JSON has items=4, periods=3, initial_inventory, demand, volume, storage_capacity, unit_order_cost, holding_cost.

So, the code will need to parse these parameters. But since the user provided the JSON, perhaps the code can hardcode these values, but maybe the function build_model() will take these parameters as inputs. However, the user's problem says that the parameters are given as JSON, so the code should use those values.

Wait, the user provided the parameters as JSON, but the code is supposed to be self-contained. So the code should include the parameters as variables. Let me check the JSON:

The JSON has:

"items": 4,

"periods": 3,

"initial_inventory": [1,3,19,13],

"demand": [[22,35,31], [27,14,27], [32,42,35], [44,31,11]],

"volume": [1,3,2,3],

"storage_capacity": 124,

"unit_order_cost": [3,4,5,5],

"holding_cost": [1,4,2,3]

So, the code can hardcode these values. But perhaps the function build_model() should take these parameters as inputs. However, the user's problem says that the code should be written with the given parameters. So the code can directly use these values.

Now, the code structure:

Define the build_model() function, which returns the LpProblem.

Inside build_model(), create the problem, define variables, add constraints, and the objective.

Let me outline the variables:

For each item i in 0..3, and period t in 0..2:

order = LpVariable.dicts("order", (i, t), lowBound=0, cat='Integer')

inventory = LpVariable.dicts("inventory", (i, t), lowBound=0, cat='Integer')

Wait, but the inventory can be a real number? Or is it integer? The problem doesn't specify, but since the demand and initial inventory are integers, and the order quantities are likely integers (since you can't order a fraction of a unit), but the problem may allow real numbers. However, the user's parameters have integer values, but the code may need to handle real numbers. However, the problem says "minimize order and holding costs", which could be continuous. So perhaps the variables are continuous. But the problem may require integer variables. However, the user hasn't specified, so perhaps we can assume continuous variables.

But the problem says "inventory balance and capacity" which are constraints. So, the code can use continuous variables.

So, in PuLP, the variables can be defined as continuous.

Now, the objective function is sum over all items and periods of (unit_order_cost[i] * order[i][t] + holding_cost[i] * inventory[i][t]).

So, the objective is to minimize that sum.

Now, the constraints:

For each period t and item i:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But for t=0, inventory[-1][i] is initial_inventory[i]. So for t=0, the equation is:

inventory[0][i] = initial_inventory[i] + order[0][i] - demand[0][i]

For t >=1, the equation is:

inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

So, for each t in 0..2, and i in 0..3:

if t == 0:

   inventory[t][i] = initial_inventory[i] + order[t][i] - demand[t][i]

else:

   inventory[t][i] = inventory[t-1][i] + order[t][i] - demand[t][i]

But how to model this in PuLP? For each t and i, we can create a constraint that enforces this equation.

So, for each t in 0 to periods-1:

   for each i in 0 to items-1:

       if t == 0:
