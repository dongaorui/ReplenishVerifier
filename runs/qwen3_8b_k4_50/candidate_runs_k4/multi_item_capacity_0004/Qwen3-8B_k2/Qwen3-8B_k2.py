import pulp and os. Then, define the parameters from the JSON. The items are 3, periods 5. The initial inventory is [3,3,17]. Demand is a 2D list. Volume is [1,2,3], storage capacity 99. Unit order costs and holding costs are given.

Next, create the PuLP problem. The problem name can be something like "MultiItemCapacityOptimization".

Define the decision variables. For each item and period, x[i][t] and inv[i][t]. Since periods start from 1 to 5, and items from 0 to 2 (assuming zero-based indexing), I'll loop through them.

Wait, the problem says periods are 5, so t ranges from 1 to 5. But in Python, it's easier to index from 0. So maybe I'll use 0-based indices for periods. Let me check the demand data. The demand is given as a list of lists, each with 5 elements. So for item 0, demand in period 0 is 18, period 1 is 32, etc. So the periods are 0 to 4 (total 5 periods). So the initial inventory is for period 0, and then periods 0 to 4.

Wait, the initial inventory is given as [3,3,17], which are the starting inventories for each item. So for period 0, the inventory is initial_inventory[i], and then for each subsequent period, the inventory is updated based on orders and demand.

So the inventory balance for item i in period t (where t ranges from 0 to 4) would be:

inv[i][t] = inv[i][t-1] + x[i][t] - demand[i][t]

But for t=0, inv[i][t-1] would be the initial inventory. So for t=0, the equation would be inv[i][0] = initial_inventory[i] + x[i][0] - demand[i][0]. Wait, no. Wait, the initial inventory is the starting inventory before any orders in period 0. So the inventory at the end of period 0 is initial_inventory[i] + x[i][0] - demand[i][0]. But maybe the initial inventory is the starting point, and the first order is in period 0. So the inventory balance for period t is:

inv[i][t] = inv[i][t-1] + x[i][t] - demand[i][t]

But for t=0, inv[i][t-1] is the initial inventory. So for t=0, inv[i][t] = initial_inventory[i] + x[i][0] - demand[i][0]. But that would be the inventory after the order and before the demand. Wait, maybe the order is placed at the beginning of the period, then the demand is subtracted. So the inventory at the end of the period is initial_inventory[i] + x[i][t] - demand[i][t]. So for t=0, the initial inventory is the starting point, and the order is placed in period 0, then demand is subtracted. So the inventory after period 0 is initial_inventory[i] + x[i][0] - demand[i][0].

But for t=1, the inventory at the start of the period is inv[i][0], then order x[i][1] is added, and demand is subtracted. So the equation holds for all t from 0 to 4.

So the constraints for inventory balance would be for each item i and period t in 0 to 4:

inv[i][t] = inv[i][t-1] + x[i][t] - demand[i][t]

But for t=0, inv[i][t-1] is the initial inventory. So for t=0, the equation is inv[i][0] = initial_inventory[i] + x[i][0] - demand[i][0]. Wait, no. Wait, the initial inventory is the starting inventory before any orders in period 0. So the inventory at the end of period 0 is initial_inventory[i] + x[i][0] - demand[i][0]. So inv[i][0] is the end-of-period inventory. So for t=0, the equation is inv[i][0] = initial_inventory[i] + x[i][0] - demand[i][0]. For t >=1, inv[i][t] = inv[i][t-1] + x[i][t] - demand[i][t].

So the inventory balance constraints need to be set up accordingly.

Now, the volume constraint for each period t: sum( inv[i][t] * volume[i] for all i ) <= storage_capacity.

So for each period t in 0 to 4, the total volume used is the sum of each item's inventory in that period multiplied by their volume. This must be <= 99.

Now, the objective function is to minimize the sum of order costs and holding costs. The order cost for item i in period t is unit_order_cost[i] * x[i][t]. The holding cost is holding_cost[i] * inv[i][t]. So the total cost is sum over all i and t of (unit_order_cost[i] * x[i][t] + holding_cost[i] * inv[i][t]).

Now, let's structure the code.

First, import pulp and os.

Then, define the parameters. The JSON parameters are given, so I can parse them into variables.

Then, create the problem. The problem is a minimization problem.

Define the variables. For x and inv. Since the problem has 3 items and 5 periods, the variables will be 3x5 for x and 3x5 for inv.

But in PuLP, variables can be created with loops. For each item and period, create x[i][t] and inv[i][t].

But in Python, it's easier to use lists of lists. So for x, create a 2D list where x[i][t] is the variable for item i in period t.

Similarly for inv.

Then, the objective function is the sum of all order costs and holding costs.

Then, the constraints:

For each item and period, the inventory balance. For t=0, inv[i][0] = initial_inventory[i] + x[i][0] - demand[i][0]. For t>0, inv[i][t] = inv[i][t-1] + x[i][t] - demand[i][t].

But how to model this in PuLP? For each i and t, we can create a constraint that inv[i][t] - inv[i][t-1] - x[i][t] + demand[i][t] = 0. Wait, rearranging the equation:

inv[i][t] = inv[i][t-1] + x[i][t] - demand[i][t]

So inv[i][t] - inv[i][t-1] - x[i][t] + demand[i][t] = 0.

But for t=0, inv[i][t-1] is the initial inventory. So for t=0, the equation becomes inv[i][0] - initial_inventory[i
