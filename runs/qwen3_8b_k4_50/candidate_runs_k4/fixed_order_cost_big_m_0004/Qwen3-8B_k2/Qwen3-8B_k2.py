pulp.LpProblem("InventoryReplenishment", pulp.LpMinimize)

Define variables:

For each period t in 1..T:

Q_t = pulp.LpVariable(f"Q_{t}", lowBound=0, cat='Continuous')
I_t = pulp.LpVariable(f"I_{t}", lowBound=0, cat='Continuous')
Y_t = pulp.LpVariable(f"Y_{t}", cat='Binary')

But since the periods are 6, we can loop from 1 to 6.

Then, the objective function:

prob += pulp.lpSum([unit_order_cost * Q_t for t in periods]) + pulp.lpSum([holding_cost * I_t for t in periods]) + pulp.lpSum([fixed_order_cost * Y_t for t in periods])

Wait, but the periods are 1 to 6. So for each t in 1..6, we have Q_t, I_t, Y_t.

Then, the constraints:

First, the initial inventory. For t=1, I_0 is 15. So for the first period, the inventory before demand is I_0 + Q_1. Then subtract demand to get I_1.

So for each t in 1..6:

I_{t-1} + Q_t - demand[t-1] = I_t.

But how to handle I_0? For t=1, I_0 is 15. For t>1, I_{t-1} is the previous I variable.

So, for each t in 1 to 6:

prob += I_{t-1} + Q_t - demand[t-1] == I_t

But in code, for t in range(1, periods+1):

But how to index the variables. Let's say we have variables stored in a list. For example, for Q, we can have a list Q = [Q_1, Q_2, ..., Q_6], same for I and Y.

So in code:

periods = 6
demand = [54, 47, 42, 50, 43, 25]

Then, for each t in 1 to 6:

I_prev = I[t-2] if t>1 else initial_inventory

Wait, maybe better to create variables for each period. Let's think:

For t in 1 to 6:

I_t is the inventory after meeting demand in period t.

So for t=1, the inventory before demand is initial_inventory + Q_1. Then subtract demand[0] (since demand is 0-indexed) to get I_1.

So the constraint for t=1 is:

initial_inventory + Q_1 - demand[0] = I_1

For t=2:

I_1 + Q_2 - demand[1] = I_2

And so on.
