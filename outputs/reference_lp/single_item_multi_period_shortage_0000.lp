\* single_item_multi_period_shortage *\
Minimize
total_cost: 16 B_0 + 16 B_1 + 16 B_2 + I_0 + I_1 + I_2 + 5 Q_0 + 5 Q_1 + 5 Q_2
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -25
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -33
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -34
End
