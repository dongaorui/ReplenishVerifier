pulp.LpProblem("SinglePeriodNewsvendor", pulp.LpMinimize)

Q = pulp.LpVariable('Q', lowBound=0, cat='Continuous')

I = pulp.LpVariable('I', lowBound=0, cat='Continuous')

B = pulp.LpVariable('B', lowBound=0, cat='Continuous')

prob += 5*Q + 3*I +5*B, "TotalCost"

prob += I + B == 87, "DemandConstraint"

prob += I <= Q, "I_LessThanOrEqualToQ"

Then solve it.

Wait, but what about the case where Q is less than I? Because if I is allowed to be up to Q, then that's handled by the constraint I <= Q. So that's correct.

So the model should be correct.

Now, the user wants the code to have the function build_model() that returns the problem. So the code structure would be:

import pulp

import os

def build_model():

    prob = pulp.LpProblem("SinglePeriodNewsvendor", pulp.LpMinimize)

    # define variables

    # add constraints

    # set objective

    return prob

Then, in the main block:

prob = build_model()

if 'OUTPUT_LP_PATH' in os.environ:

    prob.writeLP(os.environ["OUTPUT_LP_PATH"])

prob.solve(pulp.PULP_CBC_CMD(msg=False))

print("STATUS:", pulp.LpStatus[prob.status])

print("OBJECTIVE:", pulp.value(prob.objective))

So putting it all together.

Wait, but the variables are Q, I, B. Let me check if the code is correct.

Another thing to consider: the problem may have multiple optimal solutions. For example, if Q is set to 87, then I = 87 - B. But since B is zero, I is 87. But then I can't be more than Q. So if Q is 87, then I can be 87, B is zero. But that would require that I <= Q (87 <= 87), which is okay. So that's valid.

Alternatively, if Q is 90, then I = 3, B = 84. But then I =3 <= Q=90, which is okay.

So the model is correct.

Now, the code should be written with the function build
