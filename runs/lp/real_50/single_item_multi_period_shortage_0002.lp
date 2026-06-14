\* single_item_multi_period_shortage *\
Minimize
total_cost: 10 B_0 + 10 B_1 + 10 B_2 + 2 I_0 + 2 I_1 + 2 I_2 + 5 Q_0 + 5 Q_1
 + 5 Q_2
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -19
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -60
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -52
End
