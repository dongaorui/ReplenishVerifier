<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem. Let me start by understanding the problem details.

The problem has 4 periods. The initial inventory is 29. Demands for each period are [51, 60, 35, 28]. The unit order cost is 4, and holding cost is 4. The task is to formulate a linear inventory-balance model.

First, I need to define the decision variables. For each period, there's an order quantity, which I'll call 'order' variables. Also, the inventory after each period needs to be tracked. Wait, but maybe the inventory after each period is a state variable. Let me think.

In inventory models, the key is to balance the inventory from the previous period, plus the order, minus the demand, equals the inventory for the next period. So, for each period, the inventory level must satisfy the demand. Also, the order quantity can't be negative.

So, the decision variables would be the order quantities for each period. Let's denote them as order[t] for t in 0 to 3 (since there are 4 periods). Also, the inventory after each period (including the initial) would be a variable, but maybe we can express it in terms of the orders and demands.

Wait, the initial inventory is 29. Let's index periods from 0 to 3. For each period t, the inventory at the start is inv[t], and after ordering, it's inv[t] + order[t] - demand[t] = inv[t+1]. But for the first period, inv[0] is the initial inventory. So, the constraints would be:

For each period t from 0 to 3:
inv[t] + order[t] - demand[t] = inv[t+1]

But inv[0] is given as 29. Also, the order quantities can't be negative. So, order[t] >= 0 for all t.

The objective is to minimize the total cost, which includes the order costs and holding costs. The order cost is unit_order_cost * order[t] for each period. The holding cost is holding_cost * inv[t] for each period. Wait, but inv[t] is the inventory after the order and before the demand? Or after the demand? Wait, the holding cost is typically for the inventory carried over to the next period. Let me think again.

In the inventory balance equation, inv[t] is the inventory at the start of period t. Then, during the period, you order order[t], which is added to the inventory. Then, the demand is subtracted. The remaining inventory is inv[t+1]. So, the holding cost for period t would be the inventory at the start of the period (inv[t]) multiplied by the holding cost. Wait, no. Because the holding cost is for the inventory that is carried over. So, if you have inv[t] at the start of the period, that's the inventory that was carried over from the previous period. So, the holding cost for that inventory would be applied. But maybe the holding cost is applied to the inventory after the order and before the demand. Wait, this depends on the model's specifics. Let me check the problem statement again.

The problem says "linear inventory-balance model". Typically, in such models, the holding cost is based on the inventory at the end of the period. Wait, no. Let me think of the standard model. The standard model for inventory replenishment with holding and ordering costs would have the following:

For each period t:

Inventory at the beginning of the period (inv[t]) + order[t] - demand[t] = inventory at the end of the period (inv[t+1]).

The cost components are:

- Ordering cost: unit_order_cost * order[t] for each t.

- Holding cost: holding_cost * inv[t+1] for each t. Because the inventory at the end of the period is carried over to the next period. Wait, but maybe the holding cost is applied to the inventory at the end of the period. So, for each period, the holding cost is based on the inventory after the order and before the demand. Wait, no. Let me think again.

Suppose inv[t] is the inventory at the start of period t. Then, during the period, you order order[t], which is added to inv[t], then the demand is subtracted. The remaining inventory is inv[t+1]. So, the holding cost for the inventory that was carried over from the previous period (inv[t]) would be applied. But maybe the holding cost is for the inventory that is held during the period. So, if you have inv[t] at the start, and then you order order[t], then the total inventory before demand is inv[t] + order[t]. Then, after demand, it's inv[t] + order[t] - demand[t] = inv[t+1]. The holding cost would be for the inventory that is held during the period. So, perhaps the holding cost is applied to inv[t] + order[t] - demand[t] (which is inv[t+1])? Or is it applied to inv[t]?

This is a bit ambiguous. However, the problem statement says "holding cost" which is typically per unit of inventory held. In many models, the holding cost is based on the inventory at the end of the period. For example, in the Economic Order Quantity (EOQ) model, the holding cost is based on the average inventory. But in a multi-period model, the holding cost for each period is the inventory at the end of the period. Wait, no. Let me think of the standard model.

In the standard model, the holding cost for period t is the inventory at the end of the period (inv[t+1]) multiplied by the holding cost. Because that's the inventory that is carried over to the next period. So, the total holding cost would be sum over t of holding_cost * inv[t+1].

But the problem statement says "holding cost" without specifying, so I need to make an assumption. Let me check the problem's parameters again. The problem says "holding cost: 4". So, the model needs to include holding cost for each period. Let me proceed with the assumption that the holding cost is applied to the inventory at the end of the period. So, for each period t, the holding cost is holding_cost * inv[t+1].

But wait, the initial inventory is 29. So, inv[0] is 29. Then, for period 0, the inventory after order and before demand is inv[0] + order[0], then after demand, it's inv[0] + order[0] - demand[0] = inv[1]. So, the holding cost for period 0 would be inv[1] * holding_cost. Similarly for other periods.

So, the total cost is sum over t=0 to 3 of (unit_order_cost * order[t] + holding_cost * inv[t+1]).

But wait, the initial inventory is 29, which is inv[0]. Then, inv[1] is inv[0] + order[0] - demand[0]. So, the holding cost for period 0 is inv[1] * holding_cost. For period 1, it's inv[2] * holding_cost, etc.

So, the objective function is to minimize the sum of order costs and holding costs.

Now, the decision variables are the order quantities for each period, and the inventory levels. However, since the inventory levels can be expressed in terms of the orders and demands, perhaps we can model them as variables or express them in terms of the orders.

But in PuLP, it's easier to model the inventory levels as variables. Let me think. Let's define inv as a list of variables, where inv[t] is the inventory at the start of period t. Then, for each period t, the constraint is:

inv[t] + order[t] - demand[t] = inv[t+1]

With inv[0] = initial_inventory.

But since inv[0] is known, we can set it as a constant. So, inv[0] = 29.

But in PuLP, variables can be defined for inv[0], inv[1], inv[2], inv[3], inv[4]. Wait, since there are 4 periods, the inventory after period 4 (inv[4]) would be zero? Or not necessarily. Wait, the problem doesn't specify any end-of-horizon constraints. So, inv[4] can be any non-negative value. But in practice, it's possible that the model allows for leftover inventory. However, the problem doesn't mention any constraints on that. So, we can proceed.

So, the variables are:

order[t] for t in 0..3 (each order quantity)

inv[t] for t in 0..4 (inventory at the start of period t)

But inv[0] is fixed as 29. So, we can set inv[0] as a constant, and the rest as variables.

But in PuLP, variables can be defined as such. Let me outline the steps.

First, create the problem.

Then, define variables:

order = [LpVariable(f"order_{t}", lowBound=0) for t in 0..3]

inv = [LpVariable(f"inv_{t}", lowBound=0) for t in 0..4]

But inv[0] is fixed as 29. So, we can set inv[0] as a constant. Wait, but in PuLP, variables can't be fixed unless we set their value. Alternatively,
