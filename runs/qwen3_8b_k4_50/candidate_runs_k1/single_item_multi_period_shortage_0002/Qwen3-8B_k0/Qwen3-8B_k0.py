<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem with shortages. Let me start by understanding the problem.

The problem has 3 periods. The initial inventory is 20. Demands for each period are 39, 60, 52. The unit order cost is 5, holding cost is 2, and shortage penalty is 10. The task is to formulate a linear backorder model. 

So, the model should account for ordering, holding inventory, and handling shortages. Let me think about the decision variables. 

First, I need to decide how much to order in each period. Let's call that variable 'order' for each period. Then, the inventory after each period depends on the previous inventory, the order, and the demand. But since shortages are allowed, maybe we need to track the inventory level and any shortages.

Wait, in a backorder model, when there's a shortage, the demand is backordered and fulfilled in a future period. So, the inventory can't be negative. Wait, no. Wait, in backorder models, shortages are allowed but they are carried over as backorders. So, the inventory after meeting demand can't be negative, but if the demand exceeds the available inventory, the shortage is recorded and added to the next period's demand?

Wait, maybe I need to model the inventory level after each period. Let me think step by step.

Let me denote:

For each period t (from 1 to 3):

- Let I_t be the inventory at the start of period t. Wait, or maybe the end? Hmm. Let me think. The initial inventory is 20, which is the inventory at the start of period 1. Then, during period 1, we order some quantity, which is added to the inventory. Then, the demand is met. If the inventory is not enough, there's a shortage. 

Alternatively, perhaps the inventory after ordering but before meeting demand. Let me structure it properly.

Let me define:

For each period t (1 to 3):

- Let O_t be the order quantity in period t. This is the decision variable.
- Let I_t be the inventory at the start of period t. So, I_1 is the initial inventory, 20.
- Then, during period t, the inventory is I_t + O_t (after ordering), then demand D_t is met. If I_t + O_t >= D_t, then the inventory after meeting demand is I_t + O_t - D_t. If not, then the shortage is D_t - (I_t + O_t), and the inventory after meeting demand is zero. But since it's a backorder model, maybe the shortage is carried over as a backorder, so the inventory after meeting demand is zero, but the backorder is added to the next period's demand?

Wait, maybe I need to track the inventory after meeting demand and any shortages. Let me think again.

In a backorder model, shortages are allowed but they are carried over. So, the inventory after meeting demand can't be negative. Wait, no. If the inventory is not enough to meet demand, the shortage is recorded, and the demand is not met. But in backorder models, the shortage is carried over to future periods. So, the actual inventory after meeting demand is zero, but the backorder is added to the next period's demand. 

Alternatively, perhaps the model should track the inventory level and the backorders. Let me think of the variables:

Let me define:

For each period t:

- O_t: order quantity in period t (decision variable)
- I_t: inventory at the end of period t (after meeting demand)
- S_t: shortage in period t (if any)

But maybe it's better to track the inventory before meeting demand. Let me think again.

Let me structure the problem as follows:

At the start of period t, the inventory is I_{t-1} (from the end of previous period). Then, we place an order O_t, which is added to the inventory. So, the inventory before meeting demand is I_{t-1} + O_t. Then, the demand D_t is met. If the available inventory is sufficient, then the inventory after meeting demand is (I_{t-1} + O_t) - D_t. If not, then the shortage is D_t - (I_{t-1} + O_t), and the inventory after meeting demand is zero. However, in a backorder model, the shortage is carried over as a backorder, which would be added to the next period's demand. Wait, but how does that affect the model?

Alternatively, perhaps the model should track the inventory after meeting demand and the backorders. Let me think of the variables:

Let me define:

For each period t:

- O_t: order quantity (decision variable)
- I_t: inventory after meeting demand (i.e., end of period t)
- B_t: backorder (shortage) at the end of period t

But maybe that's getting complicated. Let me check standard inventory models.

In a standard multi-period inventory model with backorders, the key variables are:

- Order quantity O_t
- Inventory level I_t (after meeting demand)
- Shortage S_t (if any)

But the relationship between these variables is:

At the start of period t, the inventory is I_{t-1} (from previous period). Then, we order O_t, so the available inventory is I_{t-1} + O_t. Then, the demand D_t is met. If I_{t-1} + O_t >= D_t, then the inventory after meeting demand is I_{t-1} + O_t - D_t. If not, then the shortage is D_t - (I_{t-1} + O_t), and the inventory after meeting demand is zero. However, in backorder models, the shortage is carried over as a backorder, which would be added to the next period's demand. Wait, but how does that affect the model?

Alternatively, perhaps the model should track the inventory after meeting demand and the backorders. Let me think of the following:

The inventory after meeting demand in period t is I_t. The backorder (shortage) in period t is S_t. Then, the relationship is:

I_{t-1} + O_t = D_t + I_t + S_t

Wait, that's because the available inventory (I_{t-1} + O_t) is used to meet the demand D_t, and any excess becomes inventory I_t, and any deficit becomes shortage S_t. So, the equation is:

I_{t-1} + O_t = D_t + I_t + S_t

But since I_t and S_t are non-negative, this equation holds. However, in a backorder model, the shortage S_t is carried over to the next period. Wait, but how? Maybe the backorder S_t is added to the next period's demand. So, the demand for the next period is D_{t+1} + S_t. But that complicates the model.

Alternatively, perhaps the model should track the inventory after meeting demand and the backorders. Let me think again.

Let me consider that the backorder S_t is the amount of demand not met in period t. Then, in the next period, the backorder S_t is added to the demand. So, the demand for period t+1 is D_{t+1} + S_t. But that would require adjusting the demand for each period. However, in the problem statement, the demand is given as [39, 60, 52], so perhaps the backorders are not added to the demand. Wait, maybe the model allows for shortages, but they are not carried over. Wait, the problem says "shortages are allowed" but the model is a backorder model. So, the shortage is carried over as a backorder, which is fulfilled in a future period. Therefore, the backorder S_t is added to the next period's demand. 

But this complicates the model. Let me think of the variables again.

Let me define:

For each period t:

- O_t: order quantity (decision variable)
- I_t: inventory at the end of period t (after meeting demand)
- S_t: shortage (backorder) at the end of period t

The relationship between these variables is:

At the start of period t, the inventory is I_{t-1} (from previous period). Then, we order O_t, so the available inventory is I_{t-1} + O_t. Then, the demand D_t is met. If the available inventory is sufficient, then I_t = I_{t-1} + O_t - D_t, and S_t = 0. If not, then I_t = 0 (since all available inventory is used to meet demand), and S_t = D_t - (I_{t-1} + O_t). However, in a backorder model, the shortage S_t is carried over to the next period. Therefore, the next period's demand is D_{t+1} + S_t. Wait, but how does that affect the model? 

Alternatively, perhaps the backorder S_t is added to the next period's demand. So, the actual demand that needs to be met in period t+1 is D_{t+1} + S_t. But that would require adjusting the demand for each period. However, the problem statement gives fixed demands, so maybe the backorder is not added to the demand. 

This is getting a bit confusing. Let me check standard formulations. 

In a standard backorder model, the shortage is allowed and is carried over. The key
