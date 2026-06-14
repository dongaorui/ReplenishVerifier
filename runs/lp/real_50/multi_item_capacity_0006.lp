\* multi_item_capacity *\
Minimize
total_cost: 3 I_(0,_0) + 3 I_(0,_1) + 3 I_(0,_2) + 3 I_(1,_0) + 3 I_(1,_1)
 + 3 I_(1,_2) + 2 I_(2,_0) + 2 I_(2,_1) + 2 I_(2,_2) + 2 I_(3,_0) + 2 I_(3,_1)
 + 2 I_(3,_2) + 4 Q_(0,_0) + 4 Q_(0,_1) + 4 Q_(0,_2) + 2 Q_(1,_0) + 2 Q_(1,_1)
 + 2 Q_(1,_2) + 2 Q_(2,_0) + 2 Q_(2,_1) + 2 Q_(2,_2) + 4 Q_(3,_0) + 4 Q_(3,_1)
 + 4 Q_(3,_2)
Subject To
capacity_0: 2 I_(0,_0) + 3 I_(1,_0) + 4 I_(2,_0) + 2 I_(3,_0) <= 84
capacity_1: 2 I_(0,_1) + 3 I_(1,_1) + 4 I_(2,_1) + 2 I_(3,_1) <= 84
capacity_2: 2 I_(0,_2) + 3 I_(1,_2) + 4 I_(2,_2) + 2 I_(3,_2) <= 84
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -17
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -16
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -32
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -40
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -36
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -49
inventory_balance_2_0: I_(2,_0) - Q_(2,_0) = -16
inventory_balance_2_1: - I_(2,_0) + I_(2,_1) - Q_(2,_1) = -25
inventory_balance_2_2: - I_(2,_1) + I_(2,_2) - Q_(2,_2) = -20
inventory_balance_3_0: I_(3,_0) - Q_(3,_0) = -9
inventory_balance_3_1: - I_(3,_0) + I_(3,_1) - Q_(3,_1) = -36
inventory_balance_3_2: - I_(3,_1) + I_(3,_2) - Q_(3,_2) = -11
End
