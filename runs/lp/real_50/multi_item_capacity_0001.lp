\* multi_item_capacity *\
Minimize
total_cost: I_(0,_0) + I_(0,_1) + I_(0,_2) + I_(1,_0) + I_(1,_1) + I_(1,_2)
 + 4 Q_(0,_0) + 4 Q_(0,_1) + 4 Q_(0,_2) + 5 Q_(1,_0) + 5 Q_(1,_1) + 5 Q_(1,_2)
Subject To
capacity_0: 2 I_(0,_0) + 3 I_(1,_0) <= 89
capacity_1: 2 I_(0,_1) + 3 I_(1,_1) <= 89
capacity_2: 2 I_(0,_2) + 3 I_(1,_2) <= 89
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -8
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -22
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -44
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -31
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -18
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -37
End
