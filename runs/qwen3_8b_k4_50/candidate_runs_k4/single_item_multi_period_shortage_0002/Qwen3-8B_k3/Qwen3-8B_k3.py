<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve a multi-period inventory replenishment problem with shortages. Let me start by understanding the problem details.

The problem has 3 periods. The initial inventory is 20. Demands for each period are 39, 60, 52. The unit order cost is 5, holding cost is 2, and shortage penalty is 10. We need to model a linear backorder model, which means shortages are allowed but penalized.

First, I need to define the decision variables. For each period, there's an order quantity, which is the amount ordered. Also, there's a shortage variable for each period. But wait, in backorder models, shortages are backordered, so maybe the shortage is the amount not met by inventory plus orders. Wait, no. Let me think again.

In a backorder model, when demand exceeds available inventory, the shortage is carried over to the next period. So, the inventory at the end of each period is initial inventory plus orders minus demand, but if that's negative, the shortage is the negative value. But how to model that?

Alternatively, the model should track the inventory level after each period. Let me think about the variables. Let's say for each period, we have:

- Order quantity (q_t) for period t.
- Shortage (s_t) for period t.

But maybe the shortage is the amount that couldn't be met in period t. So, the inventory at the start of period t is previous inventory plus order from previous period minus demand. Wait, maybe I need to track the inventory after each period.

Wait, the initial inventory is 20. Let's think about each period step by step.

For period 1:

Start with initial inventory (20). Then, order q1. Then, the available inventory is 20 + q1. Then, demand is 39. If available inventory is less than demand, then the shortage is demand - available inventory. But since it's a backorder model, the shortage is carried over. Wait, no. In backorder models, the shortage is not lost but backordered. So, the inventory after meeting demand would be available inventory - demand, but if that's negative, the shortage is the negative value. Wait, maybe the inventory after period t is (previous inventory + order) - demand. If that's negative, the shortage is the absolute value. But how to model that?

Alternatively, the model can have variables for inventory after meeting demand (which could be negative, representing shortage) and then the shortage cost is based on that. But since the problem says it's a backorder model, maybe the shortage is carried over to the next period. Wait, but the problem says "shortage penalty" which is a cost for not meeting demand. So, the model should account for the shortage cost when demand is not met in the current period.

So, the key is to model the inventory level after each period, considering orders and demand, and track any shortages.

Let me think of variables:

For each period t (from 1 to 3):

- q_t: order quantity in period t. This is non-negative.
- s_t: shortage in period t. This is non-negative.

But how do these variables relate to the inventory?

The inventory at the start of period t is the previous inventory (after previous period's operations) plus any orders from the previous period. Wait, maybe I need to track the inventory after each period. Let me think:

Let me define:

For each period t (1 to 3):

- Let inv_t be the inventory at the end of period t. This is the inventory after meeting demand and any shortages.

Wait, but in the backorder model, if there's a shortage in period t, that shortage is carried over to the next period. So, the inventory after period t is inv_t = inv_{t-1} + q_t - demand_t. But if inv_t is negative, that's a shortage. Wait, no. Because if inv_{t-1} + q_t is less than demand_t, then the shortage is demand_t - (inv_{t-1} + q_t). But that shortage is carried over as a backorder. So, the inventory after period t would be inv_t = inv_{t-1} + q_t - demand_t. However, if inv_t is negative, that's a shortage. But in the backorder model, the shortage is not lost, so the inventory after period t would be zero, and the shortage is carried over as a backorder. Wait, maybe I need to model the inventory as the amount available after meeting demand, and the shortage is the amount that couldn't be met. So, the inventory after period t is max(inv_{t-1} + q_t - demand_t, 0), and the shortage is max(inv_{t-1} + q_t - demand_t, 0) * -1. But that's not correct. Wait, no. Let me think again.

In a backorder model, if the available inventory (previous inventory plus order) is less than demand, the shortage is the difference. But the shortage is carried over to the next period. So, the inventory after period t is the previous inventory plus order minus demand. If that's negative, the shortage is the negative value, and the inventory after period t is zero. Wait, no. Because the shortage is the amount that couldn't be met, which is carried over. So, the inventory after period t is the previous inventory plus order minus demand. If that's negative, then the shortage is the negative value, and the inventory after period t is zero. But that's not correct. Wait, maybe the inventory after period t is the previous inventory plus order minus demand, and if that's negative, the shortage is the absolute value. But then, the inventory after period t is zero. But that's not the case. Because the shortage is carried over as a backorder, which would be added to the next period's inventory. Wait, perhaps the model should track the backorders. So, the inventory after period t is the previous inventory plus order minus demand. If that's negative, the shortage is the negative value, and the inventory after period t is zero. But then, the shortage is carried over as a backorder. Wait, this is getting complicated. Maybe I need to model the inventory after each period as the previous inventory plus order minus demand, and the shortage is the negative of that if it's negative. But how to model that in the objective function.

Alternatively, the model can have variables for the inventory after each period (inv_t), and the shortage in each period (s_t). The relationship would be:

inv_t = inv_{t-1} + q_t - demand_t - s_t

But since s_t is the shortage, which is the amount not met. Wait, maybe:

inv_t = inv_{t-1} + q_t - demand_t + s_{t-1} - s_t

Wait, this is getting too confusing. Let me refer to standard inventory models.

In a backorder model, the inventory after meeting demand is inv_t = inv_{t-1} + q_t - demand_t. If inv_t is negative, that means there's a shortage of -inv_t, which is carried over as a backorder. So, the shortage in period t is max(0, demand_t - (inv_{t-1} + q_t)). But how to model this in the constraints.

Alternatively, the model can have variables for the inventory after each period (inv_t), and the shortage in each period (s_t). The relationship would be:

inv_t = inv_{t-1} + q_t - demand_t + s_{t-1} - s_t

Wait, maybe not. Let me think again. The inventory after period t is the previous inventory plus order minus demand, but if there's a shortage, the shortage is carried over. So, the inventory after period t is inv_t = inv_{t-1} + q_t - demand_t. If inv_t is negative, then the shortage is -inv_t, and this shortage is carried over as a backorder. So, the next period's inventory would be inv_{t} + s_t (the backorder from previous period). Wait, perhaps the model should track the backorders. Let me think of the inventory after meeting demand as inv_t, which can be negative (shortage). Then, the backorder from period t is the negative of inv_t. But that's not correct. Maybe the backorder is the amount that couldn't be met, which is max(0, demand_t - (inv_{t-1} + q_t)). But then, the backorder is carried over to the next period. So, the inventory after period t is inv_t = inv_{t-1} + q_t - demand_t. But if inv_t is negative, then the backorder is -inv_t, and the next period's inventory starts with that backorder. Wait, maybe the inventory after period t is inv_t = inv_{t-1} + q_t - demand_t. If inv_t is negative, then the shortage is -inv_t, and the next period's inventory starts with that shortage. So, the inventory after period t is inv_t, and the next period's inventory is inv_t + s_t (where s_t is the shortage from period t). Wait, this is getting too tangled. Maybe I need to model the inventory after each period as inv_t, and the shortage in period t is max(0, demand_t - (inv_{t-1} + q_t)). Then, the inventory after period t is inv_t = inv_{t-1}
