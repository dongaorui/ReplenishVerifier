import pulp 

import os 

prob = pulp.LpProblem(...) 

prob.solve(...) 

print status and objective. 

Also, the function build_model() returns the prob. 

So putting it all together. 

Let me check the parameters again. 

demand is 116. 

unit_order_cost is 5. 

holding_cost is 1. 

shortage_cost is 14. 

So the objective is 5*Q + 1*I + 14*S. 

So the code would be:

def build_model():
    prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)
    demand = 116
    unit_order_cost = 5
    holding_cost = 1
    shortage_cost = 14

    # Decision variables
    Q = pulp.LpVariable("Order_Quantity", lowBound=0, cat='Continuous')
    I = pulp.LpVariable("Ending_Inventory", lowBound=0, cat='Continuous')
    S = pulp.LpVariable("Shortage", lowBound=0, cat='Continuous')

    # Objective function
    prob += unit_order_cost * Q + holding_cost * I + shortage_cost * S

    # Constraints
    prob += I >= Q - demand
    prob += S >= demand
