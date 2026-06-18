import pulp
import os

def build_model():
    prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)
    # define variables
    Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')
    excess = pulp.LpVariable("excess", lowBound=0, cat='Continuous')
    shortage = pulp.LpVariable("shortage", lowBound=0, cat='Continuous')
    # add constraints
    prob += excess >= Q - demand
    prob += excess >= 0
    prob += shortage >= demand - Q
    prob += shortage >= 0
    # objective function
    prob += unit_order_cost * Q + holding_cost * excess + shortage_cost * shortage
    return prob

Wait, but the parameters are given as JSON. So in the code, the parameters are fixed. Wait, the problem says that the parameters are given as JSON, but in the code, they are hard-coded. Wait, the user provided the parameters as JSON, but in the code, we need to use them. So in the code, the parameters are:

demand = 84
unit_order_cost = 1
holding_cost = 1
shortage_cost = 6

But the code should use these values. So in the code, the parameters are fixed. So the code would have these variables defined.

But the function build_model() would need to have access to these parameters. So perhaps the code would have the parameters defined in the main block, and then the build_model function uses them.

Wait, but the user's problem says that the parameters are given as JSON. So perhaps the code should read them from the JSON, but the user's example shows that the parameters are fixed. However, the user's problem says that the parameters are given as JSON, but in the code, they are hard-coded. So maybe the code should have the parameters as variables.

So in the code, the parameters are:

demand = 84
unit_order_cost = 1
holding_cost = 1
shortage_cost = 6

But the code must be written with these values. So the code would have these variables defined.

So putting it all together.

Now, the code structure:

import pulp
import os

def build_model():
    prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)
    # parameters
    demand = 84
    unit_order_cost = 1
    holding_cost = 1
    shortage_cost = 6
    # variables
    Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')
    excess = pulp.LpVariable("excess", lowBound=0, cat='Continuous')
    shortage = pulp.LpVariable("shortage", lowBound=0, cat='Continuous')
    # constraints
    prob += excess >= Q - demand
    prob += excess >= 0
    prob += shortage >= demand - Q
    prob += shortage >= 0
    # objective
    prob += unit_order_cost
