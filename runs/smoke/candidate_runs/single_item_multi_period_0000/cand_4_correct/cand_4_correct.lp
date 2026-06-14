\* single_item_multi_period *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + 2 I_3 + 2 I_4 + 2 I_5 + Q_0 + Q_1 + Q_2
 + Q_3 + Q_4 + Q_5
Subject To
inventory_balance_0: I_0 - Q_0 = -15
inventory_balance_1: - I_0 + I_1 - Q_1 = -20
inventory_balance_2: - I_1 + I_2 - Q_2 = -28
inventory_balance_3: - I_2 + I_3 - Q_3 = -29
inventory_balance_4: - I_3 + I_4 - Q_4 = -47
inventory_balance_5: - I_4 + I_5 - Q_5 = -53
End
