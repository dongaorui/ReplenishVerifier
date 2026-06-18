import pulp and os. Then, create the problem. 

The decision variables are the order quantities for each period. Let's say order_vars is a list of variables, one for each period. 

Then, the inventory variables can be calculated based on the previous inventory and the order. But since we need to track the inventory levels, maybe we can create a list of inventory variables. 

Wait, but the inventory after period t is the initial inventory plus the sum of orders up to t minus the sum of demands up to t. Wait, no. Because each order is added in the period, and the demand is subtracted. So, the ending inventory after period t is initial_inventory + sum_{i=1}^t order[i] - sum_{i=1}^t demand[i]. 

But that's equivalent to the recursive formula. So, for each period t, the ending inventory is the previous ending inventory plus order[t] minus demand[t]. 

But perhaps it's easier to model the inventory as a variable for each period. Let me think. For example, inv[0] = initial_inventory. Then, for each t in 1 to 4:

inv[t] = inv[t-1] + order[t] - demand[t]

But inv[t] must be >= 0. 

So, in PuLP, we can create variables for inv[1], inv[2], inv[3], inv[4]. Then, for each t, we add a constraint that inv[t] = inv[t-1] + order[t] - demand[t]. 

But how to handle inv[0]? Since inv[0] is fixed, we can use that in the constraints. 

So, the steps would be:

1. Define the periods (4 periods).
2. Define the initial inventory (25).
3. Define the demand for each period.
4. Create variables for order quantities (order_vars) for each period.
5. Create variables for inventory levels (inv_vars) for each period (from 1 to 4).
6. Add constraints for the inventory balance equations.
7. Add constraints that inventory levels are non-negative.
8. The objective is to minimize the sum of ordering costs (sum(order_vars * unit_order_cost)) plus holding costs (sum(inv_vars * holding_cost)).

Wait, but the holding cost is per unit of inventory at the end of the period. So, for each period t, the holding cost is inv[t] * holding_cost. 

So, the total cost is sum(order_vars * unit_order_cost) + sum(inv_vars * holding_cost).

But wait, the holding cost is for the inventory carried over. So, the inv_vars are the ending inventory for each period. So, the holding cost is for each period's ending inventory. 

So, the objective function is sum(order_vars * unit_order_cost) + sum(inv_vars * holding_cost).

Now, let's think about the variables. 

The order_vars are for each period, so for periods 1 to 4. 

The inv_vars are for periods 1 to 4. 

But inv[0] is initial_inventory, which is fixed. 

So, for each t in 1 to 4:

inv[t] = inv[t-1] + order[t] - demand[t]

But inv[0] is 25. 

So, in code:

We can create a list for inv_vars, say inv = [None] * (periods + 1). inv[0] is 25. Then, for t in 1 to periods:

inv[t] = inv[t-1] + order[t] - demand[t-1] ?

Wait, the demand for period t is demand[t-1] if the list is 0-indexed. Let me check the parameters. The demand is given as [58, 42, 53, 19], which is for periods 1 to 4. So, for period 1, demand is 58, which is index 0 in the list. So, for t in 1 to 4, demand[t-1] is the demand for that period. 

So, the constraint for inv[t] would be:

inv[t] = inv[t-1] + order[t] - demand[t-1]

But in PuLP, how to model this. For each t in 1 to 4, we can create a constraint that links inv[t] to inv[t-1], order[t], and demand[t-1]. 

But since inv[t] is a variable, and inv[t-1] is a variable (for t >=1), except for inv[0] which is fixed. 

So, for each t in 1 to 4:

prob += inv[t] == inv[t-1] + order[t] - demand[t-1]

But inv[0] is fixed as 25. 

So, the code would need to create variables for inv[1], inv[2], inv[3], inv[4], and order[1], order[2], order[3], order[4]. 

Wait, but the order variables are for each period. So, for period 1, order[1] is the order quantity. 

So, the variables:

order_vars = [pulp.LpVariable(f"order_{t}", lowBound=0) for t in range(1, periods+1)]

inv_vars = [pulp.LpVariable(f"inv_{t}", lowBound=0) for t in range(1, periods+1)]

But then, for each t in 1 to 4:

inv[t] = inv[t-1] + order[t] - demand[t-1]

But inv[0] is 25. 

So, the constraints would be:

for t in 1 to 4:

prob += inv_vars[t-1] == inv_vars[t-2] + order_vars[t-1] - demand[t-1]

Wait, maybe I need to index properly. Let me think again. 

Let me use 0-based indices for the variables. Let's say periods is 4. 

For t in 0 to 3 (since periods is 4), the period
