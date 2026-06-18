pulp.LpProblem("single_period_newsvendor_0006", pulp.LpMinimize)

prob += 5*Q + 3*I + 5*B

prob += I + B == demand

prob += I >= Q - demand

prob += B >= demand - Q

But wait, the variables are Q, I, B. So the constraints are:

I + B = demand

I >= Q - demand

B >= demand - Q

But also, I and B are non-negative. But since we set their lowBound to 0, that's already covered.

Wait, but the variables are defined with lowBound=0. So the constraints I >= Q - demand and B >= demand - Q are necessary. 

But what if Q is less than demand? Then, I >= Q - demand would be I >= negative number, but since I is >=0, that's automatically satisfied. Similarly for B. 

So the model is correct.

Now, the code.

But let's check if the constraints are correctly added. For example, when Q is 87, then I >= 0 and B >= 0. So the constraints are satisfied.

Now, the code:

In the build_model function, the parameters are given as JSON. Wait, the parameters are in the JSON, but in the code, the demand is 87. So the code should use the parameters from the JSON. But the user provided the parameters as part of the problem. So in the code, the demand is fixed as 87. 

So the code would have:

demand = 87

unit_order_cost = 5

holding_cost = 3

shortage_cost = 5

But the user
