import pulp and os. 

Then, define the build_model function. 

In the build_model function, create the LpProblem. 

Define the variables. 

For x_t, we can have a list of variables, each for each period. 

Similarly for I_t. 

But in PuLP, variables can be created with loops. 

So, for periods 0 to 4 (assuming 0-based index), but the problem has periods 1 to 5. 

Wait, the problem has T=5 periods. Let's index them from 0 to 4. 

But the initial inventory is I_0 = 19. 

So for each period t in 0 to 4 (assuming 0-based), the demand is given as demand[t]. 

Wait, the demand list is [31, 17, 44, 49, 22], which is for periods 1 to 5. So if we index from 0 to 4, then demand[0] is period 1's demand. 

But perhaps it's easier to index from
