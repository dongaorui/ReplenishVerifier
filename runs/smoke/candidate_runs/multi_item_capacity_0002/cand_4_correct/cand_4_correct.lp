\* multi_item_capacity *\
Minimize
total_cost: 3 I_(0,_0) + 3 I_(0,_1) + 3 I_(0,_2) + I_(1,_0) + I_(1,_1)
 + I_(1,_2) + I_(2,_0) + I_(2,_1) + I_(2,_2) + 3 I_(3,_0) + 3 I_(3,_1)
 + 3 I_(3,_2) + 4 Q_(0,_0) + 4 Q_(0,_1) + 4 Q_(0,_2) + 4 Q_(1,_0) + 4 Q_(1,_1)
 + 4 Q_(1,_2) + 5 Q_(2,_0) + 5 Q_(2,_1) + 5 Q_(2,_2) + 4 Q_(3,_0) + 4 Q_(3,_1)
 + 4 Q_(3,_2)
Subject To
capacity_0: I_(0,_0) + I_(1,_0) + I_(2,_0) + 2 I_(3,_0) <= 88
capacity_1: I_(0,_1) + I_(1,_1) + I_(2,_1) + 2 I_(3,_1) <= 88
capacity_2: I_(0,_2) + I_(1,_2) + I_(2,_2) + 2 I_(3,_2) <= 88
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -25
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -44
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -26
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -42
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -37
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -47
inventory_balance_2_0: I_(2,_0) - Q_(2,_0) = -22
inventory_balance_2_1: - I_(2,_0) + I_(2,_1) - Q_(2,_1) = -33
inventory_balance_2_2: - I_(2,_1) + I_(2,_2) - Q_(2,_2) = -24
inventory_balance_3_0: I_(3,_0) - Q_(3,_0) = 1
inventory_balance_3_1: - I_(3,_0) + I_(3,_1) - Q_(3,_1) = -42
inventory_balance_3_2: - I_(3,_1) + I_(3,_2) - Q_(3,_2) = -41
End
