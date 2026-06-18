<think>
Okay, let's tackle this problem. The user wants a Python program using PuLP for the single-period newsvendor problem. The goal is to minimize the total cost, which includes ordering, holding, and shortage costs. 

First, I need to understand the problem. The decision variables are Q (order quantity), I (leftover inventory), and B (shortage). The demand is fixed at 87. The constraints must ensure that the sum of I and B equals the demand, right? Because whatever isn't ordered (Q) must either be leftover or cause a shortage. Wait, no. Wait, the demand is 87. So the total of what's ordered (Q) must satisfy the demand. But since it's a single period, the order Q is the amount ordered, and the demand is 87. So the relationship between Q, I, and B is that Q = I + B + ...? Wait, no. Let me think again.

In the newsvendor model, the demand is D. The order quantity is Q. The actual demand is D, so the leftover inventory I is max(Q - D, 0), and the shortage B is max(D - Q, 0). But in this problem, the user wants to model it with variables I and B. So the constraint would be that I + B = D. Because if you order Q, then either you have leftover (I) or shortage (B), but not both. Wait, no. Wait, if Q is greater than D, then I = Q - D and B = 0. If Q is less than D, then I = 0 and B = D - Q. So I + B = D. So the constraint is I + B = demand. But also, Q must be >= 0, I >= 0, B >= 0. 

So the problem is to choose Q, I, B such that I + B = demand, and minimize the cost: unit_order_cost * Q + holding_cost * I + shortage_cost * B. 

So the variables are Q, I, B. The constraints are I + B = demand, and all variables >= 0. 

Now, in PuLP, I need to define these variables. Let's name them Q, I, B. The objective is to minimize 5Q + 3I +5B. 

Wait, the parameters are given as unit_order_cost=5, holding_cost=3, shortage_cost=5. So the objective function is correct. 

So the steps are:

1. Import pulp and os.
2. Define the function build_model() that creates the problem.
3. In the problem, define the variables Q, I, B as continuous variables >=0.
4. Add the constraint I + B = demand (87).
5. The objective is to minimize 5Q +3I +5B.
6. Solve the problem with PULP_CBC_CMD and set msg=False.
7. Print the status and objective value.
8. If the environment variable OUTPUT_LP_PATH exists, write the LP file.

Wait, but how does Q relate to I and B? Because in the newsvendor model, Q is the order quantity, and I and B are derived from Q and demand. However, in this problem, the user wants to model it with variables I and B, but also Q. So the constraint is that Q must be such that I and B are non-negative. Wait, but how do we relate Q to I and B? Because if I and B are variables, then Q can be expressed as I + B + something? No. Wait, no. Because if I is the leftover, then I = max(Q - D, 0), and B = max(D - Q, 0). But in this problem, the user wants to model it with variables I and B, so perhaps the constraint is that Q = I + B + ...? No. Wait, maybe the constraint is that Q - I = B? Or perhaps Q = I + B? Wait, no. Let me think again.

If the demand is D, then the total of I and B must be D. Because if you order Q, then either you have I = Q - D (if Q >= D) and B = 0, or I = 0 and B = D - Q (if Q < D). So in both cases, I + B = D. Therefore, the constraint is I + B = D. But Q is the order quantity, which can be anything. However, in the problem, the user wants to minimize the cost, which includes the order cost. So Q is part of the decision variables. But how is Q related to I and B? Because if I and B are variables, then Q can be expressed as I + B + something? Wait, no. Because if I is the leftover, then Q = I + B + ...? No. Let me think again. 

If I is the leftover, then I = Q - D if Q >= D. Otherwise, I = 0. Similarly, B = D - Q if Q < D, else 0. So in any case, I + B = D. Therefore, the constraint is I + B = D. But Q can be anything. However, the cost includes 5Q, so the model must have Q as a variable. But how is Q related to I and B? Because if I and B are variables, then Q can be expressed as I + B + ...? No. Wait, perhaps Q is not directly related to I and B except through the constraint I + B = D. But then, how does Q affect the problem? Because the cost is 5Q, so the model must have Q as a variable. However, without any constraints linking Q to I and B, the model would allow Q to be any value, but I and B are constrained to sum to D. But that's not correct. Because if Q is larger than D, then I = Q - D and B = 0. If Q is smaller than D, then I = 0 and B = D - Q. So in reality, Q is not directly linked to I and B except through the relation that I and B are derived from Q and D. But in this problem, the user wants to model it with variables I and B. So perhaps the model should have Q as a variable, and the constraints are I + B = D, and Q >= I (since if Q >= D, then I = Q - D, B = 0), and Q <= D + B (since if Q < D, then B = D - Q). Wait, but that's getting complicated. 

Alternatively, perhaps the model should have Q as a variable, and I and B as variables, with the constraints that I = max(Q - D, 0), B = max(D - Q, 0). But since we can't model max in PuLP directly, we need to find a way to express these relationships. However, in this problem, the user wants to model it with variables I and B, so perhaps the correct approach is to have the constraint I + B = D, and also Q >= I (since if Q >= D, then I = Q - D, which is Q - D = I, so Q = I + D. But since I + B = D, then Q = I + D = I + (D - B) = I + D - B. Wait, this seems messy. 

Alternatively, perhaps the model should have Q as a variable, and the constraints are I = Q - D if Q >= D, else I = 0. Similarly for B. But how to model that in PuLP? That's tricky. 

Wait, but the problem says "choose order Q, leftover inventory I, and shortage B for demand 87". So the variables are Q, I, B. The constraints are that I + B = 87, and Q >= I (since if Q is larger than D, then I is positive, and B is zero. If Q is less than D, then I is zero and B is positive. So the constraint I + B = 87 is necessary. But how to ensure that Q is such that I and B are non-negative? 

Wait, perhaps the model should have the following constraints:

I + B = demand (87)

I <= Q

B <= D - Q ?

No, that's not right. Let me think again. 

If Q is the order quantity, then:

If Q >= D: I = Q - D, B = 0. So I = Q - D, B = 0. So I + B = Q - D + 0 = Q - D. But the demand is D, so this would imply that I + B = Q - D, which is not equal to D. So this approach is wrong. 

Wait, this suggests that my earlier assumption that I + B = D is incorrect. Let me re-express the problem. 

In the newsvendor model, the total demand is D. The order quantity is Q. The actual demand is D. So the leftover inventory I is max(Q - D, 0), and the shortage B is max(D - Q, 0). Therefore, I + B = max(Q - D, 0) + max(D - Q, 0) = |Q - D|. But that's not equal to D. So my earlier assumption was wrong. 

Wait, that's a problem. So the constraint I + B = D is not correct. Then what is the correct constraint? 

Let me think again. For example, if Q = 100, D = 87. Then I = 13, B = 0. So I +
