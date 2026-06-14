\* single_item_multi_period *\
Minimize
total_cost: 3 I_0 + 3 I_1 + 3 I_2 + 3 I_3 + 4 Q_0 + 4 Q_1 + 4 Q_2 + 4 Q_3
Subject To
inventory_balance_0: I_0 - Q_0 = -9
inventory_balance_1: - I_0 + I_1 - Q_1 = -20
inventory_balance_2: - I_1 + I_2 - Q_2 = -29
inventory_balance_3: - I_2 + I_3 - Q_3 = -21
End
