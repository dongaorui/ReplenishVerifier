import pulp
import os

def build_model():
    prob = pulp.LpProblem("single_period_newsvendor_0008", pulp.LpMinimize)
    # define variables
    Q = pulp.LpVariable('Q', lowBound=0)
    I = pulp.LpVariable('I', lowBound=0)
    S = pulp.LpVariable('S', lowBound=0)
    # objective
    prob += 2*Q + 3*I + 6*S
    # constraint
    prob += Q - I - S == 49
    return prob

Then, in the main block:

if __name__ == "__main__":
    prob = build_model()
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))

Wait, but the problem says to have the function build_model() return the prob. 

But in the code, the variables are defined inside the function. 

But wait, the problem says to have the function build_model() return the LpProblem object. 

Yes. 

But let me check if the model is correct. 

Let me think about the optimal solution. 

In the newsvendor problem, the optimal order quantity Q is determined by the critical fractile. The critical fractile is (C_s + C_h) / (C_s + C_h + C_o), but wait, maybe I need to recall the formula. 

Wait, in the newsvendor model, the cost of overstocking is
