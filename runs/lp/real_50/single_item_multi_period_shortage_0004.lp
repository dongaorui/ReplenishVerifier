\* single_item_multi_period_shortage *\
Minimize
total_cost: 9 B_0 + 9 B_1 + 9 B_2 + I_0 + I_1 + I_2 + 2 Q_0 + 2 Q_1 + 2 Q_2
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -28
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -35
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -23
End
