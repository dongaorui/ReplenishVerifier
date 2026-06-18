<think>
Okay, I need to create a Python program using PuLP to solve this multi-item capacity-constrained replenishment problem. Let me start by understanding the problem.

First, the problem has 4 items over 3 periods. Each period, there's demand for each item, initial inventory, and we have to decide how much to order each period. The constraints are the storage capacity and the volume per item. The objective is to minimize total costs, which include ordering and holding costs.

Let me think about the decision variables. For each item and period, I need to decide the order quantity. Let's denote that as x[i][t], where i is the item index and t is the period. Also, the inventory after each period must be calculated. The inventory starts with initial inventory, then subtracts demand and adds orders. But since orders are placed at the beginning of the period, the inventory after the period would be previous inventory minus demand plus order. Wait, maybe I need to model the inventory level at the end of each period. Let me think.

The inventory at the end of period t for item i is initial_inventory[i] + sum of orders from previous periods up to t, minus the sum of demands up to t. Wait, no. Let me clarify:

For each item i, the inventory at the start of period t is initial_inventory[i] plus the sum of orders in periods before t. Then, during period t, demand is subtracted. So the inventory after period t is (initial_inventory[i] + sum_{s=1 to t} order[s][i]) - sum_{s=1 to t} demand[s][i]. But since the order is placed at the beginning of the period, the inventory after the order is added, then demand is subtracted. So the inventory after period t is (initial_inventory[i] + sum_{s=1 to t} order[s][i]) - sum_{s=1 to t} demand[s][i]. But this must be non-negative, right? Wait, the problem doesn't mention any constraints on inventory levels being non-negative, but maybe that's implied. However, the problem statement doesn't specify, so perhaps we don't need to include that. Wait, but the storage capacity is a constraint. So the total inventory across all items at the end of each period can't exceed the storage capacity. Wait, no. The storage capacity is a total capacity. So the sum of all items' inventory at the end of each period must be <= storage_capacity. Wait, but the problem says "capacity" is 104. So the total inventory across all items at the end of each period can't exceed 104. Or is it the capacity per period? The problem says "capacity" as a single value, so I think it's the total capacity. So for each period, the sum of the inventory levels of all items at the end of that period must be <= 104.

Wait, but the problem says "storage capacity" is 104. So the total inventory across all items at the end of each period can't exceed 104. So for each period t, sum_{i=1 to 4} (inventory[i][t]) <= 104.

But how is the inventory calculated? Let's think again. For each item i, the inventory after period t is:

inventory[i][t] = initial_inventory[i] + sum_{s=1 to t} order[i][s] - sum_{s=1 to t} demand[i][s]

But since the initial inventory is given, and for each period, the order is placed, then the inventory after that period is updated. However, the storage capacity applies to the total inventory across all items at the end of each period. So for each period t, the sum over all items of their inventory at the end of period t must be <= 104.

But wait, the problem says "capacity" is 104. So that's the total capacity. So the sum of all items' inventory at the end of each period must be <= 104.

So the constraints are:

For each period t (from 1 to 3), sum_{i=1 to 4} (inventory[i][t]) <= 104.

But how to model the inventory[i][t]?

Alternatively, maybe the storage capacity is the total capacity at the end of each period. So for each period, the sum of the inventory levels of all items at the end of that period must not exceed 104.

So the first step is to model the inventory levels for each item and period.

But how to compute that? Let's think about the variables. For each item i and period t, the order quantity x[i][t]. Then, the inventory after period t for item i is:

inv[i][t] = initial_inventory[i] + sum_{s=1 to t} x[i][s] - sum_{s=1 to t} demand[i][s]

But since the initial inventory is given, and for each period, the order is added, then the demand is subtracted. However, the inventory after period t is the inventory after the order is placed and the demand is met. So for the first period, the inventory after period 1 is initial_inventory[i] + x[i][1] - demand[i][1].

But the problem is that the inventory after period t is needed for the next period's calculation. However, since the problem is over 3 periods, and the storage capacity applies to each period's end, we need to model the inventory for each period.

But how to model this in PuLP? Let's think about the variables. For each item i and period t, the order quantity x[i][t]. Then, for each item i and period t, the inventory after period t is:

inv[i][t] = initial_inventory[i] + sum_{s=1 to t} x[i][s] - sum_{s=1 to t} demand[i][s]

But since the storage capacity applies to the sum of inv[i][t] across all items for each period t, we need to model that.

But how to compute inv[i][t] in PuLP? Because for each t, inv[i][t] depends on the sum of x[i][s] from s=1 to t. So for each item i and period t, inv[i][t] is a variable? Or can we compute it as an expression?

Alternatively, perhaps we can model the inventory as a variable for each item and period. But that might complicate things. Alternatively, we can compute the inventory as an expression based on the order variables and the demand.

But in PuLP, we can't directly compute expressions for constraints unless they are linear. So perhaps we can model the inventory as a variable, but that might be complex. Alternatively, we can express the constraints in terms of the order variables and the demand.

Let me think again. The storage capacity constraint for period t is:

sum_{i=1 to 4} (initial_inventory[i] + sum_{s=1 to t} x[i][s] - sum_{s=1 to t} demand[i][s]) ) <= 104

But this is for each period t. So for each t, the sum over all items of (initial_inventory[i] + sum_{s=1 to t} x[i][s] - sum_{s=1 to t} demand[i][s]) ) <= 104.

But this can be rewritten as:

sum_{i=1 to 4} (initial_inventory[i] - sum_{s=1 to t} demand[i][s]) + sum_{i=1 to 4} sum_{s=1 to t} x[i][s] <= 104

But the first part is a constant for each t, and the second part is the sum of orders up to period t for all items.

But perhaps this is manageable. Let me think about the objective function. The objective is to minimize the total cost, which includes the unit order costs and the holding costs.

The unit order cost is for each order placed. So for each item i and period t, the cost is unit_order_cost[i] * x[i][t]. The holding cost is for each item i and period t, the holding cost per unit times the inventory at the end of period t. Wait, but the holding cost is per unit per period. So for each item i and period t, the holding cost is holding_cost[i] * inv[i][t]. But inv[i][t] is the inventory at the end of period t. So the total holding cost is sum over all items and periods of holding_cost[i] * inv[i][t].

So the objective function is:

sum_{i=1 to 4} sum_{t=1 to 3} (unit_order_cost[i] * x[i][t]) + sum_{i=1 to 4} sum_{t=1 to 3} (holding_cost[i] * inv[i][t])

But inv[i][t] is initial_inventory[i] + sum_{s=1 to t} x[i][s] - sum_{s=1 to t} demand[i][s]

So substituting that into the objective function:

sum_{i=1 to 4} sum_{t=1 to 3} (unit_order_cost[i] * x[i][t]) + sum_{i=1 to 4} sum_{t=1 to 3} (holding_cost[i] * (initial_inventory[i] + sum_{s=1 to t} x[i][s] - sum_{s=1 to t} demand[i][s]))

But this seems complex. However, in PuLP, we can model this by
