import pulp and os. Then define the build_model function that returns the LpProblem. 

In the build_model function, create the problem, define variables Q, I, B as continuous variables. 

Then add the constraint Q - I + B == demand. 

The objective is 2*Q + 2*I +6*B. 

Then solve with PULP_CBC_CMD, set msg=False. 

Then print the status and objective value. 

Also, check if the environment variable OUTPUT_LP_PATH exists, and write the LP file if so. 

So the code structure would be:

import pulp
import os

def build_model():
    prob = pulp.LpProblem("single_period_newsvendor_0001", pulp.LpMinimize)
    # define variables
    Q = pulp.LpVariable("Q", lowBound=0)
    I = pulp.LpVariable("I", lowBound=0)
    B = pulp.LpVariable("B", lowBound=0)
    # objective function
    prob += 2*Q + 2*I + 6*B
    # constraint
    prob += Q - I + B == 61, "DemandConstraint"
    return prob

if __name__ == "__main__":
    prob = build_model()
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))

Wait, but the problem says to have the function build_model() return the prob. Then in the main block, call build_model(), and proceed. 

Yes. 

Now, check if the variables are correctly defined. 

But wait, the problem says to choose Q, I, B. So the variables are Q, I, B. 

But in the model, the constraint is Q - I + B = 61. 

Yes. 

Now, solving this model. Let's think about the optimal solution. 

The objective is to minimize 2Q + 2I +6B. 

But since Q - I + B = 61, we can express one variable in terms of the others. For example, B = 61 - Q + I. 

Substituting into the objective: 2Q + 2I +6*(61 - Q + I) = 2Q + 2I + 366 -6Q +6I = -4Q +8I +366. 

To minimize this, we need to maximize Q and minimize I. But since Q and I are non-negative, but also B must be non-negative. 

So B = 61 - Q + I ≥ 0. 

But since Q and I are variables, how do we find the optimal solution? 

Alternatively, since the problem is linear, the optimal solution will be at the boundary. 

But perhaps the optimal solution is to set I=0 and B=0, but that would require Q=61. Then the objective is 2*61 + 0 +0 = 122. 

But if we set Q=61, then I=0, B=0. 

But what if we set Q=61, I=0, B=0. 

But let's check the constraint: Q - I + B = 61 -0 +0 =61, which is correct. 

But maybe there's a better solution. 

Wait, let's think. Suppose we set I=0, then B = 61 - Q. 

So the objective becomes 2Q + 0 +6*(61 - Q) = 2Q + 366 -6Q = -4Q + 366. 

To minimize this, we need to maximize Q. But since B must be ≥0, 61 - Q ≥0 → Q ≤61. So maximum Q is 61. Then the objective is -4*61 +366 = -244 +366 = 122. Which is the same as before. 

Alternatively, if we set B=0, then Q - I =61 → I = Q -61. But since I ≥0, Q must be ≥61. Then the objective is 2Q + 2*(Q-61) +0 = 2Q +2Q -122 =4Q -122. To minimize this, we need to minimize Q. The minimum Q is 61, leading to 4*61 -122 = 244 -122 = 122. Same as before. 

So the optimal solution is Q=61, I=0, B=0, with
