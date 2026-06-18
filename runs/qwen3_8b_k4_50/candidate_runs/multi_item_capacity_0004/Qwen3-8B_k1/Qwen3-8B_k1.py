import pulp and os.

Then, define the build_model function.

Inside build_model:

- Read the parameters from the JSON. But since the parameters are given as a JSON, but in the code, they are hard-coded. Wait, the user provided the parameters as JSON, but in the code, they need to be included as variables. So, in the code, the parameters are:

items = 3

periods = 5

initial_inventory = [3, 3, 17]

demand = [[18, 32, 14, 25, 33], [28, 20, 38, 44, 29], [49, 43, 10, 45, 29]]

volume = [1, 2, 3]

storage_capacity = 99

unit_order_cost = [3, 3, 5]

holding_cost = [2, 3, 2]

So,
