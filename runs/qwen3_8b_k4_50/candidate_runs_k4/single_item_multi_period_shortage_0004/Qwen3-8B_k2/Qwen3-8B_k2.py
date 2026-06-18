<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem has three periods with initial inventory of 11 and demand [39, 35, 23]. The goal is to minimize ordering, holding, and shortage costs. The coefficients are 2 for ordering, 1 for holding, and 9 for shortage. The model should include inventory, order, and shortage variables. 

First, I need to define the decision variables. Let's think about what variables are needed. 

For each period, there's an order quantity, which is the amount ordered. Then, there's the inventory level at the end of the period, and possibly the shortage if demand isn't met. Wait, but how do these variables relate?

The inventory at the start of each period is the previous period's inventory minus the demand plus the order. But since there's a possibility of shortage, maybe the inventory can't be negative. Wait, no. The problem allows for temporary unmet demand, so shortages are allowed. So, the inventory after order and before meeting demand could be negative, which would represent a shortage. 

Wait, perhaps the model should track the inventory after order, then subtract demand, and if that's negative, that's a shortage. Or maybe the inventory is the amount available after order, and if it's less than demand, the shortage is the difference. 

Let me think of the standard model for this. Typically, the inventory at the end of period t is equal to the beginning inventory plus order quantity minus demand. But if the beginning inventory plus order is less than demand, then there's a shortage. So, the shortage variable would be the amount by which the demand exceeds the available inventory. 

Alternatively, the inventory can't be negative, and the shortage is the amount that's not met. So, the model needs to track the inventory and the shortage. 

Let me structure the variables. For each period, we have:

- Order quantity (let's call it O_t)
- Inventory level at the end of the period (I_t)
- Shortage at the end of the period (S_t)

But how do these variables relate? 

The inventory at the end of period t is equal to the inventory at the start of the period plus the order quantity minus the demand, minus the shortage. Wait, maybe not. Let me think again. 

The inventory at the start of period t is I_{t-1} (initial inventory for t=1). Then, during the period, we order O_t, which is added to the inventory. Then, the demand D_t is met. If the available inventory (I_{t-1} + O_t) is less than D_t, then the shortage S_t is D_t - (I_{t-1} + O_t). The actual inventory after meeting demand would be zero, but the shortage is the amount not met. 

Alternatively, the inventory after order is I_{t-1} + O_t. Then, the demand is met by the inventory, and any shortage is the amount that can't be met. So, the inventory after meeting demand is max(I_{t-1} + O_t - D_t, 0), and the shortage is max(D_t - (I_{t-1} + O_t), 0). 

But in the model, we need to track these variables. So, for each period t, the inventory after order is I_{t-1} + O_t. Then, the demand is met, so the inventory after meeting demand is I_t = max(I_{t-1} + O_t - D_t, 0), and the shortage is S_t = max(D_t - (I_{t-1} + O_t), 0). 

But how to model this in PuLP? Because we can't directly use max functions in constraints. Instead, we can model the relationship between I_t, O_t, and S_t. 

The key equation is: I_{t-1} + O_t - D_t = I_t - S_t. Because if the available inventory (I_{t-1} + O_t) is less than D_t, then I_t would be zero, and S_t would be D_t - (I_{t-1} + O_t). So, rearranged, I_{t-1} + O_t - D_t = I_t - S_t. 

This equation must hold for each period. 

So, for each period t (from 1 to T), the constraint is:

I_{t-1} + O_t - D_t = I_t - S_t 

But for t=1, I_0 is the initial inventory, which is 11. 

So, the variables are:

- O_t: order quantity in period t (non-negative)
- I_t: inventory at end of period t (non-negative)
- S_t: shortage in period t (non-negative)

The objective is to minimize the sum over all periods of (unit_order_cost * O_t) + (holding_cost * I_t) + (shortage_cost * S_t). 

So, the problem is to define these variables and constraints. 

Now, let's think about how to implement this in PuLP. 

First, the periods are 3. So, for each period t in 1..3, we need variables O_t, I_t, S_t. 

But in PuLP, we can create variables for each period. Let's index them by period. 

Let me outline the steps:

1. Import pulp and os.
2. Define the build_model function that returns the LpProblem.
3. Create the problem instance.
4. Define the variables:
   - For each period t (from 1 to periods), O_t (order quantity), I_t (inventory), S_t (shortage).
   - Also, the initial inventory is given as 11, which is I_0.
5. Define the objective function: sum (unit_order_cost * O_t + holding_cost * I_t + shortage_cost * S_t) for all t.
6. Add constraints for each period:
   - For t=1 to periods:
     I_{t-1} + O_t - D_t = I_t - S_t
   - Also, I_t >= 0, S_t >= 0, O_t >= 0.
7. Solve the problem.
8. Print the status and objective value.
9. Optionally write the LP file if the environment variable is set.

Wait, but the initial inventory is I_0 = 11. For t=1, the constraint is I_0 + O_1 - D_1 = I_1 - S_1. 

So, for each t in 1..periods:

I_{t-1} + O_t - D_t = I_t - S_t 

But how to handle the initial inventory? For t=1, I_0 is 11. 

So, the variables for I_t are for t=0 to periods. Wait, no. The initial inventory is I_0, and for t=1 to periods, we have I_1, I_2, etc. 

So, the variables are:

- O: list of order variables for each period (t=1 to periods)
- I: list of inventory variables for each period (t=0 to periods)
- S: list of shortage variables for each period (t=1 to periods)

Wait, but I_0 is given as initial_inventory. So, for the first period, the constraint is I_0 + O_1 - D_1 = I_1 - S_1. 

So, the variables for I are from t=0 to t=periods. But I_0 is fixed as 11. 

So, in the model, I_0 is a known value, not a variable. 

So, the variables are:

- O_t for t in 1..periods
- I_t for t in 1..periods (since I_0 is fixed)
- S_t for t in 1..periods

Wait, but the constraint for t=1 is I_0 + O_1 - D_1 = I_1 - S_1. 

So, the variables for I are for t=1 to periods. 

So, in code:

We can create variables for O, I, S for each period. 

Let me think about how to code this. 

In Python, for periods=3, we can loop from 1 to 3 (assuming 1-based index). 

But in PuLP, variables can be created with loops. 

So, for each period t in 1..periods:

O_t = pulp.LpVariable(f"order_{t}", lowBound=0)
I_t = pulp.LpVariable(f"inventory_{t}", lowBound=0)
S_t = pulp.LpVariable(f"shortage_{t}", lowBound=0)

Then, for each t in 1..periods:

The constraint is:

I_prev + O_t - demand[t-1] == I_t - S_t 

Where I_prev is the initial inventory for t=1, and for t>1, I_prev is I_{t-1}.

Wait, for t=1, I_prev is initial_inventory (11). For t=2, I_prev is I_1. For t=3, I_prev is I_2. 

So, for each t in 1..periods:

if t == 1:
    I_prev = initial_inventory
else:
    I_prev = I[t-1]

But how to code this in PuLP? 

We can loop through
