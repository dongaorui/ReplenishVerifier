\* single_item_multi_period_shortage *\
Minimize
total_cost: 16 B_0 + 16 B_1 + 16 B_2 + 16 B_3 + 16 B_4 + 2 I_0 + 2 I_1 + 2 I_2
 + 2 I_3 + 2 I_4 + 3 Q_0 + 3 Q_1 + 3 Q_2 + 3 Q_3 + 3 Q_4
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -35
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -47
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -30
inventory_balance_3: B_2 - B_3 - I_2 + I_3 - Q_3 = -49
inventory_balance_4: B_3 - B_4 - I_3 + I_4 - Q_4 = -20
End
