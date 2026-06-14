\* multi_item_capacity *\
Minimize
total_cost: I_(0,_0) + I_(0,_1) + I_(0,_2) + I_(0,_3) + 2 I_(1,_0)
 + 2 I_(1,_1) + 2 I_(1,_2) + 2 I_(1,_3) + 5 Q_(0,_0) + 5 Q_(0,_1) + 5 Q_(0,_2)
 + 5 Q_(0,_3) + 3 Q_(1,_0) + 3 Q_(1,_1) + 3 Q_(1,_2) + 3 Q_(1,_3)
Subject To
capacity_0: 4 I_(0,_0) + 2 I_(1,_0) <= 145
capacity_1: 4 I_(0,_1) + 2 I_(1,_1) <= 145
capacity_2: 4 I_(0,_2) + 2 I_(1,_2) <= 145
capacity_3: 4 I_(0,_3) + 2 I_(1,_3) <= 145
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -35
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -47
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -48
inventory_balance_0_3: - I_(0,_2) + I_(0,_3) - Q_(0,_3) = -30
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -30
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -38
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -38
inventory_balance_1_3: - I_(1,_2) + I_(1,_3) - Q_(1,_3) = -23
End
