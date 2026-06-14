\* multi_item_capacity *\
Minimize
total_cost: 3 I_(0,_0) + 3 I_(0,_1) + 3 I_(0,_2) + 3 I_(0,_3) + 3 I_(0,_4)
 + 3 I_(1,_0) + 3 I_(1,_1) + 3 I_(1,_2) + 3 I_(1,_3) + 3 I_(1,_4) + I_(2,_0)
 + I_(2,_1) + I_(2,_2) + I_(2,_3) + I_(2,_4) + 3 I_(3,_0) + 3 I_(3,_1)
 + 3 I_(3,_2) + 3 I_(3,_3) + 3 I_(3,_4) + 2 Q_(0,_0) + 2 Q_(0,_1) + 2 Q_(0,_2)
 + 2 Q_(0,_3) + 2 Q_(0,_4) + 4 Q_(1,_0) + 4 Q_(1,_1) + 4 Q_(1,_2) + 4 Q_(1,_3)
 + 4 Q_(1,_4) + 2 Q_(2,_0) + 2 Q_(2,_1) + 2 Q_(2,_2) + 2 Q_(2,_3) + 2 Q_(2,_4)
 + Q_(3,_0) + Q_(3,_1) + Q_(3,_2) + Q_(3,_3) + Q_(3,_4)
Subject To
capacity_0: I_(0,_0) + I_(1,_0) + I_(2,_0) + 2 I_(3,_0) <= 150
capacity_1: I_(0,_1) + I_(1,_1) + I_(2,_1) + 2 I_(3,_1) <= 150
capacity_2: I_(0,_2) + I_(1,_2) + I_(2,_2) + 2 I_(3,_2) <= 150
capacity_3: I_(0,_3) + I_(1,_3) + I_(2,_3) + 2 I_(3,_3) <= 150
capacity_4: I_(0,_4) + I_(1,_4) + I_(2,_4) + 2 I_(3,_4) <= 150
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -9
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -42
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -41
inventory_balance_0_3: - I_(0,_2) + I_(0,_3) - Q_(0,_3) = -26
inventory_balance_0_4: - I_(0,_3) + I_(0,_4) - Q_(0,_4) = -13
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -14
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -50
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -37
inventory_balance_1_3: - I_(1,_2) + I_(1,_3) - Q_(1,_3) = -27
inventory_balance_1_4: - I_(1,_3) + I_(1,_4) - Q_(1,_4) = -12
inventory_balance_2_0: I_(2,_0) - Q_(2,_0) = 1
inventory_balance_2_1: - I_(2,_0) + I_(2,_1) - Q_(2,_1) = -31
inventory_balance_2_2: - I_(2,_1) + I_(2,_2) - Q_(2,_2) = -18
inventory_balance_2_3: - I_(2,_2) + I_(2,_3) - Q_(2,_3) = -50
inventory_balance_2_4: - I_(2,_3) + I_(2,_4) - Q_(2,_4) = -26
inventory_balance_3_0: I_(3,_0) - Q_(3,_0) = -2
inventory_balance_3_1: - I_(3,_0) + I_(3,_1) - Q_(3,_1) = -38
inventory_balance_3_2: - I_(3,_1) + I_(3,_2) - Q_(3,_2) = -45
inventory_balance_3_3: - I_(3,_2) + I_(3,_3) - Q_(3,_3) = -37
inventory_balance_3_4: - I_(3,_3) + I_(3,_4) - Q_(3,_4) = -45
End
