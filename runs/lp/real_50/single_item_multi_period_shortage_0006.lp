\* single_item_multi_period_shortage *\
Minimize
total_cost: 18 B_0 + 18 B_1 + 18 B_2 + 18 B_3 + 18 B_4 + 18 B_5 + 4 I_0
 + 4 I_1 + 4 I_2 + 4 I_3 + 4 I_4 + 4 I_5 + 3 Q_0 + 3 Q_1 + 3 Q_2 + 3 Q_3
 + 3 Q_4 + 3 Q_5
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -48
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -68
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -66
inventory_balance_3: B_2 - B_3 - I_2 + I_3 - Q_3 = -64
inventory_balance_4: B_3 - B_4 - I_3 + I_4 - Q_4 = -32
inventory_balance_5: B_4 - B_5 - I_4 + I_5 - Q_5 = -65
End
