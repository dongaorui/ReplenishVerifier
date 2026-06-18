<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The store has 4 periods. They start with 24 units. The demands for each period are [33, 20, 29, 21]. Ordering costs are 4 per unit, and holding costs are 3 per unit. The goal is to minimize the total cost, which includes ordering and holding costs.

First, I need to define the decision variables. The main variables here are the order quantities for each period. Let's call them order[t] for t from 0 to 3 (since there are 4 periods). Also, I need to track the inventory levels after each period. Let's say inventory[t] represents the inventory at the end of period t.

Wait, but inventory levels depend on previous orders and demands. Let me think about the constraints. The initial inventory is 24. For each period, the inventory before the order is the previous inventory minus the demand. Then, after ordering, the inventory increases by the order quantity. But wait, the order happens before the demand is met? Or is the order placed after the demand is known? Hmm, the problem says "replenishment" which usually implies that orders are placed before the period's demand. So the order for period t is placed before the demand of that period is met. So the inventory at the start of period t is previous inventory plus order[t] minus demand[t]. Wait, no. Let me think again.

Let me model the inventory flow. Let's assume that at the start of period t, the inventory is inv[t]. Then, the demand for period t is met from the inventory. So inv[t] must be at least demand[t]. Then, after meeting the demand, the inventory is inv[t] - demand[t]. Then, the order for period t is added, which increases the inventory. Wait, but maybe the order is placed at the beginning of the period. So the order is added to the inventory before the demand is subtracted. Or is the order placed after the demand is met?

This is crucial for the model. Let me think. Typically, in inventory models, the order is placed at the beginning of the period, and the demand is met from the inventory. So the inventory at the start of period t is inv[t], which is the previous inventory plus the order placed in period t. Then, the demand is subtracted from that. So the inventory after meeting the demand is inv[t] - demand[t]. But that would mean that the order is placed before the demand is met. So the order quantity for period t is added to the inventory before the demand is subtracted. Wait, but that would mean that the order is placed at the beginning of the period, and the demand is met from the inventory. So the inventory at the start of period t is inv_prev + order[t], and then after meeting the demand, the inventory becomes inv_prev + order[t] - demand[t]. But then, the next period's inventory is that value.

Wait, maybe I should model the inventory after the order is placed but before the demand is met. Let me think again. Let's define the inventory after the order is placed but before the demand is met as inv[t]. Then, the demand is subtracted from inv[t], leading to inv[t] - demand[t], which becomes the inventory at the end of the period. But then, the next period's inventory starts with that value. So the order for period t is added to the previous inventory (from the end of the previous period) to get inv[t]. So the constraint would be:

inv[t] = previous_inventory + order[t]

Then, the demand must be met, so inv[t] >= demand[t]. Wait, no. Because inv[t] is the inventory before the demand is met. So inv[t] must be at least demand[t]. Then, after meeting the demand, the inventory is inv[t] - demand[t], which becomes the inventory at the end of the period. So the next period's inventory starts with that value.

But how to model this? Let me think of variables:

Let me define:

- order[t]: the quantity ordered in period t (t from 0 to 3)
- inv[t]: the inventory at the end of period t (after meeting the demand)

Wait, but then for period 0:

Initial inventory is 24. Then, order[0] is added to that. So the inventory before demand is 24 + order[0]. Then, the demand is 33. So the inventory after meeting the demand is (24 + order[0]) - 33. That's inv[0].

Then, for period 1, the inventory starts with inv[0], and order[1] is added. So inventory before demand is inv[0] + order[1]. Then, subtract demand[1] to get inv[1].

So the constraints would be:

For each period t in 0 to 3:

inv[t] = inv_prev + order[t] - demand[t]

Wait, no. Let me rephrase:

At the start of period t, the inventory is inv_prev (the inventory at the end of period t-1). Then, order[t] is added, so the inventory before demand is inv_prev + order[t]. Then, the demand is subtracted, leading to inv_prev + order[t] - demand[t] = inv[t].

So the constraint for inv[t] is:

inv[t] = inv_prev + order[t] - demand[t]

But inv_prev is inv[t-1], except for t=0, where inv_prev is the initial inventory (24).

So for t=0:

inv[0] = initial_inventory + order[0] - demand[0]

For t >=1:

inv[t] = inv[t-1] + order[t] - demand[t]

But since inv[t] must be non-negative, because you can't have negative inventory. Wait, but the problem doesn't specify whether backorders are allowed. The problem says "cost-minimizing replenishment", so I think we can assume that inventory can't be negative. So inv[t] >= 0 for all t.

But the problem says "demand is faced", so the inventory before meeting the demand must be at least the demand. Wait, no. Because if the inventory before meeting the demand is inv_prev + order[t], which must be >= demand[t]. Because otherwise, you can't meet the demand. So that's a constraint.

So for each period t:

inv_prev + order[t] >= demand[t]

But inv_prev is inv[t-1] for t >=1, and initial_inventory for t=0.

So the constraints are:

For t=0:

initial_inventory + order[0] >= demand[0]

For t >=1:

inv[t-1] + order[t] >= demand[t]

But inv[t] is inv[t-1] + order[t] - demand[t], which must be >=0.

Wait, but inv[t] is the inventory after meeting the demand. So inv[t] = inv_prev + order[t] - demand[t], and inv[t] >=0.

So the constraints are:

For each t in 0 to 3:

inv_prev + order[t] >= demand[t]

and

inv[t] = inv_prev + order[t] - demand[t] >=0

But inv_prev is the inventory at the end of the previous period. So for t=0, inv_prev is initial_inventory. For t=1, inv_prev is inv[0], etc.

So the variables are order[t] and inv[t].

But since inv[t] is determined by the previous inv and order, maybe we can model it as a sequence of equations.

But in PuLP, we can model these as constraints.

So the steps are:

1. Define the problem as a minimization problem.

2. Define variables:

   - order[t] for t in 0..3 (non-negative integers, but since it's LP, they can be real numbers, but the problem says "replenishment" which might imply integer quantities. Wait, the problem says "unit_order_cost" and "holding_cost" per unit. So the variables can be real numbers, but the problem might require integer solutions. However, the problem says "LP", so it's a linear program, which allows real numbers. So the variables can be continuous.

But the problem says "replenishment" which might imply that orders can be fractional. So we can model order[t] as continuous variables.

3. The objective function is the sum over all periods of (order[t] * unit_order_cost) + (inv[t] * holding_cost).

Wait, the holding cost is per unit per period. So for each period, the inventory at the end of the period is inv[t], so the holding cost for that period is inv[t] * holding_cost. So the total cost is sum over t (order[t] * unit_order_cost + inv[t] * holding_cost).

But wait, the holding cost is for the inventory at the end of the period. So yes.

So the objective is to minimize total cost.

Now, the constraints:

For each period t:

inv_prev + order[t] >= demand[t]

and

inv[t] = inv_prev + order[t] - demand[t] >=0

But inv_prev is the inventory at the end of the previous period. So for t=0, inv_prev is initial_inventory. For t=1, inv_prev is inv[0], etc.

So the variables are order[t] and inv[t], for t=0 to 3.

But how to model this in PuLP?

Let me think about the variables. Let's create variables for order and inventory.

In code:

periods
