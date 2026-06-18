<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem statement thoroughly.

The problem has 4 periods. The initial inventory is 16, and the demands for each period are [22, 44, 23, 44]. We need to decide the order quantity Q_t for each period, the inventory level I_t, and a binary variable Y_t indicating if an order is placed. The goal is to minimize the total cost, which includes unit order cost, holding cost, and fixed order cost. The Big-M method is used with M=133 to link the order quantity and the binary variable.

First, I'll outline the decision variables. For each period t (from 1 to T), we have:

- Q_t: the quantity ordered in period t. This should be a non-negative integer variable.
- I_t: the inventory level at the end of period t. Also non-negative.
- Y_t: a binary variable indicating whether an order is placed in period t (1 if ordered, 0 otherwise).

The constraints will involve the inventory balance. For each period, the inventory at the start plus the order quantity minus the demand equals the inventory at the end. Also, the order quantity must be zero if Y_t is zero, and at least some minimum if Y_t is one. That's where the Big-M method comes in.

The objective function is the sum of unit order costs (5 per unit ordered), holding costs (3 per unit held), and fixed order costs (80 per order placed). So, for each period, we add 5*Q_t + 3*I_t + 80*Y_t to the total cost.

Now, let's think about the constraints. The initial inventory is 16, so for period 1, the starting inventory is 16. Then, for each period t, the inventory after the order is I_{t-1} + Q_t - demand_t = I_t. Wait, but the order is placed before the period, so the inventory at the start of period t is I_{t-1} (from the end of previous period). Then, after ordering Q_t, the inventory becomes I_{t-1} + Q_t, then subtract the demand to get I_t. So the correct equation is I_{t-1} + Q_t - demand_t = I_t. But since I_0 is the initial inventory, which is 16.

So for each period t from 1 to T, the constraint is I_{t-1} + Q_t - demand[t-1] = I_t. Wait, since the demand is given as a list, maybe index from 0 to T-1. So for period 1, demand is 22, etc.

Now, the Big-M constraints. The idea is that if Y_t is 1, then Q_t must be at least some minimum (but since the problem doesn't specify a minimum order quantity, maybe it's zero? Wait, but the problem says "fixed ordering costs" which are incurred when an order is placed. So if Y_t is 1, then Q_t must be at least zero (but maybe there's a minimum order quantity? The problem doesn't mention that, so perhaps Q_t can be zero even if Y_t is 1? Wait, no. Because Y_t is a binary variable indicating whether an order is placed. If Y_t is 1, then an order is placed, but the quantity could be zero? That seems odd. Wait, maybe the problem assumes that if Y_t is 1, then Q_t must be at least some positive value. But the problem statement doesn't specify that. Hmm. Wait, the problem says "Use order Q_t, inventory I_t, binary order trigger Y_t, and Big-M links with M=133". So the Big-M method is used to link Q_t and Y_t. Typically, in such models, the Big-M constraints are:

Q_t >= M * Y_t (but that would force Q_t to be large if Y_t is 1, which isn't helpful). Wait, no. Wait, the standard approach is to model that if Y_t is 1, then Q_t must be at least some minimum (like 1), but if Y_t is 0, then Q_t must be zero. But the problem doesn't specify a minimum order quantity. However, the problem says that the fixed order cost is incurred when Y_t is 1. So perhaps the model allows Q_t to be zero even if Y_t is 1. But that would mean that the fixed cost is paid even if no order is placed. That seems odd. Wait, maybe the problem is that Y_t is 1 if an order is placed (i.e., Q_t > 0), but the Big-M constraints are used to enforce that. So the constraints would be:

Q_t >= M * Y_t (but that would require Q_t to be at least M if Y_t is 1, which is not correct). Wait, perhaps the correct way is to have Q_t >= 0, and Y_t is 1 if Q_t > 0. But since we can't directly model that in linear programming, we use Big-M constraints. So the standard approach is to have:

Q_t >= M * Y_t (but that would require Q_t to be at least M if Y_t is 1, which is not correct). Wait, maybe the other way around. Let me think again.

The standard Big-M approach for linking a binary variable Y_t with a continuous variable Q_t is to have:

Q_t >= M * Y_t (but that would require Q_t to be at least M if Y_t is 1, which is not helpful). Wait, perhaps the correct constraints are:

Q_t >= 0 (since you can't order negative quantity)

and 

Q_t <= M * Y_t 

and 

Q_t >= 0 

Wait, no. Let me think. If Y_t is 1, then Q_t can be any value (but if Y_t is 0, then Q_t must be zero). So the constraints would be:

Q_t >= 0 

Q_t <= M * Y_t 

But that would mean that if Y_t is 0, then Q_t must be zero. However, if Y_t is 1, then Q_t can be up to M. But in this problem, the fixed cost is incurred when Y_t is 1, regardless of Q_t. So the model allows for Y_t to be 1 even if Q_t is zero. But that would mean that the fixed cost is paid even if no order is placed. That's not typical. So perhaps the problem assumes that Y_t is 1 if and only if Q_t > 0. But how to model that with Big-M?

Alternatively, maybe the problem uses the Big-M method to enforce that if Y_t is 1, then Q_t must be at least some minimum (like 1), but since the problem doesn't specify, perhaps the constraints are:

Q_t >= 0 

Q_t <= M * Y_t 

But that would allow Q_t to be zero even if Y_t is 1. However, the fixed cost is incurred when Y_t is 1. So the model would allow for Y_t to be 1 even if Q_t is zero, but that would mean that the fixed cost is paid without any order. That's possible, but perhaps the problem expects that Y_t is 1 only when Q_t is positive. But since the problem doesn't specify, perhaps the correct approach is to use the Big-M constraints to link Y_t and Q_t as follows:

Q_t >= 0 

Q_t <= M * Y_t 

But then, if Y_t is 1, Q_t can be anything up to M. However, if Y_t is 0, Q_t must be zero. So the model would have the fixed cost for Y_t=1, but Q_t can be zero. But that's allowed. However, in practice, you might want to have Q_t >= 1 when Y_t=1, but since the problem doesn't specify, perhaps the given Big-M is used as per the problem's instruction.

Wait, the problem says "Use order Q_t, inventory I_t, binary order trigger Y_t, and Big-M links with M=133". So the Big-M is used to link Q_t and Y_t. The standard way to model that an order is placed (Y_t=1) if and only if Q_t > 0 is to have:

Q_t >= 0 

Q_t <= M * Y_t 

But that would allow Q_t to be zero when Y_t is 1. So perhaps the problem expects that the Big-M constraints are:

Q_t >= 0 

Q_t <= M * Y_t 

But then, the fixed cost is incurred when Y_t is 1, regardless of Q_t. So even if Q_t is zero, the fixed cost is paid. That's possible, but maybe the problem expects that Y_t is 1 only when Q_t is positive. However, without more information, I'll proceed with the standard Big-M approach.

So, the constraints for each period t:

1. Inventory balance: I_{t-1} + Q_t - demand[t-1] = I_t 

But since the initial inventory is 16, for t=1, I_0 = 16. For t=2, I_1 is the inventory after period 1, etc.

2. Big-M constraints for Q_t and Y_t:

Q_t >= 0 

Q_t <= M * Y_t 

But since M is given as 13
