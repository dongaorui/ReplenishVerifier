\* multi_item_capacity *\
Minimize
total_cost: 2 I_(0,_0) + 2 I_(0,_1) + 2 I_(0,_2) + 2 I_(0,_3) + 2 I_(0,_4)
 + 3 I_(1,_0) + 3 I_(1,_1) + 3 I_(1,_2) + 3 I_(1,_3) + 3 I_(1,_4) + 2 I_(2,_0)
 + 2 I_(2,_1) + 2 I_(2,_2) + 2 I_(2,_3) + 2 I_(2,_4) + 3 Q_(0,_0) + 3 Q_(0,_1)
 + 3 Q_(0,_2) + 3 Q_(0,_3) + 3 Q_(0,_4) + 3 Q_(1,_0) + 3 Q_(1,_1) + 3 Q_(1,_2)
 + 3 Q_(1,_3) + 3 Q_(1,_4) + 5 Q_(2,_0) + 5 Q_(2,_1) + 5 Q_(2,_2) + 5 Q_(2,_3)
 + 5 Q_(2,_4)
Subject To
capacity_0: I_(0,_0) + 2 I_(1,_0) + 3 I_(2,_0) <= 99
capacity_1: I_(0,_1) + 2 I_(1,_1) + 3 I_(2,_1) <= 99
capacity_2: I_(0,_2) + 2 I_(1,_2) + 3 I_(2,_2) <= 99
capacity_3: I_(0,_3) + 2 I_(1,_3) + 3 I_(2,_3) <= 99
capacity_4: I_(0,_4) + 2 I_(1,_4) + 3 I_(2,_4) <= 99
inventory_balance_0_0: I_(0,_0) - Q_(0,_0) = -15
inventory_balance_0_1: - I_(0,_0) + I_(0,_1) - Q_(0,_1) = -32
inventory_balance_0_2: - I_(0,_1) + I_(0,_2) - Q_(0,_2) = -14
inventory_balance_0_3: - I_(0,_2) + I_(0,_3) - Q_(0,_3) = -25
inventory_balance_0_4: - I_(0,_3) + I_(0,_4) - Q_(0,_4) = -33
inventory_balance_1_0: I_(1,_0) - Q_(1,_0) = -25
inventory_balance_1_1: - I_(1,_0) + I_(1,_1) - Q_(1,_1) = -20
inventory_balance_1_2: - I_(1,_1) + I_(1,_2) - Q_(1,_2) = -38
inventory_balance_1_3: - I_(1,_2) + I_(1,_3) - Q_(1,_3) = -44
inventory_balance_1_4: - I_(1,_3) + I_(1,_4) - Q_(1,_4) = -29
inventory_balance_2_0: I_(2,_0) - Q_(2,_0) = -32
inventory_balance_2_1: - I_(2,_0) + I_(2,_1) - Q_(2,_1) = -43
inventory_balance_2_2: - I_(2,_1) + I_(2,_2) - Q_(2,_2) = -10
inventory_balance_2_3: - I_(2,_2) + I_(2,_3) - Q_(2,_3) = -45
inventory_balance_2_4: - I_(2,_3) + I_(2,_4) - Q_(2,_4) = -29
End
