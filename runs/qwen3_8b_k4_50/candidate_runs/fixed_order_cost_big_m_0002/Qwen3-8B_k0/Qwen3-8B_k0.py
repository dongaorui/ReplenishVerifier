import pulp and os.

Then, create the problem.

The function build_model() should return the LpProblem.

Inside build_model(), we need to define the variables.

Let me outline the steps:

1. Define the periods (3 in this case).
2. Define the initial inventory (5).
3. Define the demand for each period.
4. Define the variables:

   For each period t (1 to 3):

   - O_t: order quantity. Continuous variable >=0.
   - Y_t: binary variable.
   - I_t: inventory at end of period t. Continuous variable >=0.

But in PuLP, variables can be created with loops.

So, for each period in 1 to periods:

   O = LpVariable(f"O_{t}", lowBound=0)
   Y = LpVariable(f"Y_{t}", cat='Binary')
   I = LpVariable(f"I_{t}", lowBound=0)

But need to make sure that the variables are properly indexed.

Then, the constraints:

For each period t:

   The inventory balance equation.

But for t=1, the previous inventory is initial_inventory.

So, for t in 1 to periods:

   if t == 1:
       prev_inventory = initial_inventory
   else:
       prev_inventory = I_{t-1}

   So, the constraint is:

   prev_inventory + O_t - demand[t-1] == I_t

Wait, the demand is given as a list, so for period 1, demand[0] is 21, etc.

So, for each t in 1 to periods:

   demand_t = demand[t-1]

   So, the constraint is:

   prev_inventory + O_t - demand_t == I_t

But how to handle the previous inventory. For t=1, prev_inventory is initial_inventory. For t>1, it's I_{t-1}.

So, for t=1:

   5 + O_1 - D_1 = I_1

For t=2:

   I_1 + O_2 - D_2 = I_2

For t=3:

   I_2 + O_3 - D_3 = I_3

So, in code, for each t in 1 to periods:

   if t == 1:
       prev_inv = initial_inventory
   else:
       prev_inv = I[t-1]

   prob += prev_inv + O[t] - demand[t-1] == I[t]

But in PuLP, variables are stored in a dictionary or list. So, perhaps create lists for O, Y, I.

So, in code:

periods = 3
initial_inventory = 5
demand = [21, 42, 29]
unit_order_cost =
