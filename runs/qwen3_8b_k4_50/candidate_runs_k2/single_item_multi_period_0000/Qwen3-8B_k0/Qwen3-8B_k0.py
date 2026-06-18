<think>
Okay, I need to create a Python program using PuLP to solve this inventory replenishment problem. Let me start by understanding the problem.

The problem is about planning the replenishment of a single item over 5 periods. The initial inventory is 19, and the demands for each period are given as [31, 17, 44, 49, 22]. The goal is to minimize the total cost, which includes order costs and holding costs. The order cost is 4 per order, and the holding cost is 1 per unit held.

First, I need to define the decision variables. The main variables here are the order quantities for each period and the inventory levels at the end of each period. Let me think: for each period, we decide how much to order (let's call this variable 'order'), and the inventory after meeting demand will be the previous inventory plus the order minus the demand. 

Wait, the inventory balance constraints are crucial here. For each period, the inventory at the start plus the order equals the inventory at the end plus the demand. Or maybe it's the other way around. Let me get that right. 

The inventory at the end of period t is equal to the inventory at the start of period t plus the order quantity for period t minus the demand for period t. So, if I have inventory levels, maybe I should track the end-of-period inventory. Let me define variables for that. 

Let me think about the variables. Let's say for each period t (from 1 to T), we have:

- order[t]: the amount ordered in period t. This can be zero if no order is placed.
- inventory[t]: the inventory at the end of period t.

But since the initial inventory is given, inventory[0] is 19. Then, for each period t (starting from 1 to T), the inventory balance equation would be:

inventory[t] = inventory[t-1] + order[t] - demand[t]

But wait, the demand is for the period. So during period t, the demand is met by the inventory and the order. So the equation is correct.

The objective is to minimize the total cost, which is the sum over all periods of (order cost if order[t] > 0) plus holding cost multiplied by inventory[t]. Wait, but the holding cost is per unit held. So for each period, the holding cost is holding_cost * inventory[t]. But the order cost is unit_order_cost multiplied by the number of orders. Wait, the problem says "minimize order cost 4 and holding cost 1". So the order cost is 4 per order, not per unit. So if you order any quantity in a period, you pay 4. So the order cost is 4 * number of periods where order[t] > 0. Or is it 4 per unit ordered? Wait, the problem says "order cost 4" which is a bit ambiguous. But in typical inventory models, the order cost is a fixed cost per order, not per unit. So if you place an order in a period, regardless of the quantity, you pay 4. So the total order cost is sum over all periods of (4 if order[t] > 0 else 0). 

But the problem says "unit_order_cost": 4. So maybe it's per unit ordered. Wait, the problem says "Minimize order cost 4 and holding cost 1". So perhaps the order cost is 4 per unit ordered. Wait, but that would be different from standard models. Let me check the problem statement again. 

The problem says "Minimize order cost 4 and holding cost 1 using inventory-balance constraints." So the order cost is 4 per order, not per unit. Wait, but the parameters are given as unit_order_cost: 4. That might be a bit confusing. Wait, the parameters are:

"unit_order_cost": 4, "holding_cost": 1. So maybe the order cost is 4 per unit ordered. But that's not standard. Alternatively, maybe the order cost is a fixed cost per order, regardless of quantity. But the parameter is called unit_order_cost, which suggests per unit. Hmm. 

Wait, the problem says "order cost 4 and holding cost 1". So perhaps the order cost is 4 per order, and holding cost is 1 per unit. But the parameter is called unit_order_cost, which is confusing. Maybe the problem is using "unit_order_cost" as the cost per unit ordered. So the total order cost is sum over all periods of (unit_order_cost * order[t]). 

But that would make the order cost depend on the quantity ordered. However, in standard models, the order cost is a fixed cost per order, not per unit. But given the parameters, perhaps the problem expects that the order cost is 4 per unit ordered. Let me check the problem again. 

The problem says "Minimize order cost 4 and holding cost 1". So maybe the order cost is 4 per order (fixed cost), and holding cost is 1 per unit. But the parameter is called unit_order_cost. That's conflicting. 

Alternatively, maybe the problem is using "unit_order_cost" as the cost per unit ordered. So if you order 10 units, you pay 4 * 10. But that's not typical. However, given the parameters, I need to model it as per the problem's description. 

Wait, the problem says "unit_order_cost": 4. So perhaps the order cost is 4 per unit ordered. So the total order cost is sum over all periods of (unit_order_cost * order[t]). 

But then, the holding cost is 1 per unit held. So the total cost is sum (unit_order_cost * order[t]) + sum (holding_cost * inventory[t]). 

But let me check the problem statement again. The problem says "Minimize order cost 4 and holding cost 1". So the order cost is 4 per order, and holding cost is 1 per unit. But the parameter is called unit_order_cost. That's confusing. 

Alternatively, maybe the problem is using "unit_order_cost" as the cost per order, but that's not standard. 

Wait, perhaps the problem is using "unit_order_cost" as the cost per unit ordered. So the total order cost is sum (unit_order_cost * order[t]). 

But given that the problem says "order cost 4", maybe it's a fixed cost per order. So if you place an order in a period, you pay 4, regardless of the quantity. So the total order cost is sum (4 * (order[t] > 0)). 

But how to model that in PuLP? Because PuLP's objective function is linear. So if you have a binary variable indicating whether an order is placed in period t, then the cost would be 4 * binary_variable. But the problem doesn't mention binary variables. 

Alternatively, maybe the problem is using the unit_order_cost as the cost per unit ordered. So the total order cost is sum (unit_order_cost * order[t]). 

But given that the problem says "order cost 4", perhaps it's a fixed cost. However, the parameters are given as unit_order_cost: 4. So perhaps the problem expects that the order cost is 4 per unit ordered. 

But this is ambiguous. However, given that the problem says "unit_order_cost", I think the correct interpretation is that the order cost is 4 per unit ordered. So the total order cost is sum (unit_order_cost * order[t]). 

But then, the problem says "Minimize order cost 4 and holding cost 1". So the total cost is sum (order cost) + sum (holding cost). 

So the objective function is sum (4 * order[t]) + sum (1 * inventory[t]). 

But I need to confirm. Let me think of an example. Suppose in period 1, we order 10 units. Then the order cost is 4 * 10 = 40. If we order 0, then it's 0. 

But if the order cost is fixed per order, then even if you order 0, you don't pay. But if you order any positive quantity, you pay 4. 

But the problem's parameters are given as unit_order_cost: 4. So perhaps the problem expects that the order cost is per unit. 

But given that the problem says "order cost 4", maybe it's a fixed cost. However, the parameter is called unit_order_cost. 

This is a bit confusing. But given that the problem says "unit_order_cost": 4, I think the correct approach is to model the order cost as 4 per unit ordered. 

So the total cost is sum (4 * order[t]) + sum (1 * inventory[t]). 

But let me check the problem's example. Let's say the initial inventory is 19. 

For period 1, demand is 31. So the inventory at the end of period 1 is initial_inventory + order[1] - demand[1]. 

But if the initial inventory is 19, and demand is 31, then we need to order at least 31 - 19 = 12 units. 

But if we order 12, then the order cost is 4 * 12 = 48. The holding cost is 0 (since inventory after period 1 is 19 + 12 - 31 = 0). 

But if we order more, say 20, then the order cost is 4 * 20 = 80, and holding cost is 0. 

But the problem is
