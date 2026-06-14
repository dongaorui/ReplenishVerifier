\* single_item_multi_period_shortage *\
Minimize
total_cost: 20 B_0 + 20 B_1 + 20 B_2 + 20 B_3 + 20 B_4 + 20 B_5 + 3 I_0
 + 3 I_1 + 3 I_2 + 3 I_3 + 3 I_4 + 3 I_5 + 5 Q_0 + 5 Q_1 + 5 Q_2 + 5 Q_3
 + 5 Q_4 + 5 Q_5
Subject To
inventory_balance_0: - B_0 + I_0 - Q_0 = -20
inventory_balance_1: B_0 - B_1 - I_0 + I_1 - Q_1 = -55
inventory_balance_2: B_1 - B_2 - I_1 + I_2 - Q_2 = -20
inventory_balance_3: B_2 - B_3 - I_2 + I_3 - Q_3 = -63
inventory_balance_4: B_3 - B_4 - I_3 + I_4 - Q_4 = -66
inventory_balance_5: B_4 - B_5 - I_4 + I_5 - Q_5 = -27
End
