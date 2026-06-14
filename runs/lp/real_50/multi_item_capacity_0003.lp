\* multi_item_capacity *\
Minimize
total_cost: 4 I_(0,_0) + 4 I_(0,_1) + 4 I_(0,_2) + I_(1,_0) + I_(1,_1)
 + I_(1,_2) + I_(2,_0) + I_(2,_1) + I_(2,_2) + 2 I_(3,_0) + 2 I_(3,_1)
 + 2 I_(3,_2) + 4 Q_(0,_0) + 4 Q_(0,_1) + 4 Q_(0,_2) + 3 Q_(1,_0) + 3 Q_(1,_1)
 + 3 Q_(1,_2) + Q_(2,_0) + Q_(2,_1) + Q_(2,_2) + Q_(3,_0) + Q_(3,_1)
 + Q_(3,_2)
Subject To
capacity_0: 3 I_(0,_0) + 3 I_(1,_0) + 2 I_(2,_0) + 3 I_(3,_0) <= 118
capacity_1: 3 I_(0,_1) + 3 I_(1,_1) + 2 I_(2,_1) + 3 I_(3,_1) <= 118
capacity_2: 3 I_(0,_2) + 3 I_(1,_2) + 2 I_(2,_2) + 3 I_(3,_2) <= 118
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -7
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -25
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -35
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -9
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -46
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -25
inventory_balance_2_0: I_(2,_0) - Q_(2,_0) = -35
inventory_balance_2_1: - I_(2,_0) + I_(2,_1) - Q_(2,_1) = -48
inventory_balance_2_2: - I_(2,_1) + I_(2,_2) - Q_(2,_2) = -12
inventory_balance_3_0: I_(3,_0) - Q_(3,_0) = -45
inventory_balance_3_1: - I_(3,_0) + I_(3,_1) - Q_(3,_1) = -15
inventory_balance_3_2: - I_(3,_1) + I_(3,_2) - Q_(3,_2) = -36
End
