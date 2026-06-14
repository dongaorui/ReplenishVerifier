\* single_item_multi_period *\
Minimize
total_cost: I_0 + I_1 + I_2 + I_3 + I_4 + I_5 + 3 Q_0 + 3 Q_1 + 3 Q_2 + 3 Q_3
 + 3 Q_4 + 3 Q_5
Subject To
inventory_balance_0: I_0 - Q_0 = -18
inventory_balance_1: - I_0 + I_1 - Q_1 = -25
inventory_balance_2: - I_1 + I_2 - Q_2 = -38
inventory_balance_3: - I_2 + I_3 - Q_3 = -37
inventory_balance_4: - I_3 + I_4 - Q_4 = -28
inventory_balance_5: - I_4 + I_5 - Q_5 = -57
End
