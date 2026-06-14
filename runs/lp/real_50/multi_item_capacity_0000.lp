\* multi_item_capacity *\
Minimize
total_cost: 4 I_(0,_0) + 4 I_(0,_1) + 4 I_(0,_2) + 4 I_(0,_3) + 4 I_(0,_4)
 + 3 I_(1,_0) + 3 I_(1,_1) + 3 I_(1,_2) + 3 I_(1,_3) + 3 I_(1,_4) + Q_(0,_0)
 + Q_(0,_1) + Q_(0,_2) + Q_(0,_3) + Q_(0,_4) + Q_(1,_0) + Q_(1,_1) + Q_(1,_2)
 + Q_(1,_3) + Q_(1,_4)
Subject To
capacity_0: 3 I_(0,_0) + 4 I_(1,_0) <= 86
capacity_1: 3 I_(0,_1) + 4 I_(1,_1) <= 86
capacity_2: 3 I_(0,_2) + 4 I_(1,_2) <= 86
capacity_3: 3 I_(0,_3) + 4 I_(1,_3) <= 86
capacity_4: 3 I_(0,_4) + 4 I_(1,_4) <= 86
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -33
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -46
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -40
inventory_balance_0_3: - I_(0,_2) + I_(0,_3) - Q_(0,_3) = -25
inventory_balance_0_4: - I_(0,_3) + I_(0,_4) - Q_(0,_4) = -40
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -22
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -22
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -16
inventory_balance_1_3: - I_(1,_2) + I_(1,_3) - Q_(1,_3) = -16
inventory_balance_1_4: - I_(1,_3) + I_(1,_4) - Q_(1,_4) = -37
End
