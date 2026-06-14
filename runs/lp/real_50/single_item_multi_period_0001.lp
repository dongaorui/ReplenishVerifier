\* single_item_multi_period *\
Minimize
total_cost: I_0 + I_1 + I_2 + I_3 + I_4 + Q_0 + Q_1 + Q_2 + Q_3 + Q_4
Subject To
inventory_balance_0: I_0 - Q_0 = -29
inventory_balance_1: - I_0 + I_1 - Q_1 = -54
inventory_balance_2: - I_1 + I_2 - Q_2 = -38
inventory_balance_3: - I_2 + I_3 - Q_3 = -51
inventory_balance_4: - I_3 + I_4 - Q_4 = -27
End
