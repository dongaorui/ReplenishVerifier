import pulp and os. Then, create the LpProblem instance. The function build_model() should return the problem. 

Inside build_model(), define the variables. Q is a continuous variable, but since it's an order quantity, maybe it's integer? Wait, the problem doesn't specify that, so I'll assume it's continuous. But in practice, order quantities are integers, but the problem might not require that. Let me check the problem statement again. The parameters are given as integers, but the problem says "order quantity" which could be any non-negative real number. However, the problem might expect an integer. Hmm, but the user hasn't specified, so perhaps it's better to keep it as a continuous variable. But maybe the optimal solution is an integer. Let me think. The problem is a newsvendor model, which typically allows for continuous quantities. So I'll proceed with continuous.

So, Q = pulp.LpVariable("order_quantity", lowBound=0, cat='Continuous')

Then, the objective function is the sum of ordering cost, holding cost, and shortage cost. Let's compute each part:

ordering_cost = unit_order_cost * Q
holding_cost = holding_cost * max(Q - demand, 0)
shortage_cost = shortage_cost * max(demand - Q, 0)

But in PuLP, we can't directly use max in the objective. So we need to model these terms. However, since the problem is a single period, and the demand is known, perhaps we can express the objective as:

total_cost = unit_order_cost * Q + holding_cost * (Q - demand if Q >= demand else 0) + shortage_cost * (demand - Q if Q < demand else 0)

But how to represent this in PuLP? Well, since the problem is linear, we can split it into two parts. Let me think. The holding cost is holding_cost * (Q - demand) when Q >= demand, and zero otherwise. Similarly, the shortage cost is shortage_cost * (demand - Q) when Q < demand, and zero otherwise. 

But in linear programming, we can't have conditional expressions. So we need to model this with auxiliary variables. Wait, but since the problem is a single period and the demand is known, perhaps we can express the total cost as:

total_cost = unit_order_cost * Q + holding_cost * (Q - demand) * (Q >= demand) + shortage_cost * (demand - Q) * (Q < demand)

But PuLP doesn't support logical conditions directly. So how to model this? Alternatively, since the problem is convex and the optimal solution is at the point where the marginal cost of ordering equals the marginal cost of shortage, perhaps we can find the optimal Q without needing to model the max functions. Wait, but the user wants a linear program. 

Wait, the newsvendor problem is typically a single-period problem where the optimal order quantity is determined by the critical fractile. However, in this case, the problem is to model it as a linear program. So perhaps the way to model it is to have two variables: ending inventory (I) and shortage (S). Then, the constraints would be:

I + S = demand
I = Q - demand if Q >= demand, else I = 0
S = demand - Q if Q < demand, else S = 0

But how to express this in linear constraints. Let me think. Since I and S are non-negative, we can have:

I = max(Q - demand, 0)
S = max(demand - Q, 0)

But in PuLP, we can model this with the following constraints:

I >= Q - demand
I >= 0
S >= demand - Q
S >= 0

But then, since I and S are non-negative, these constraints would capture the max functions. However, the problem is that the total cost would be:

ordering_cost + holding_cost * I + shortage_cost * S

So, the objective function would be unit_order_cost * Q + holding_cost * I + shortage_cost * S.

But then, we need to add the constraints that I and S are non-negative, and that I + S = demand. Wait, because I + S = max(Q - demand, 0) + max(demand - Q, 0) = |Q - demand|. But since demand is fixed, I + S = |Q - demand|. However, the problem is that the total cost is unit_order_cost * Q + holding_cost * I + shortage_cost * S. 

But how to model I and S in terms of Q. Let me think again. 

Alternatively, since I = max(Q - demand, 0) and S = max(demand - Q, 0), we can model this with the following constraints:

I >= Q - demand
I >= 0
S >= demand - Q
S >= 0

But then, the total cost is unit_order_cost * Q + holding_cost * I + shortage_cost * S. 

But in this case, the problem becomes a linear program with variables Q, I, S. 

So, the constraints would be:

I >= Q - demand
I >= 0
S >= demand - Q
S >= 0
I + S = demand ?

Wait, no. Because I + S = max(Q - demand, 0) + max(demand - Q, 0) = |Q - demand|. But since demand is fixed, this is |Q - demand|. However, the sum I + S is not necessarily equal to demand. For example, if Q is greater than demand, then I = Q - demand and S = 0, so I + S = Q - demand. If Q is less than demand, then I = 0 and S = demand - Q, so I + S = demand - Q. So in both cases, I + S = |Q - demand|. But the demand is fixed, so this is not equal to demand. Therefore, the sum I + S is not equal to demand. Therefore, there's no need for that constraint. 

So, the problem can be modeled with variables Q, I, S, and the constraints:

I >= Q - demand
I >= 0
S >= demand - Q
S >= 0

But then, the objective is to minimize unit_order_cost * Q + holding_cost * I + shortage_cost * S. 

But since I and S are variables, this would be a linear program. However, the problem is that the model may have multiple solutions, but the optimal solution would be when the marginal cost of ordering is balanced with the marginal cost of shortage. 

But for the purpose of this problem, the user wants to model it as a linear program. So, perhaps this is the way to go. 

So, the variables are Q, I, S. 

But maybe we can simplify by just using Q and then express I and S in terms of Q. However, since PuLP requires linear constraints, we need to model the max functions. 

Alternatively, since the problem is a single period, and the demand is known, perhaps the optimal Q is determined by the critical fractile. But the user wants a linear program, so we need to model it as such. 

So, proceeding with the variables Q, I, S. 

Let me structure the code. 

In the build_model function, create the problem. Then, define variables Q, I, S. 

Then, add the constraints:

I >= Q - demand
I >= 0
S >= demand - Q
S >= 0

Then, the objective is unit_order_cost * Q + holding_cost * I + shortage_cost * S. 

But wait, the problem says that the order quantity is Q, and the ending inventory is I, and the shortage is S. So the total cost is ordering cost (unit_order_cost * Q) plus holding cost (holding_cost * I) plus shortage cost (shortage_cost * S). 

Yes. 

So, the code would be:

prob = pulp.LpProblem("single_period_newsvendor_0002", pulp.LpMinimize)

Q = pulp.LpVariable("order_quantity", lowBound=0, cat='Continuous')
I = pulp.LpVariable("ending_inventory", lowBound=0, cat='Continuous')
S = pulp.LpVariable("shortage", lowBound=0, cat='Continuous')

prob += unit_order_cost * Q + holding_cost * I + shortage_cost * S

prob += I >= Q -
