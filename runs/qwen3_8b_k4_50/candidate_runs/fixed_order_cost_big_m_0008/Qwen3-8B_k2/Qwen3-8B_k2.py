<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The firm has a 6-period horizon. They start with 6 units of inventory. Each period, there's a demand, and they need to decide how much to order. There are costs involved: unit order cost, holding cost, and a fixed order cost whenever they place an order. The problem mentions using a Big-M method with M=229.

First, I need to model this as a mixed-integer linear programming problem. The key here is to handle the fixed order cost, which is only incurred if an order is placed. The Big-M method is used to model this binary decision (order or not) with a continuous variable.

Let me think about the decision variables. For each period, I need to track the inventory level and whether an order was placed. Let's define:

- Let x_t be the amount ordered in period t. Since we can't order negative, x_t ≥ 0.
- Let y_t be a binary variable indicating if an order is placed in period t (1 if ordered, 0 otherwise).
- Let I_t be the inventory at the end of period t.

The objective is to minimize the total cost, which includes the unit order cost (sum over x_t * unit_order_cost), holding cost (sum over I_t * holding_cost), and fixed order cost (sum over y_t * fixed_order_cost).

Constraints:

1. Inventory balance: For each period t, the inventory at the end of the period is the previous inventory minus demand plus the order placed. So, I_t = I_{t-1} - demand[t] + x_t. But since I_0 is the initial inventory (6), we need to handle the first period correctly.

Wait, the initial inventory is 6. So for t=1, I_0 is 6. Then, for each t from 1 to 6, I_t = I_{t-1} - demand[t-1] + x_t. Wait, the demand is given as a list for periods 0 to 5 (assuming zero-based index). So maybe the periods are 1-based in the problem. Let me check the parameters again.

The problem says the demand is [41, 36, 49, 44, 41, 18], which is 6 periods. So for period 1 to 6, the demand is as listed. So for each period t (from 1 to 6), the demand is demand[t-1].

So the inventory balance equation for period t is:

I_t = I_{t-1} - demand[t-1] + x_t.

But we need to make sure that inventory can't be negative. Wait, the problem doesn't mention any constraints on inventory being non-negative. Wait, but in reality, you can't have negative inventory. So perhaps we need to ensure that I_t ≥ 0 for all t. Wait, but the problem might allow for backorders? The problem statement doesn't specify, so I think we need to assume that inventory can't be negative. So I_t ≥ 0 for all t.

But the problem says "unit ordering, holding, and fixed order costs are 4, 4, and 77". So the holding cost is per unit, and the unit order cost is per unit ordered. So the fixed order cost is incurred whenever an order is placed, regardless of the quantity.

Now, the challenge is to model the fixed order cost. Since y_t is 1 if an order is placed in period t, but x_t can be zero. However, if x_t is zero, then y_t should be zero. But how to enforce that? Because if x_t is zero, but y_t is 1, that would be a problem. So we need to link x_t and y_t such that if x_t > 0, then y_t must be 1. But since x_t can be zero, but y_t can be 1 (if there's a fixed cost even if no order is placed?), but that's not the case. The fixed cost is only incurred when an order is placed. So if x_t is zero, then y_t should be zero. But how to model that?

In the Big-M method, we can model this with the following constraints:

x_t ≤ M * y_t for all t. This ensures that if y_t is 0, then x_t must be 0. Because if y_t is 0, then x_t can't exceed 0 (since M is a large number, but if x_t is zero, then it's okay). Wait, but M is given as 229. So the constraint is x_t ≤ M * y_t. Also, since x_t can't be negative, we have x_t ≥ 0. So this ensures that if y_t is 1, x_t can be up to M, but if y_t is 0, x_t must be 0. However, this might not capture the case where x_t is zero but y_t is 1. Wait, but the fixed cost is only incurred when an order is placed. So if x_t is zero, then y_t should be zero. But how to enforce that? Because if x_t is zero, but y_t is 1, then the fixed cost is added, which is not correct. So the constraints need to ensure that y_t is 1 only if x_t > 0. But since x_t is a continuous variable, how to model that?

Alternatively, perhaps the fixed cost is incurred whenever an order is placed, regardless of the quantity. So even if x_t is zero, but y_t is 1, that would be a problem. Therefore, the correct way is to have y_t = 1 if x_t > 0. But since x_t is a continuous variable, we can't directly model that. So the Big-M approach is to use the constraints:

x_t ≤ M * y_t

and

x_t ≥ ε * y_t

where ε is a small positive number. But since the problem allows x_t to be zero, but if x_t is zero, then y_t must be zero. However, in the problem statement, the fixed order cost is incurred whenever an order is placed. So if x_t is zero, but y_t is 1, that would be an error. Therefore, the constraints should ensure that y_t is 1 only if x_t > 0. But how?

Alternatively, perhaps the fixed cost is only incurred if x_t > 0. So the fixed cost is fixed_order_cost * y_t, where y_t is 1 if x_t > 0. But again, how to model that. The standard approach is to use the Big-M method with the constraints:

x_t ≤ M * y_t

and

x_t ≥ ε * y_t

But since the problem allows x_t to be zero, but if x_t is zero, then y_t must be zero. However, in practice, the fixed cost is only incurred if an order is placed. So if x_t is zero, then y_t must be zero. Therefore, the constraints should be:

x_t ≤ M * y_t

and

x_t ≥ 0

But then, if x_t is zero, y_t can be 0 or 1. However, the fixed cost is fixed_order_cost * y_t. So if x_t is zero but y_t is 1, the fixed cost is added, which is not correct. Therefore, we need to ensure that y_t is 1 only if x_t > 0. But how?

This is a classic issue in MIP modeling. The standard approach is to use the constraints:

x_t ≤ M * y_t

and

x_t ≥ ε * y_t

where ε is a small positive number (like 1). But since the problem allows x_t to be zero, but if x_t is zero, then y_t must be zero. However, if we use x_t ≥ ε * y_t, then if y_t is 1, x_t must be at least ε. So if ε is 1, then x_t must be at least 1. Therefore, if x_t is zero, then y_t must be zero. This way, the fixed cost is only incurred when x_t is positive. But in the problem, the unit order cost is 4, so the order quantity can be zero. But the fixed cost is only incurred if an order is placed. So the model should have y_t = 1 if x_t > 0. Therefore, the constraints x_t ≥ ε * y_t with ε=1 would ensure that if y_t is 1, x_t is at least 1. Therefore, the fixed cost is only added when x_t is at least 1. But the problem allows x_t to be zero, but then y_t must be zero. Therefore, the constraints:

x_t ≤ M * y_t

x_t ≥ 0

But then, if x_t is zero, y_t can be 0 or 1. However, the fixed cost is fixed_order_cost * y_t. So if x_t is zero and y_t is 1, the fixed cost is added, which is incorrect. Therefore, the correct approach is to have:

x_t ≥ ε * y_t

where ε is a small positive number (like 1). Then, if y_t is 1, x_t must be at least ε, which ensures that x_t is positive. Therefore, the fixed cost is only added when x_t is positive. But in the problem, the fixed cost is incurred whenever an order is placed. So even if x_t is zero
