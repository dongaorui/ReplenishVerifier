import pulp and os. Then create the problem. 

The function build_model() should return the LpProblem. 

In the problem, the objective is to minimize 2*Q + 2*I + 6*B. 

Constraints:

1. Q + B - I = 61 (demand satisfaction)
2. Q >= 0
3. I >= 0
4. B >= 0

So in PuLP, we need to define these variables and constraints. 

Let me think about the variables. 

We can define Q, I, B as continuous variables. 

So in code:

prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)

Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')
I = pulp.LpVariable("I", lowBound=0, cat='Continuous')
B = pulp.LpVariable("B", lowBound=0, cat='Continuous')

Then the objective function is 2*Q + 2*I + 6*B. 

prob += 2*Q + 2*I + 6*B, "Objective"

Then the constraint: Q + B - I == 61. 

prob += Q + B - I == 61, "Demand_Satisfaction"

Then solve with PULP_CBC_CMD, and print the status and objective value.

Wait, but the problem says to have the function build_model() that returns the prob. So the code structure would be:

def build_model():
    prob = pulp.LpProblem(...)
    # define variables
    # add constraints and objective
    return prob

Then in the main block, call build_model(), solve, etc.

Also, check for the environment variable OUTPUT_LP_PATH. If it exists, write the LP file.

So putting it all together.

Now, the code must include:

import pulp
import os

def build_model():
    prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)
    Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')
    I = pulp.LpVariable("I", lowBound=0, cat='Continuous')
    B = pulp.LpVariable("B", lowBound=0, cat='Continuous')
    prob += 2*Q + 2*I + 6*B, "Objective"
    prob += Q + B - I == 61, "Demand_Satisfaction"
    return prob

if __name__ == "__main__":
    prob = build_model()
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))

Wait, but the problem says to have the function build_model() return the prob. So that's correct.

But wait, the problem says that the parameters are given as JSON. But in this case, the parameters are fixed. The demand is 61, and the costs are given. So the code uses those values directly. 

But the user's JSON parameters are:

{
  "demand": 61,
  "unit_order_cost": 2,
  "holding_cost": 2,
  "shortage_cost": 6
}

So the objective is unit_order_cost * Q + holding_cost * I + shortage_cost * B. Which is 2Q + 2I + 6B. So that's correct.

So the code is correct. 

Now, check if the constraints are properly named. The constraint is named "Demand_Satisfaction".

Yes. 

So the code should work. Let me test it mentally. 

The optimal solution would be to choose Q such that the cost is minimized. Let's think about the problem. 

The constraint is Q + B - I = 61. Since I and B are non-negative, we can express this as Q = 61 + I - B. But since I and B are non-negative, this might not be straightforward. 

Alternatively, since the problem is linear, the optimal solution will be at the boundary. Let's think about the possible cases. 

If we order Q = 61, then I = 0, B = 0. The cost is 2*61 + 2*0 + 6*0 = 122. 

If we order Q = 60, then B = 1, I = 0. Cost is 2*60 + 2*0 + 6*1 = 120 + 6 = 126. Which is worse. 

If we order Q = 62, then I = 1, B = 0. Cost is 2*62 + 2*1 + 6*0 = 124 + 2 = 126. Also worse. 

So the minimum is at Q=61, I=0, B
