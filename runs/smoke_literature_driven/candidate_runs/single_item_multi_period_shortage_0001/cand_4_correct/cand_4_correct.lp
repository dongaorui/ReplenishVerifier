\* single_item_multi_period_shortage *\
Minimize
total_cost: 18 B_0 + 18 B_1 + 18 B_2 + 18 B_3 + 18 B_4 + I_0 + I_1 + I_2 + I_3
 + I_4 + Q_0 + Q_1 + Q_2 + Q_3 + Q_4
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -39
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -43
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -56
inventory_balance_3: B_2 - B_3 - I_2 + I_3 - Q_3 = -32
inventory_balance_4: B_3 - B_4 - I_3 + I_4 - Q_4 = -65
End
