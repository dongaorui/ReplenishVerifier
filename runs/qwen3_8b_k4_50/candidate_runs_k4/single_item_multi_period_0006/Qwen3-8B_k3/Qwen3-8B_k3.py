<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem is a single-item, multi-period replenishment. There are 4 periods. The initial inventory is 29. Demands for each period are [51, 60, 35, 28]. The unit order cost is 4, and the holding cost is 4. The task is to formulate and solve a linear inventory-balance model.

First, I need to define the decision variables. The main variables here are the order quantities for each period. Let's call them order[t] for t from 0 to 3 (since there are 4 periods). Also, the inventory after each period needs to be tracked. Maybe I can have inventory[t] representing the inventory at the end of period t.

Wait, the inventory balance equation. For each period, the inventory at the start plus the order minus the demand equals the inventory at the end. But the initial inventory is given, so for period 0, the starting inventory is 29. Then, for each period t, the inventory after the order and before demand is inventory[t] + order[t], and then subtract demand[t] to get inventory[t+1]. Wait, maybe I need to model it as:

At the beginning of period t, the inventory is inv[t]. Then, we place an order of order[t], which is added to the inventory. Then, the demand for the period is subtracted. So the inventory after the period is inv[t] + order[t] - demand[t] = inv[t+1].

But the initial inventory is inv[0] = 29. Then, for each period t from 0 to 3, we have the equation inv[t] + order[t] - demand[t] = inv[t+1]. However, for the last period, t=3, there's no period after, so inv[4] would be zero? Or maybe it's allowed to have leftover inventory. Wait, the problem doesn't specify any constraints on ending inventory, so maybe it's allowed. But the model should account for that.

The objective is to minimize the total cost, which includes ordering costs and holding costs. The ordering cost is unit_order_cost multiplied by the sum of all orders. The holding cost is holding_cost multiplied by the sum of the inventory levels at the end of each period. Wait, or is it the average inventory? Wait, the problem says "holding cost" which is typically per unit per period. So, for each period, the holding cost is holding_cost multiplied by the inventory at the end of the period. So the total holding cost is sum over all periods of holding_cost * inv[t].

So the objective function is: minimize (sum(order[t] * unit_order_cost for t in periods) + sum(inv[t] * holding_cost for t in periods)).

Now, the variables: order[t] must be >=0, and inv[t] must be >=0. Also, the inventory balance equations must hold.

So, the steps are:

1. Create the PuLP problem.
2. Define the decision variables: order for each period, and inventory for each period.
3. Add constraints for the inventory balance.
4. Add non-negativity constraints.
5. Define the objective function.
6. Solve and print the results.

Let me think about the variables. Since there are 4 periods, the order variables are for periods 0 to 3. Similarly, inventory variables are for periods 0 to 3 (since inv[0] is initial inventory, and inv[4] would be the end inventory, but maybe not needed? Wait, the inventory balance equation for period t is inv[t] + order[t] - demand[t] = inv[t+1]. So for t=0, inv[0] is 29, then inv[1] = inv[0] + order[0] - demand[0]. Similarly for t=1, inv[2] = inv[1] + order[1] - demand[1], etc. So the inventory variables are inv[0], inv[1], inv[2], inv[3], inv[4]. Wait, but inv[4] is the inventory after period 3. However, the problem doesn't mention any constraints on inv[4], so it's allowed to be positive.

But in the objective function, the holding cost is for each period's inventory. So for each period t (from 0 to 3?), or from 0 to 4? Wait, the problem says "holding cost" for each period. Let me check the problem statement again. The problem says "holding cost: 4". The task is to formulate a linear inventory-balance model. So the holding cost is likely per unit per period. So for each period, the inventory at the end of the period (inv[t]) is multiplied by the holding cost. So for t from 0 to 3, inv[t] is the inventory after the period. Wait, no. Let me think again.

The inventory balance equation is:

At the start of period t, the inventory is inv[t]. Then, order[t] is added, then demand[t] is subtracted. So the inventory at the end of the period is inv[t] + order[t] - demand[t] = inv[t+1]. So for t=0, inv[0] is initial inventory (29). Then, inv[1] is the inventory after period 0. Then, inv[1] is the starting inventory for period 1. So the holding cost for period t is the inventory at the end of the period, which is inv[t]. Wait, no. The holding cost is for the inventory that is held during the period. So if the inventory at the end of the period is inv[t], then during the period, the inventory was inv[t] (after the order and before the demand). Wait, maybe I need to model the holding cost as the inventory after the order and before the demand. Or is it the inventory after the demand?

This is a bit ambiguous. Let me think. Typically, in inventory models, the holding cost is based on the inventory held during the period. So if you order in period t, then the inventory is increased by the order, and then the demand is subtracted. The holding cost for the period would be the average inventory during the period. But since the problem says "holding cost" without specifying, perhaps it's the inventory at the end of the period. Or maybe the problem assumes that the holding cost is applied to the inventory after the order and before the demand. However, the problem statement says "holding cost" and the example parameters are given. Let me check the problem statement again.

The problem says "holding cost: 4". The task is to formulate a linear inventory-balance model. The standard model for this is the Economic Order Quantity (EOQ) model, but for multiple periods. The standard model includes ordering cost and holding cost. The holding cost is typically based on the average inventory during the period. However, in some models, it's based on the ending inventory. But since the problem doesn't specify, perhaps the model should use the ending inventory. Alternatively, maybe the problem expects the holding cost to be applied to the inventory after the order and before the demand. Wait, but the problem says "inventory-balance model", which usually refers to the balance between inventory, orders, and demand.

Alternatively, perhaps the holding cost is applied to the inventory at the end of the period. For example, in the model, the holding cost is the sum of inv[t] * holding_cost for t in 0 to 3. Because inv[t] is the inventory after the order and before the demand. Wait, no. Let me think again.

The inventory balance equation is:

inv[t] + order[t] - demand[t] = inv[t+1]

So inv[t] is the inventory at the beginning of period t. Then, order[t] is added, and demand[t] is subtracted. So the inventory at the end of period t is inv[t+1]. Therefore, during period t, the inventory starts at inv[t], and ends at inv[t+1]. The average inventory during the period would be (inv[t] + inv[t+1])/2. However, if the problem uses the ending inventory as the holding cost, then it's inv[t+1] for each period. But the problem says "holding cost" and the parameters are given. Let me check the problem's parameters again.

The problem says "holding cost: 4". The task is to formulate a linear model. The standard approach for such problems is to have the holding cost as the sum of the ending inventory for each period multiplied by the holding cost. So for each period t, the holding cost is inv[t+1] * holding_cost. But since inv[0] is the initial inventory, which is not part of any period's holding cost. Wait, no. Let me think again.

The initial inventory is 29. That's the inventory at the beginning of period 0. Then, during period 0, the order is placed, and the demand is met. The inventory at the end of period 0 is inv[1]. So the holding cost for period 0 is inv[1] * holding_cost. Similarly, for period 1, the holding cost is inv[2] * holding_cost. So the total holding cost is sum over t=0 to 3 of inv[t+1] * holding_cost. But inv[4] is the ending inventory after period 3. However, the problem may not have any constraints on inv[4], so it's allowed to be positive.

But the problem's parameters don't specify whether the holding cost
