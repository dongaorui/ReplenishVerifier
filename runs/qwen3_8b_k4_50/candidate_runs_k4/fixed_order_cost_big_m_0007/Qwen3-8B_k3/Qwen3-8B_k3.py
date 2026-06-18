<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP to solve an inventory replenishment optimization problem. Let me start by understanding the problem details.

The problem has 3 periods. Initial inventory is 12, and demands are 23, 24, 29. We need to decide the order quantity Q_t each period, inventory I_t, and a binary variable Y_t indicating if an order is placed. The fixed order cost is 24, unit order cost is 2, holding cost is 2. Also, we need to use Big-M method with M=76 to link Q_t and Y_t.

First, I need to set up the PuLP model. Let me recall how to structure this. The model will have variables for Q_t, I_t, and Y_t. The objective is to minimize the sum of unit order costs, holding costs, and fixed order costs. 

The constraints are:
1. Inventory balance: For each period, inventory after demand must equal previous inventory plus order quantity minus demand. But since the initial inventory is given, I need to handle the first period correctly.
2. The order quantity Q_t must be zero when Y_t is zero, and at least zero when Y_t is one. This is where the Big-M comes in. So, Q_t >= M * Y_t? Wait, no. Wait, the Big-M method is used to enforce that if Y_t is 1, then Q_t must be at least some value. Wait, actually, the standard approach is to have Q_t >= M * Y_t, but since M is a large number, this would force Q_t to be zero if Y_t is zero. Wait, no. Wait, if Y_t is 1, then Q_t can be any value, but if Y_t is 0, then Q_t must be zero. Wait, no. Wait, the binary variable Y_t indicates whether an order is placed. So, if Y_t is 1, then an order is placed, so Q_t can be positive. If Y_t is 0, then no order is placed, so Q_t must be zero. So the constraint would be Q_t >= M * Y_t? Wait, no. Wait, if Y_t is 0, then Q_t must be zero. So to enforce that, we can have Q_t <= M * Y_t. Wait, but that would require that if Y_t is 0, Q_t must be zero. But since M is a large number, if Y_t is 1, then Q_t can be up to M. But how to link Q_t and Y_t. Let me think again.

The standard Big-M formulation for a binary variable Y_t and a continuous variable Q_t where Q_t is zero when Y_t is zero and can be any non-negative value when Y_t is 1. So the constraints would be:

Q_t >= 0
Q_t <= M * Y_t
Y_t is binary.

Wait, no. Wait, if Y_t is 0, then Q_t must be zero. So Q_t <= M * Y_t would ensure that. Because if Y_t is 0, then Q_t must be <= 0, but since Q_t is non-negative, that forces Q_t to be zero. But if Y_t is 1, then Q_t can be up to M. But in this problem, the order quantity can be any non-negative value when Y_t is 1. So that's correct. However, the problem says to use Big-M links with M=76. So the M here is 76. So the constraints would be Q_t <= M * Y_t. But also, we need to ensure that if Y_t is 1, then Q_t can be any value. But since the problem allows for any Q_t when Y_t is 1, this constraint is sufficient. However, perhaps there's another constraint to ensure that Q_t is non-negative. So, Q_t >= 0. 

But wait, the problem says "Use order Q_t, inventory I_t, binary order trigger Y_t, and Big-M links with M=76". So the Big-M is used to link Q_t and Y_t. So the constraints would be Q_t >= 0 and Q_t <= M * Y_t. Wait, but that would mean that when Y_t is 1, Q_t can be up to M. But the actual order quantity could be larger than M? No, because M is chosen as a sufficiently large number. But in this case, the M is given as 76. So perhaps the problem expects that the Big-M is used to model the relationship between Q_t and Y_t. 

But maybe the problem requires that Q_t is zero when Y_t is zero, and can be any value when Y_t is 1. So the constraints would be Q_t >= 0 and Q_t <= M * Y_t. Wait, but that would allow Q_t to be up to M when Y_t is 1. But if the actual required order quantity is larger than M, then this would be a problem. However, since M is given as 76, perhaps the problem assumes that the maximum possible order quantity is 76. But in this case, the demands are 23, 24, 29. The initial inventory is 12. Let's see. For example, in period 1, initial inventory is 12, demand is 23. So if we don't order, the inventory would be 12 - 23 = -11, which is not allowed. So we must order in period 1. So Y_1 must be 1. So Q_1 must be at least 23 - 12 = 11 (since inventory after order is 12 + Q_1 - 23 >= 0). Wait, but the inventory after order is I_1 = initial_inventory + Q_1 - demand_1. Wait, no. Wait, the inventory after order is I_1, which is the inventory before demand. Wait, maybe the inventory balance is:

I_t = I_{t-1} + Q_t - demand_t.

But initial inventory is I_0 = 12. Then for t=1, I_1 = I_0 + Q_1 - demand_1. Then I_1 must be >= 0. So for period 1, I_0 is 12, demand is 23. So I_1 = 12 + Q_1 - 23 >= 0 → Q_1 >= 11. So the order quantity must be at least 11. But if Y_1 is 1, then Q_1 can be any value >= 11. But according to the Big-M constraints, Q_1 <= M * Y_1. Since M is 76, and Y_1 is 1, Q_1 can be up to 76. But the actual required Q_1 is 11. So the model would allow that. 

So the constraints for Q_t and Y_t are:

Q_t >= 0
Q_t <= M * Y_t
Y_t is binary.

But wait, that would allow Q_t to be zero when Y_t is 1, which is not allowed. Wait, no. Because if Y_t is 1, then Q_t can be zero? But that would mean that the order is placed (Y_t=1) but the order quantity is zero. That's not allowed. So perhaps the constraints should be Q_t >= 0 and Q_t >= M * (1 - Y_t). Wait, no. Wait, the standard way to model that if Y_t is 1, then Q_t must be at least some value. Wait, maybe the problem requires that when Y_t is 1, Q_t must be at least the required quantity to meet the demand. But perhaps the problem is more about linking Y_t and Q_t such that Y_t=1 implies that Q_t is positive. But the problem says "binary order trigger Y_t", which probably means that Y_t=1 indicates that an order is placed, but the actual quantity can be any non-negative value. However, in reality, if Y_t=1, then Q_t must be at least the amount needed to meet the demand. But perhaps the problem doesn't require that, and the constraints are only about the relationship between Q_t and Y_t. 

Wait, the problem says "Use order Q_t, inventory I_t, binary order trigger Y_t, and Big-M links with M=76". So the Big-M is used to link Q_t and Y_t. So the standard approach is to have Q_t >= 0 and Q_t <= M * Y_t. But that would allow Q_t to be zero when Y_t is 1, which is not allowed. So perhaps the correct constraints are Q_t >= 0 and Q_t >= (some minimum) * Y_t. Wait, but how to ensure that if Y_t is 1, then Q_t is positive. 

Alternatively, perhaps the problem requires that Y_t=1 if and only if Q_t > 0. So the constraints would be Q_t >= 0, and Q_t <= M * Y_t, and Q_t >= (some epsilon) * Y_t. But since the problem doesn't mention any minimum order quantity, maybe the constraints are just Q_t >= 0 and Q_t <= M * Y_t. But then, if Y_t is 1, Q_t can be zero. Which would be an order placed with zero quantity. That's not allowed. So perhaps the correct constraints are Q_t >= 0
