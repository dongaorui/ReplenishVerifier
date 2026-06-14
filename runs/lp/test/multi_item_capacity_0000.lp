\* multi_item_capacity *\
Minimize
total_cost: 3 I_(0,_0) + 3 I_(0,_1) + 3 I_(0,_2) + 3 I_(0,_3) + I_(1,_0)
 + I_(1,_1) + I_(1,_2) + I_(1,_3) + 5 Q_(0,_0) + 5 Q_(0,_1) + 5 Q_(0,_2)
 + 5 Q_(0,_3) + 2 Q_(1,_0) + 2 Q_(1,_1) + 2 Q_(1,_2) + 2 Q_(1,_3)
Subject To
capacity_0: 2 I_(0,_0) + 2 I_(1,_0) <= 114
capacity_1: 2 I_(0,_1) + 2 I_(1,_1) <= 114
capacity_2: 2 I_(0,_2) + 2 I_(1,_2) <= 114
capacity_3: 2 I_(0,_3) + 2 I_(1,_3) <= 114
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -19
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -32
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -23
inventory_balance_0_3: - I_(0,_2) + I_(0,_3) - Q_(0,_3) = -27
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -2
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -48
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -50
inventory_balance_1_3: - I_(1,_2) + I_(1,_3) - Q_(1,_3) = -20
End
