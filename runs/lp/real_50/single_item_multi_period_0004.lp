\* single_item_multi_period *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + 2 I_3 + 3 Q_0 + 3 Q_1 + 3 Q_2 + 3 Q_3
Subject To
inventory_balance_0: I_0 - Q_0 = -13
inventory_balance_1: - I_0 + I_1 - Q_1 = -25
inventory_balance_2: - I_1 + I_2 - Q_2 = -44
inventory_balance_3: - I_2 + I_3 - Q_3 = -39
End
