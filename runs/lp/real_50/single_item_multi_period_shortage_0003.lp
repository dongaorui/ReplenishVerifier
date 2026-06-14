\* single_item_multi_period_shortage *\
Minimize
total_cost: 8 B_0 + 8 B_1 + 8 B_2 + 8 B_3 + 8 B_4 + 4 I_0 + 4 I_1 + 4 I_2
 + 4 I_3 + 4 I_4 + 3 Q_0 + 3 Q_1 + 3 Q_2 + 3 Q_3 + 3 Q_4
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -49
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -69
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -53
inventory_balance_3: B_2 - B_3 - I_2 + I_3 - Q_3 = -20
inventory_balance_4: B_3 - B_4 - I_3 + I_4 - Q_4 = -58
End
