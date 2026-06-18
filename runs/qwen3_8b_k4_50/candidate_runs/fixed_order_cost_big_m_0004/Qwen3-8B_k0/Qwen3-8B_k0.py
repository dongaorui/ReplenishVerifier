import pulp and os.

Then, define the periods as 6. The initial inventory is 15. The demand is a list of 6 elements.

We need to create variables for each period. Let's index from 0 to 5 (since there are 6 periods). So for t in 0 to 5:

Q_t: quantity ordered in period t.

I_t: inventory after period t.

Y_t: binary variable indicating if an order is placed in period t.

But the initial inventory is I_0 = 15. Wait, no. Wait, the initial inventory is before the first period. So for period 0 (assuming 0-based), the inventory before demand is 15. Then after demand, it's 15 - demand[0] + Q_0. But that would
