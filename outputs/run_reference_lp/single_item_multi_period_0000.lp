\* single_item_multi_period *\
Minimize
total_cost: I_0 + I_1 + I_2 + 5 Q_0 + 5 Q_1 + 5 Q_2
Subject To
inventory_balance_0: I_0 - Q_0 = -47
inventory_balance_1: - I_0 + I_1 - Q_1 = -21
inventory_balance_2: - I_1 + I_2 - Q_2 = -38
End
