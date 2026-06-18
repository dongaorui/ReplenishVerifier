<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has 3 periods. We need to decide the order quantity Q_t each period, inventory I_t, and backlog B_t. The initial inventory is 10. Demand for each period is [24, 52, 35]. The costs are order cost 3, holding cost 4, and shortage cost 11. The goal is to minimize total cost with net inventory balance.

First, I should define the decision variables. For each period t (from 1 to 3), I need Q_t (order quantity), I_t (inventory after order and before demand), and B_t (backlog from previous periods). Wait, but backlog might be related to the previous period's shortage. Let me think about the inventory balance.

The net inventory balance equation should be: I_t = I_{t-1} + Q_t - D_t - B_{t-1} + ...? Wait, maybe I need to model the inventory and backlog properly. Let me think again.

At each period, the inventory after order is I_t. Then, the demand D_t is met first. If I_t is less than D_t, then there's a shortage. The backlog B_t would accumulate the unmet demand. Alternatively, maybe the inventory after meeting demand is I_t - D_t, but if that's negative, it becomes backlog. Hmm, perhaps the correct way is:

The inventory after order is I_t. Then, the demand D_t is subtracted. If I_t >= D_t, then the inventory after demand is I_t - D_t, and backlog B_t is zero. If I_t < D_t, then the backlog B_t is D_t - I_t, and the inventory after demand is zero. Wait, but backlog is the amount that couldn't be met. So the inventory after demand is max(I_t - D_t, 0), and the shortage is max(D_t - I_t, 0). But how does this relate to the variables?

Alternatively, the inventory balance equation could be:

I_t = I_{t-1} + Q_t - D_t - B_{t-1} ?

Wait, maybe the correct way is that the inventory at the start of period t is I_{t-1} (from previous period's end). Then, we order Q_t, so the inventory before demand is I_{t-1} + Q_t. Then, the demand D_t is subtracted. If there's a shortage, the backlog B_t is the amount not met. So:

I_t (inventory after demand) = I_{t-1} + Q_t - D_t - B_t ?

Wait, maybe not. Let me think of the inventory balance. Let me consider that the inventory after order is I_{t} (before demand). Then, the demand D_t is subtracted. If I_t >= D_t, then the inventory after demand is I_t - D_t, and B_t = 0. If I_t < D_t, then the inventory after demand is zero, and B_t = D_t - I_t. So the equation would be:

I_t (after demand) = max(I_t_prev + Q_t - D_t, 0)

But how to model this with variables? Maybe the correct way is to have the inventory after order (before demand) as I_t, and then the demand is subtracted. So:

I_t_prev (inventory at the start of period t) + Q_t = I_t (inventory before demand) 

Then, the demand D_t is subtracted. The inventory after demand is I_t - D_t. If this is negative, it's a shortage, which becomes backlog. So:

I_t - D_t = I_t_after_demand 

But I_t_after_demand can't be negative. So:

I_t_after_demand = max(I_t - D_t, 0)

But how to model this in the constraints? Maybe we need to track the backlog. Let me think again.

Alternatively, the net inventory balance equation could be:

I_t_prev + Q_t - D_t = I_t_after_demand - B_t 

Wait, perhaps the correct equation is:

I_t_prev + Q_t = D_t + I_t_after_demand + B_t 

Because the total available (inventory plus order) is equal to the demand plus the remaining inventory and backlog. But I'm getting confused here. Let me look for standard inventory models.

In standard models, the inventory balance equation is:

Inventory at the end of period t = Inventory at the start of period t + Order quantity - Demand - Shortage 

Wait, but shortage is the amount not met. So:

Inventory at the end of period t = Inventory at the start of period t + Order quantity - Demand 

But if this is negative, then the shortage is the negative value. So:

Inventory at the end of period t = max(Inventory at the start + Order quantity - Demand, 0)

Shortage = max(Demand - (Inventory at the start + Order quantity), 0)

But how to model this with variables. Let me think of the variables:

Let me define:

For each period t:

- Q_t: order quantity (non-negative)
- I_t: inventory at the end of period t (non-negative)
- B_t: backlog at the end of period t (non-negative)

But the inventory at the end of period t is the inventory after meeting demand. So:

I_t = I_{t-1} + Q_t - D_t - B_{t-1} ?

Wait, maybe not. Let me think of the inventory and backlog as follows:

At the start of period t, the inventory is I_{t-1} (from previous period's end). Then, we order Q_t. So the total available is I_{t-1} + Q_t. Then, the demand D_t is met first. If I_{t-1} + Q_t >= D_t, then the inventory after meeting demand is I_{t-1} + Q_t - D_t, and backlog B_t is zero. If I_{t-1} + Q_t < D_t, then the inventory after meeting demand is zero, and backlog B_t is D_t - (I_{t-1} + Q_t).

So the equation for the inventory after meeting demand (which is I_t) is:

I_t = max(I_{t-1} + Q_t - D_t, 0)

And the backlog B_t is max(D_t - (I_{t-1} + Q_t), 0)

But how to model this in PuLP. Since PuLP can't directly handle max functions, we need to use constraints to represent these relationships.

Alternatively, we can model the inventory and backlog as:

I_t + B_t = I_{t-1} + Q_t - D_t 

But since I_t and B_t are non-negative, this equation can be rewritten as:

I_t + B_t = I_{t-1} + Q_t - D_t 

But since I_t and B_t can't be negative, this equation must hold. However, this would allow I_t and B_t to be negative if the right-hand side is negative. So we need to ensure that I_t and B_t are non-negative. Therefore, the constraints would be:

I_t >= 0 

B_t >= 0 

And the equation:

I_t + B_t = I_{t-1} + Q_t - D_t 

But this equation can be rewritten as:

I_t + B_t = I_{t-1} + Q_t - D_t 

But since I_t and B_t are non-negative, this equation implies that I_{t-1} + Q_t - D_t can be positive or negative. However, if it's negative, then I_t and B_t would have to sum to a negative value, which is impossible. Therefore, this suggests that the equation is not correct. 

Wait, perhaps the correct equation is:

I_t + B_t = I_{t-1} + Q_t - D_t 

But since I_t and B_t are non-negative, this equation can only hold if I_{t-1} + Q_t - D_t >= 0. Otherwise, the left side would be non-negative, but the right side would be negative. Therefore, this equation is not valid. 

So, perhaps the correct way is to model the inventory and backlog as:

I_t = I_{t-1} + Q_t - D_t - B_t 

But this seems similar to the previous equation. 

Alternatively, perhaps the correct way is to model the inventory and backlog as follows:

The inventory after order is I_{t} (before demand). Then, the demand D_t is subtracted. The inventory after demand is I_{t} - D_t. If this is negative, then the backlog is the negative value. So:

I_{t} - D_t = I_{t_after_demand} - B_t 

Wait, this is getting too confusing. Let me refer to standard inventory models. 

In the standard model, the inventory balance equation is:

Inventory at the end of period t = Inventory at the start of period t + Order quantity - Demand 

But if this is negative, it's considered as a shortage. So the equation can be written as:

I_t = I_{t-1} + Q_t - D_t 

But if I_t is negative, then it's a shortage. However, in this problem, the backlog B_t is the amount of shortage. So perhaps:

I_t = I_{t-1} + Q_t - D_t 

But if I_t is negative, then B_t = -I_t 

But then, the inventory
