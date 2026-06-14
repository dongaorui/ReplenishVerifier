\* single_item_multi_period *\
Minimize
total_cost: 4 I_0 + 4 I_1 + 4 I_2 + 4 I_3 + 4 Q_0 + 4 Q_1 + 4 Q_2 + 4 Q_3
Subject To
inventory_balance_0: I_0 - Q_0 = -33
inventory_balance_1: - I_0 + I_1 - Q_1 = -42
inventory_balance_2: - I_1 + I_2 - Q_2 = -53
inventory_balance_3: - I_2 + I_3 - Q_3 = -19
End
