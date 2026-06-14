\* single_item_multi_period *\
Minimize
total_cost: 4 I_0 + 4 I_1 + 4 I_2 + 4 I_3 + 4 I_4 + 4 I_5 + 5 Q_0 + 5 Q_1
 + 5 Q_2 + 5 Q_3 + 5 Q_4 + 5 Q_5
Subject To
inventory_balance_0: I_0 - Q_0 = -27
inventory_balance_1: - I_0 + I_1 - Q_1 = -23
inventory_balance_2: - I_1 + I_2 - Q_2 = -30
inventory_balance_3: - I_2 + I_3 - Q_3 = -50
inventory_balance_4: - I_3 + I_4 - Q_4 = -49
inventory_balance_5: - I_4 + I_5 - Q_5 = -31
End
