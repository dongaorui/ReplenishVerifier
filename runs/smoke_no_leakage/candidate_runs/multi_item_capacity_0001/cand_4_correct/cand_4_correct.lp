\* multi_item_capacity *\
Minimize
total_cost: 3 I_(0,_0) + 3 I_(0,_1) + 3 I_(0,_2) + 2 I_(1,_0) + 2 I_(1,_1)
 + 2 I_(1,_2) + 4 Q_(0,_0) + 4 Q_(0,_1) + 4 Q_(0,_2) + 2 Q_(1,_0) + 2 Q_(1,_1)
 + 2 Q_(1,_2)
Subject To
capacity_0: 3 I_(0,_0) + 2 I_(1,_0) <= 130
capacity_1: 3 I_(0,_1) + 2 I_(1,_1) <= 130
capacity_2: 3 I_(0,_2) + 2 I_(1,_2) <= 130
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -10
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -35
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -27
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = 1
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -23
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -46
End
