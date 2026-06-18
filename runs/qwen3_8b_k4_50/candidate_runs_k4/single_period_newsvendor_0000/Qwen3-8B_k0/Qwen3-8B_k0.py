pulp.LpProblem("single_period_newsvendor_0000", pulp.LpMinimize)

2. Define variables. 

Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')

I = pulp.LpVariable("I", lowBound=0, cat='Continuous')

B = pulp.LpVariable("B", lowBound=0, cat='Continuous')

3. Objective function: 1*Q + 1*I + 9*B. 

prob += 1*Q + 1*I + 9*B, "Objective"

4. Constraint: Q - I + B = 111. 

prob += Q - I + B == 111, "DemandConstraint"

Wait, but the problem says "demand satisfaction". So that's the constraint. 

Then, solve with PULP_CBC_CMD, set msg=False. 

Then print the status and objective. 

Also, check if the environment variable OUTPUT_LP_PATH exists. 

So the code should have:

import pulp
import os

def build_model():
    prob = pulp.LpProblem("single_period_newsvendor_0000", pulp.LpMinimize)
    # variables
    Q = pulp.LpVariable("Q", lowBound=0, cat='Continuous')
    I = pulp.LpVariable("I", lowBound=0, cat='Continuous')
    B = pulp.LpVariable("B", lowBound=0, cat='Continuous')
    # objective
    prob += 1*Q + 1*I + 9*B, "Objective"
    # constraints
    prob += Q - I + B == 111, "DemandConstraint"
    return prob

if __name__ == "__main__":
    prob = build_model()
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))

Wait, but the problem says to define the function build_model() that returns the prob. Then in the main block, call it. 

Yes. 

But wait, the problem says "choose order Q, leftover inventory I, and shortage B for demand 111". So the variables are Q, I, B. 

But in the model, the constraint is Q - I + B = 111. 

But let me check if that's correct. 

Let me think of an example. Suppose Q=111, then I=0, B=0. Then the constraint is 111 - 0 + 0 = 111. Correct. 

If Q=100, then I=0, B=11. Then 100 - 0 + 11 = 111. Correct. 

If Q=120, then I=9, B=0. 120 -9 +0 = 111. Correct. 

Yes, that's correct. 

So the model is correct. 

Now, the code should be written as per the user's instructions. 

But the user also says to give decision variables meaningful names. Which they are. 

Also, the constraints are named with descriptive strings. 

So the code should be as written. 

Now, check the hard requirements:

- import pulp and os: yes.

- prob = pulp.LpProblem(...): yes.

- solve with PULP_CBC_CMD(msg=False): yes.

- print status and objective: yes.

- define build_model() that returns prob: yes.

- in main, call build_model, write LP if env var exists: yes.

- only one code block, no explanations.

So the code should be correct. 

But wait, the problem says "Minimize 1Q + 1I + 9B subject to demand satisfaction." So the model is correct. 

Now, what is the optimal solution? Let's think. 

The objective is Q + I +9B. 

But from the constraint Q - I + B = 111. 

We can express I = Q + B - 111. 

But since I >=0, Q + B -111 >=0 → Q + B >= 111. 

But substituting into the objective: Q + (Q + B -111) +9B = 2Q +10B -111. 

But since Q can be expressed in terms of B? Or maybe not. 

Alternatively, since Q can be any value as long as Q + B >= 111. 

But the problem is to minimize 2Q +10B -111. 

But since Q and B
