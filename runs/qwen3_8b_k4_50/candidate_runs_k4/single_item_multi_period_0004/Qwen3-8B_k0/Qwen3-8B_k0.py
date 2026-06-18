<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem is about planning the replenishment of a single item over 4 periods. The initial inventory is 17, and the demands for each period are [30, 25, 44, 39]. The goal is to minimize the total cost, which includes order costs and holding costs. The order cost is 3 per order, and the holding cost is 2 per unit held.

First, I need to define the decision variables. The main variables here are the order quantities for each period and the inventory levels at the end of each period. Let me think: for each period, we need to decide how much to order. Also, the inventory after each period must satisfy the demand of that period.

Let me break it down. Let's denote the order quantity in period t as Q_t. The inventory at the start of period t is I_{t-1} (initial inventory is 17, so I_0 = 17). Then, the inventory after meeting demand in period t would be I_t = I_{t-1} + Q_t - D_t. But wait, the demand must be met, so the inventory after ordering and before demand is I_{t-1} + Q_t, and then after demand, it's I_{t-1} + Q_t - D_t. But the problem says to use inventory-balance constraints, so I need to model that.

Wait, the problem says to use inventory-balance constraints. So for each period, the inventory at the end of the period (after demand) must equal the initial inventory plus the order quantity minus the demand. So for each period t (from 1 to T), the inventory balance is:

I_t = I_{t-1} + Q_t - D_t

But I need to make sure that the inventory can't be negative. Wait, the problem doesn't mention any constraints on inventory levels being non-negative, but in reality, you can't have negative inventory. However, the problem might assume that the order quantity is sufficient to meet demand. But maybe the model should include that constraint. Wait, the problem statement doesn't specify, so perhaps it's allowed to have negative inventory? Or maybe the model implicitly ensures that by the constraints. Hmm, but in practice, you can't have negative inventory. So perhaps the model should include that the inventory after demand is non-negative. However, the problem statement doesn't mention this. Let me check the problem again.

The problem says "inventory-balance constraints" but doesn't mention non-negativity. However, in real-world scenarios, inventory can't be negative. But since the problem doesn't specify, maybe we can assume that the order quantity is sufficient to meet demand. However, to be safe, maybe I should include the constraint that the inventory after demand is non-negative. But the problem might not require that. Let me check the parameters again. The initial inventory is 17, and the first demand is 30. So in period 1, the initial inventory is 17. If we order Q_1, then after adding Q_1, the inventory before demand is 17 + Q_1. Then, after demand, it's 17 + Q_1 - 30. This must be >= 0? Or is it allowed to be negative? The problem doesn't specify, but since the holding cost is applied to the inventory, perhaps negative inventory would imply a shortage, which isn't considered here. Therefore, the model should ensure that the inventory after demand is non-negative. So I need to add constraints that I_t >= 0 for all t.

Wait, but the problem says "inventory-balance constraints" which might refer to the balance equation, not the non-negativity. However, the problem might not require that. But given that the holding cost is 2 per unit, perhaps the model should have non-negative inventory. Otherwise, if inventory is negative, that would imply a shortage, which isn't accounted for here. Therefore, I should include the non-negativity constraints on the inventory levels.

So, the variables are:

- Q_t: order quantity in period t (t=1 to 4)
- I_t: inventory after demand in period t (t=0 to 4, where I_0 is initial inventory 17)

Wait, I_0 is the initial inventory. Then, for each period t (from 1 to 4), the inventory balance is:

I_t = I_{t-1} + Q_t - D_t

But I_0 is given as 17. So for t=1, I_1 = I_0 + Q_1 - D_1.

But the problem is to minimize the total cost, which includes order costs and holding costs. The order cost is 3 per order, so for each period where Q_t > 0, we have a cost of 3. Wait, but the problem says "unit_order_cost" is 3. Wait, the problem says "Minimize order cost 3 and holding cost 2". Wait, the problem says "order cost 3" which might mean that each order incurs a fixed cost of 3, regardless of the quantity. So if you order in a period, you pay 3. So the order cost is a fixed cost per order, not per unit. So the total order cost is the sum over all periods of (if Q_t > 0, then 3 else 0). But how to model that in PuLP? Because PuLP can't directly handle if-conditions. So perhaps we need to model it as a binary variable indicating whether an order is placed in period t, and then multiply by the unit order cost. But that might complicate things. Alternatively, since the problem says "unit_order_cost" is 3, maybe it's a per-unit cost? Wait, the problem says "Minimize order cost 3 and holding cost 2". Wait, the problem might have a typo. Let me check the parameters again.

The parameters are:

"unit_order_cost": 3,

"holding_cost": 2

So the unit_order_cost is 3 per unit ordered? Or is it a fixed cost per order? The problem says "order cost 3" which is ambiguous. But given that the problem says "unit_order_cost", it's more likely that it's a per-unit cost. Wait, but that would be unusual. Typically, order cost is a fixed cost per order, not per unit. However, the problem's wording is unclear. Let me re-examine the problem statement.

The problem says: "Minimize order cost 3 and holding cost 2 using inventory-balance constraints."

So the total cost is the sum of order costs and holding costs. The order cost is 3 per order, and holding cost is 2 per unit held. So if you order in a period, you pay 3, regardless of the quantity. So for example, if you order 10 units in period 1, you pay 3. If you order 0, you pay 0. So the order cost is a fixed cost per order, not per unit. Therefore, the total order cost is the sum over all periods of (if Q_t > 0, then 3 else 0). But how to model that in PuLP?

Alternatively, maybe the problem is that the order cost is 3 per unit ordered. That would make the total order cost sum(Q_t * 3). But the problem says "order cost 3", which is ambiguous. However, given that the problem provides "unit_order_cost" as 3, perhaps it's per unit. Wait, but the problem says "Minimize order cost 3 and holding cost 2". So maybe the order cost is a fixed cost of 3 per order, and the holding cost is 2 per unit. So for example, if you order in period t, you pay 3, and for each unit held in inventory, you pay 2. So the total cost is sum(3 * (Q_t > 0)) + sum(2 * I_t).

But how to model that in PuLP? Because PuLP can't directly handle the (Q_t > 0) condition. So we need to model it with binary variables. Let me think. For each period t, we can have a binary variable y_t which is 1 if Q_t > 0, 0 otherwise. Then the order cost is sum(3 * y_t). But then we need to link y_t with Q_t. For example, Q_t >= y_t * epsilon, where epsilon is a small positive number (like 1), to ensure that if y_t is 1, then Q_t is at least 1. But this requires introducing binary variables, which complicates the model. However, the problem might not require that. Maybe the problem assumes that the order cost is per unit ordered. Let me check the problem again.

The problem says "unit_order_cost": 3. So that suggests that the cost is per unit ordered. So the total order cost is sum(Q_t * 3). Then the holding cost is sum(I_t * 2). So the total cost is sum(3 * Q_t) + sum(2 * I_t). That seems more straightforward. So the problem is to minimize the sum of order costs (per unit) and holding costs (per unit). So that would make sense. Let me proceed with that assumption.

So the objective function is:

Total cost = sum_{t=1 to T} (3 * Q_t) + sum_{t=0 to T} (2 * I_t)

Wait, but I
