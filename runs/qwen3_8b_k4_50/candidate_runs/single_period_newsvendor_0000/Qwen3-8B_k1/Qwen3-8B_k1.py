import pulp
import os

def build_model():
    prob = pulp.LpProblem("single_period_newsvendor_0000", pulp.LpMinimize)
    # Decision variables
    Q = pulp.LpVariable("Order_Quantity", lowBound=0, cat='Continuous')
    I = pulp.LpVariable("Leftover_Inventory", lowBound=0, cat='Continuous')
    B = pulp.LpVariable("Shortage", lowBound=0, cat='Continuous')
    
    # Objective function: minimize total cost
    prob += Q + I + 9*B, "Total_Cost"
    
    # Constraint: demand satisfaction
    prob += Q + I - B == 111, "Demand_Satisfaction"
    
    return prob

if __name__ == "__main__":
    prob = build_model()
    # Write LP file if output path is specified
    if 'OUTPUT_LP_PATH' in os.environ:
        prob.writeLP(os.environ["OUTPUT_LP_PATH"])
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    # Print results
    print("STATUS:", pulp.LpStatus[prob.status])
    print("OBJECTIVE:", pulp.value(prob.objective))
