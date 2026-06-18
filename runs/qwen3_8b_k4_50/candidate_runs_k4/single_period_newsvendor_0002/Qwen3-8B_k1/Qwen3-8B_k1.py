import pulp and os. Then, define the function build_model() that returns the LpProblem. The problem name could be something like "single_period_newsvendor_0002".

In the function, create the problem instance. Then, define the variable Q. Since Q can't be negative, we set the bounds to 0. Then, the objective function is the sum of the three costs. Let me compute each part:

ordering_cost = unit_order_cost * Q
holding_cost = holding_cost * max(Q - demand, 0)
shortage_cost = shortage_cost * max(demand - Q, 0)

But in PuLP, how do I express max? Well, since Q is a variable, we can use the pulp.lpSum function with expressions. However, the max function can be represented using constraints. Wait, but in this case, since we are dealing with a single variable, maybe we can model it with two variables: ending_inventory and shortage. Wait, but maybe it's easier to express the objective directly using the max functions. However, PuLP doesn't support max in the objective directly. So we need to model it with auxiliary variables.

Wait, but in this case, since the problem is a single variable, perhaps we can express the objective as:

total_cost = unit_order_cost * Q + holding_cost * (Q - demand) if Q >= demand else 0 + shortage_cost * (demand - Q) if Q < demand else 0

But how to model this in PuLP. Alternatively, we can split the objective into two parts. Let me think. Let me define two variables: inventory and shortage. But maybe that's complicating. Alternatively, since the problem is convex, maybe we can express the objective as:

total_cost = unit_order_cost * Q + holding_cost * (Q - demand) + shortage_cost * (demand - Q) 

But that would be incorrect because when Q >= demand, the holding cost is (Q - demand) and the shortage cost is zero. When Q < demand, the holding cost is zero and the shortage cost is (demand - Q). So the total cost can be written as:

total_cost = unit_order_cost * Q + max( (Q - demand) * holding_cost, 0 ) + max( (demand - Q) * shortage_cost, 0 )

But how to model this in PuLP. Since PuLP doesn't support max in the objective directly, we need to use constraints to represent the max terms. However, since this is a single variable, maybe we can model it with two terms. Let me think. Let me consider that the total cost is:

total_cost = unit_order_cost * Q + holding_cost * (Q - demand) * (Q >= demand) + shortage_cost * (demand - Q) * (Q < demand)

But how to represent this in PuLP. Alternatively, since the problem is a single variable, maybe we can use the fact that the optimal Q is where the marginal cost of ordering one more unit equals the marginal benefit. But perhaps that's not necessary here. Let me think again.

Alternatively, since the problem is a single variable, we can express the objective as:

total_cost = unit_order_cost * Q + holding_cost * max(Q - demand, 0) + shortage_cost * max(demand - Q, 0)

But how to model this in PuLP. The max function can be represented using auxiliary variables and constraints. For example, for the holding cost term, we can have:

inventory = Q - demand
if inventory >= 0, then holding_cost * inventory, else 0.

But how to model that. Let me think. Let me create a variable for the inventory and another for the shortage. But perhaps it's easier to model the objective as:

total_cost = unit_order_cost * Q + holding_cost * (Q - demand) + shortage_cost * (demand - Q) 

But that would be incorrect because when Q is less than demand, the holding cost term would be negative, but we need to have zero. So that approach would not work. Therefore, we need to model the max terms properly.

Alternatively, since the problem is convex and the optimal solution is at the point where the marginal cost of ordering equals the marginal benefit, perhaps we can find the optimal Q analytically. But the user wants a linear program. Wait, but the problem is a single variable and the objective is convex, so it's a convex optimization problem. However, the max functions make it non-linear. Wait, but the problem says to formulate a linear program. So maybe there's a way to linearize it.

Wait, the problem says "formulate and solve the corresponding linear program". So the model must be linear. Therefore, the max functions need to be represented with linear constraints.

Let me think again. Let me define two variables: inventory and shortage. Let me have:

inventory = max(Q - demand, 0)
shortage = max(demand - Q, 0)

But since inventory and shortage are non-negative, and Q is the order quantity. Then, the total cost is:

unit_order_cost * Q + holding_cost * inventory + shortage_cost * shortage

But how to model inventory and shortage in terms of Q and demand. Since inventory = Q - demand if Q >= demand, else 0. Similarly for shortage.

So, we can model this with two constraints:

inventory = Q - demand if Q >= demand, else 0
shortage = demand - Q if Q < demand, else 0

But how to express this in PuLP. Let me think. We can add constraints that:

inventory >= Q - demand
inventory >= 0
shortage >= demand - Q
shortage >= 0

But that's not sufficient. Because inventory is the max(Q - demand, 0), which can be represented as:

inventory >= Q - demand
inventory >= 0
and inventory is a variable.

Similarly for shortage:

shortage >= demand - Q
shortage >= 0

But then, how to ensure that inventory and shortage are correctly calculated. However, since the problem is to minimize the total cost, which includes holding_cost * inventory + shortage_cost * shortage, and the other terms, perhaps we can proceed.

But this approach would require adding these constraints. Let me try to model this.

So, the variables would be Q, inventory, and shortage. But since inventory and shortage are dependent on Q, perhaps we can model them as variables with constraints.

Alternatively, since inventory and shortage are non-negative, and Q is the order quantity, we can model:

inventory = max(Q - demand, 0)
shortage = max(demand - Q, 0)

But how to express this in PuLP. Let me think. For the inventory variable, we can have:

inventory >= Q - demand
inventory >= 0

Similarly, for shortage:

shortage >= demand - Q
shortage >= 0

But then, the total cost would be:

unit_order_cost * Q + holding_cost * inventory + shortage_cost * shortage
