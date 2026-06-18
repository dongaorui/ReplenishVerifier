<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem with fixed order costs and the Big-M method. Let me start by understanding the problem.

First, the firm has a 4-period horizon. They start with 20 units of inventory. The demands for each period are [55, 32, 48, 46]. The costs are unit_order_cost=2, holding_cost=3, and fixed_order_cost=48. The Big-M value is given as 181. The goal is to minimize the total cost, which includes ordering, holding, and fixed setup costs.

So, the model needs to decide how much to order each period and manage inventory levels. Since there's a fixed cost whenever an order is placed, we need binary variables to indicate if an order is placed in a period. The Big-M method is used to model the fixed costs, which is a common approach in mixed-integer programming.

Let me outline the decision variables. For each period, we'll have:

- Order quantity (let's say o_t) which is the amount ordered in period t.
- Binary variable (say, y_t) which is 1 if an order is placed in period t, 0 otherwise.

But wait, the fixed cost is incurred whenever an order is placed, regardless of the quantity. So, the fixed cost is fixed_order_cost * y_t for each period t.

The objective function will be the sum of:

- Unit order cost * o_t for each period (since each unit ordered costs 2)
- Holding cost * (inventory at end of period t) for each period (since holding cost is 3 per unit)
- Fixed order cost * y_t for each period (48 per order)

But how do we model the inventory? The inventory at the start of period t is initial_inventory if t=1, else inventory from previous period minus demand. Then, after ordering, the inventory increases by o_t. So, we need to track inventory levels.

Let me think about the constraints. For each period t:

Inventory at start of t: inv[t-1] (if t>1, else initial_inventory)
Inventory after order: inv[t] = inv[t-1] - demand[t] + o_t

Wait, but the inventory after order must be non-negative. Wait, no, the problem doesn't mention any constraints on inventory levels being non-negative. Wait, but in reality, you can't have negative inventory. So, the model should ensure that the inventory after order is non-negative. Wait, but the problem statement doesn't specify that. Hmm. Let me check the problem again.

The problem says "build a Big-M mixed-integer replenishment model". So, perhaps the model allows for negative inventory? Or maybe not. But in real-world scenarios, you can't have negative inventory. So, the model should ensure that the inventory after order is non-negative. Wait, but the problem might not require that. Let me check the problem statement again.

The problem says "A firm pays a setup cost whenever it places an order during a 4-period horizon." So, the firm can place an order, which adds to the inventory. The demand must be met, so the inventory after order must be at least zero. Wait, no. Let me think: the demand is faced each period. So, the inventory at the start of the period must be sufficient to meet the demand. Otherwise, the firm would have a shortage. But the problem doesn't mention shortage costs, so perhaps the model assumes that the firm can order enough to meet demand. Therefore, the inventory after order must be at least zero. Wait, no. Let me think again.

The inventory at the start of period t is inv[t]. Then, the firm orders o_t, which is added to the inventory. Then, the demand is subtracted. So, the inventory after order is inv[t] + o_t, and then after meeting demand, the inventory is inv[t] + o_t - demand[t]. But that must be non-negative? Or is it allowed to be negative? The problem doesn't specify, but in most inventory models, you can't have negative inventory. So, the model should ensure that inv[t] + o_t >= demand[t]. Wait, no. Let me think again.

Actually, the inventory at the start of period t is inv[t]. Then, the firm orders o_t, which is added to the inventory. Then, the demand is met by the inventory. So, the inventory after order is inv[t] + o_t. Then, after meeting demand, the inventory is inv[t] + o_t - demand[t]. This must be non-negative. Otherwise, the firm can't meet the demand. Therefore, the constraint is inv[t] + o_t >= demand[t]. But how do we model that?

Alternatively, maybe the model allows for negative inventory, but that's not typical. So, perhaps the problem assumes that the firm can order enough to meet the demand. Therefore, the model should ensure that the inventory after order is sufficient to meet the demand. So, inv[t] + o_t >= demand[t]. But how to model that?

Alternatively, perhaps the model allows for negative inventory, but that's not the case here. Let me check the problem again. The problem says "build a Big-M mixed-integer replenishment model". So, the standard approach is to model the inventory as:

For each period t:

inv[t] = inv[t-1] + o_t - demand[t]

But inv[t] must be >= 0. Wait, no. Because inv[t] is the inventory at the end of period t. So, the inventory at the start of period t is inv[t-1], then you order o_t, which increases the inventory. Then, the demand is subtracted. So, the inventory after order is inv[t-1] + o_t, and then after meeting demand, it's inv[t-1] + o_t - demand[t]. This must be >= 0. Therefore, the constraint is inv[t-1] + o_t >= demand[t]. But inv[t] is inv[t-1] + o_t - demand[t], which must be >= 0.

So, the model needs to track the inventory levels. Let me think about how to model this with PuLP.

Let me define variables:

- o_t: order quantity in period t (continuous, >=0)
- y_t: binary variable indicating if an order is placed in period t (1 if ordered, 0 otherwise)
- inv_t: inventory at the end of period t (continuous, >=0)

But since inv_t is the end of period t, which is the start of period t+1. So, for t from 1 to 4, inv_0 is the initial inventory (20). Then, for each t in 1 to 4:

inv_t = inv_{t-1} + o_t - demand[t]

But inv_t must be >= 0.

Wait, but the problem says that the firm pays a setup cost whenever it places an order. So, the setup cost is incurred if o_t > 0. However, in the Big-M model, we can't directly model that. Instead, we use the binary variable y_t to indicate whether an order is placed. So, the setup cost is fixed_order_cost * y_t. But how to link o_t and y_t? Because if y_t is 1, then o_t can be any non-negative value. But if y_t is 0, then o_t must be 0. So, the constraint is o_t <= M * y_t, where M is a large enough number. But in this case, the Big-M is given as 181. Wait, the problem says to use M=181. So, the Big-M is 181. So, the constraint is o_t <= M * y_t. But since the maximum possible order quantity in any period is the sum of all demands (since the firm can order enough to meet all demands), but perhaps the M is given as 181. So, we can use that.

So, the constraints for each period t:

1. o_t <= M * y_t (so that if y_t is 0, o_t must be 0)
2. inv_t = inv_{t-1} + o_t - demand[t]
3. inv_t >= 0
4. The objective is to minimize total cost: sum (unit_order_cost * o_t) + sum (holding_cost * inv_t) + sum (fixed_order_cost * y_t)

But wait, the holding cost is per unit of inventory at the end of the period. So, for each period t, the holding cost is holding_cost * inv_t.

So, the objective function is:

Total cost = sum_{t=1 to 4} (unit_order_cost * o_t) + sum_{t=1 to 4} (holding_cost * inv_t) + sum_{t=1 to 4} (fixed_order_cost * y_t)

Now, the variables:

- o_t: continuous variables for order quantity in each period
- y_t: binary variables for order placement in each period
- inv_t: continuous variables for inventory at the end of each period

But how to model inv_t? Since inv_t is dependent on previous inv and o_t. So, for each period t, we can write:

inv_t = inv_{t-1} + o_t - demand[t]

But inv_0 is the initial inventory, which is 20.

So, for t=1 to 4:

inv_1 = inv_0 + o_1 - demand[0]
inv_2 = inv_1 + o
