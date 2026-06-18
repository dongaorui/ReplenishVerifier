import pulp
import os

def build_model():
    prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)
    # Variables
    Q = pulp.LpVariable("Order_Quantity", lowBound=0, cat='Continuous')
    I = pulp.LpVariable("Ending_Inventory", lowBound=0, cat='Continuous')
    S = pulp.LpVariable("Shortage", lowBound=0, cat='Continuous')
    
    # Objective function
    prob += 5*Q + 1*I + 14*S, "Total_Cost"
    
    # Constraints
    prob += I + S == 116, "Demand_Satisfied"
    prob += I >= Q - 116, "Inventory_Lower_Bound"
    prob += S >= 116 - Q, "Shortage_Lower_Bound"
    
    return prob

Then, in the main block:

if __name__ == "__main__":
    prob = build_model()
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))

Wait, but the problem says that the demand is given as 116, so the constraints are fixed. But in the code, the demand is hard-coded as 116. However, the parameters are passed via JSON, but in the code, the parameters are fixed. Wait, the user provided the parameters as JSON, but in the code, the parameters are fixed. But the code should use the parameters from the JSON. Wait, the problem says that the code should use the parameters given in the JSON. But in the code, the parameters are hard-coded. Wait, the user's JSON parameters are:

{
  "demand": 116,
  "unit_order_cost": 5,
  "holding_cost": 1,
  "shortage_cost": 14
}

So the code should use these values. But in the code, the parameters are hard-coded. So the code is correct as per the given parameters. But the user might want the code to be parameterized. However, the problem says that the code should be written for the given parameters, so hard-coding is acceptable here.

But wait, the code uses the parameters from the JSON. So in the code, the variables are defined with the correct coefficients. So the code is correct.

Testing this model, the optimal solution would be Q=116, I=0, S=0. The total cost is 5*116 = 580. Let me check if the constraints are satisfied.

I + S = 116: 0 + 0 = 116? No, that's not possible. Wait, there's a mistake here. Oh no! Wait, the constraint I + S = demand is 116. But if Q is 116, then I = Q - demand = 0, S = 0. So I + S = 0, which is not equal to 116. That's a problem. Wait
