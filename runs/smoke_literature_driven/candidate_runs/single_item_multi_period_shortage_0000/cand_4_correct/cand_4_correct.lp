\* single_item_multi_period_shortage *\
Minimize
total_cost: 9 B_0 + 9 B_1 + 9 B_2 + 9 B_3 + 9 B_4 + 4 I_0 + 4 I_1 + 4 I_2
 + 4 I_3 + 4 I_4 + Q_0 + Q_1 + Q_2 + Q_3 + Q_4
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -17
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -22
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -66
inventory_balance_3: B_2 - B_3 - I_2 + I_3 - Q_3 = -49
inventory_balance_4: B_3 - B_4 - I_3 + I_4 - Q_4 = -54
End
