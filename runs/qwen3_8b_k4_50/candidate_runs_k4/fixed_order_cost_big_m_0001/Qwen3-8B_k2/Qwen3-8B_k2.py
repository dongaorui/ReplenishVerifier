<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem statement thoroughly.

The problem involves ordering inventory over multiple periods. Each order has a variable unit cost and a fixed activation cost. The goal is to minimize the total cost, which includes ordering costs, holding costs, and fixed costs. The model needs binary variables to indicate whether an order is placed in a period. Also, there's a Big-M value provided, which I should use in the constraints.

First, let me list out the parameters given. The initial inventory is 15. The demands for each of the 6 periods are [55, 51, 27, 60, 59, 39]. The unit order cost is 4, holding cost is 2, fixed order cost is 29, and Big-M is 291.

The decision variables I need to define are:
- Order quantity variables for each period. Let's call them order_q, which is a continuous variable for each period.
- Binary variables to indicate if an order is placed in a period. Let's call them order_binary, which is 1 if an order is placed, 0 otherwise.

Wait, but the problem says that the fixed cost is incurred if an order is placed. So the binary variables will determine whether the fixed cost is added. Also, the order quantity must be zero if the binary is zero, and non-zero if the binary is one. But how to link them? That's where the Big-M comes into play.

The constraints will include:
1. Inventory balance for each period. The inventory at the start of the period plus the order quantity minus the demand equals the inventory at the end of the period.
2. The order quantity must be zero if the binary is zero. This can be modeled using the Big-M method. For each period, order_q <= M * order_binary. Since M is given as 291, which is larger than the maximum possible order quantity (since the maximum demand is 60, but maybe the Big-M is set to a higher value to ensure it's safe).
3. The order quantity can't be negative. So order_q >= 0.
4. The initial inventory is 15, so the first period's inventory starts with that.

Let me think about the variables. Let's define:

- For each period t (from 0 to 5), we have:
   - order_q[t]: the quantity ordered in period t.
   - order_binary[t]: binary variable indicating if an order is placed in period t.

The inventory levels can be tracked as a variable, say inventory[t], which represents the inventory at the end of period t. Wait, but the inventory at the start of period t is inventory[t-1], and then after ordering and meeting demand, it becomes inventory[t].

Wait, the initial inventory is 15, which is the inventory at the start of period 0. Then, for each period, the inventory after ordering and before demand is inventory[t] = inventory[t-1] + order_q[t]. Then, after meeting demand, inventory[t] = inventory[t] - demand[t]. Wait, no. Let me clarify:

The inventory at the start of period t is inv_start[t]. Then, we order order_q[t], so the inventory after ordering is inv_start[t] + order_q[t]. Then, the demand for period t is subtracted, so the inventory at the end of period t is inv_end[t] = inv_start[t] + order_q[t] - demand[t]. But inv_start[t+1] = inv_end[t].

So, for the first period (t=0), inv_start[0] = initial_inventory = 15. Then, inv_end[0] = 15 + order_q[0] - demand[0]. Then, inv_start[1] = inv_end[0], and so on.

But in the model, we need to track the inventory levels. So perhaps we can define inventory as a variable for each period, representing the inventory at the end of that period. Then, the constraint for each period t (except t=0) would be:

inventory[t] = inventory[t-1] + order_q[t] - demand[t]

But for t=0, inventory[0] = initial_inventory + order_q[0] - demand[0].

Wait, no. Let me think again. The initial inventory is the inventory at the start of period 0. Then, during period 0, we order order_q[0], so the inventory after ordering is initial_inventory + order_q[0]. Then, after meeting the demand of 55, the inventory at the end of period 0 is initial_inventory + order_q[0] - demand[0]. That's inventory[0].

Then, for period 1, the inventory at the start is inventory[0], and so on.

So, for each period t (from 0 to 5), the inventory at the end of the period is:

inventory[t] = inventory[t-1] + order_q[t] - demand[t]

But for t=0, inventory[-1] is the initial inventory. So, we can model this with a loop.

Now, the objective function is to minimize the total cost, which includes:

- Variable order costs: sum over all periods (unit_order_cost * order_q[t])
- Fixed order costs: sum over all periods (fixed_order_cost * order_binary[t])
- Holding costs: sum over all periods (holding_cost * inventory[t])

Wait, but the holding cost is applied to the inventory at the end of the period. Because the inventory is held during the period. So yes, the holding cost is based on the inventory at the end of each period.

So the total cost is:

Total cost = sum (unit_order_cost * order_q[t]) + sum (fixed_order_cost * order_binary[t]) + sum (holding_cost * inventory[t]) for all t in 0..5.

Now, the constraints:

1. For each period t, inventory[t] = inventory[t-1] + order_q[t] - demand[t], with inventory[-1] = initial_inventory.

But since inventory is a variable, we need to model this as a constraint. For t >= 1, inventory[t] = inventory[t-1] + order_q[t] - demand[t]. For t=0, inventory[0] = initial_inventory + order_q[0] - demand[0].

But how to model this in PuLP? We can create a list of inventory variables, say inv = [LpVariable("inv_{}".format(t), ...) for t in 0..5]. Then, for each t in 0 to 5:

if t == 0:
   inv[0] = initial_inventory + order_q[0] - demand[0]
else:
   inv[t] = inv[t-1] + order_q[t] - demand[t]

But in PuLP, we can't directly assign equations like that. Instead, we need to create constraints for each of these equations.

So for each t in 0 to 5:

if t == 0:
   prob += inv[t] == initial_inventory + order_q[t] - demand[t]
else:
   prob += inv[t] == inv[t-1] + order_q[t] - demand[t]

But wait, the initial inventory is 15. So for t=0, the equation is inv[0] = 15 + order_q[0] - demand[0].

But in PuLP, variables can't be directly assigned like that. So we need to create constraints for each of these equations.

Another thing: the order_q[t] must be non-negative. Also, the order_binary[t] is a binary variable. And the order_q[t] must be zero if order_binary[t] is zero. This is where the Big-M comes in.

The constraint for order_q[t] is:

order_q[t] <= M * order_binary[t]

Because if order_binary[t] is 0, then order_q[t] must be 0. Since M is 291, which is larger than any possible order quantity (since the maximum demand is 60, but maybe the Big-M is set to a higher value to ensure that even if the order quantity is larger than the demand, it's allowed. Wait, but the problem says that the Big-M value is 291. So we need to use that.

So for each period t, we add the constraint:

order_q[t] <= big_m * order_binary[t]

Additionally, since order_q[t] can't be negative, we have order_q[t] >= 0.

Now, putting all together.

Let me outline the steps:

1. Import pulp and os.

2. Define the parameters from the JSON.

3. Create the LpProblem instance.

4. Define the decision variables:

   - order_q: list of continuous variables for each period.
   - order_binary: list of binary variables for each period.
   - inventory: list of continuous variables for each period.

5. Add constraints for inventory balance.

6. Add constraints linking order_q and order_binary via Big-M.

7. Add constraints for non-negativity of order_q.

8. Define the objective function as the sum of variable costs, fixed costs, and holding costs.

9. Solve the problem.

10. Print the status and objective value.

Now, let's think about the code structure.

First, the function build_model() returns the LpProblem object. The main block calls build_model(), checks for the environment variable, writes the LP if needed, solves, and prints the results.

So, inside build_model(), we need to create the problem, define variables, add constraints, and set
