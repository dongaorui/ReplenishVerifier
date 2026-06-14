\* single_item_multi_period *\
Minimize
total_cost: 3 I_0 + 3 I_1 + 3 I_2 + 3 I_3 + 3 I_4 + 3 I_5 + 4 Q_0 + 4 Q_1
 + 4 Q_2 + 4 Q_3 + 4 Q_4 + 4 Q_5
Subject To
inventory_balance_0: I_0 - Q_0 = -36
inventory_balance_1: - I_0 + I_1 - Q_1 = -52
inventory_balance_2: - I_1 + I_2 - Q_2 = -32
inventory_balance_3: - I_2 + I_3 - Q_3 = -15
inventory_balance_4: - I_3 + I_4 - Q_4 = -25
inventory_balance_5: - I_4 + I_5 - Q_5 = -59
End
