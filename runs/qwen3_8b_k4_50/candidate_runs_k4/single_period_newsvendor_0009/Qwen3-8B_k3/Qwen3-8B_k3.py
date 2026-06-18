pulp.LpProblem("single_period_newsvendor_0009", pulp.LpMinimize)
    # Define variables
    Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')
    I = pulp.LpVariable("I", lowBound=0, cat='Continuous')
    B = pulp.LpVariable("B", lowBound=0, cat='Continuous')
    # Objective function
    prob += 4*Q + 1*I + 10*B
    # Constraint: Q - I + B = demand (41)
    prob += Q - I + B == 41, "DemandConstraint"
    return prob

Then, in the main block:

import os
import pulp

def build_model():
    # ... as above

if __name__ == "__main__":
    prob = build_model()
    # Check for output path
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))

Wait, but the user requires that the code must contain the import pulp, import os, and the prob = pulp.LpProblem(...) etc. So the code should have all that.

Also, the user says to define the function build_model() that returns the prob. So the code should have that function.

Now, checking the constraints. The constraint is Q - I + B = 41. That's correct.

Now, solving this problem. Let's think about the optimal solution. The objective is to minimize 4Q + I + 10B. The constraint is Q - I + B = 41. Let's express variables in terms of others. For example, B = 41 - Q + I. Substitute into the objective:

4Q + I + 10*(41 - Q + I) = 4Q + I + 410 -10Q +10I = -6Q +11I +410. 

But since B must be >=0, 41 - Q + I >=0 => I >= Q -41. But since I >=0, this implies that Q -41 <= I. But I is non-negative. So Q can be anything, but B must be non-negative. 

Alternatively, perhaps we can express the problem in terms of Q. Let me think. Since the constraint is Q - I + B = 41, and I and B are non-negative. 

But perhaps the optimal solution is to set I=0 and B=41 - Q. Then the objective becomes 4Q + 0 + 10*(41 - Q) = 4Q + 410 -10Q = -6Q +410. To minimize this, since the coefficient of Q is negative, we want to maximize Q. However, Q can't be more than 41, because if Q is larger than 41, then B would be 41 - Q + I. Wait, no. If Q is larger than 41, then I would be Q -41, and B would be 0. Because in that case, the constraint is Q - I + B =41. If Q is larger than 41, then I can be Q -41, B=0. So substituting into the objective: 4Q + (Q -41) + 0 = 5Q -41. Which increases as Q increases. So the objective would be minimized when Q is as small as possible. 

Wait, this seems conflicting. Let me think again. 

If we set I=0 and B=41 - Q, then Q must be <=41, because B can't
