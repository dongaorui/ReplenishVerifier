\* single_item_multi_period *\
Minimize
total_cost: 3 I_0 + 3 I_1 + 3 I_2 + 3 I_3 + 3 I_4 + Q_0 + Q_1 + Q_2 + Q_3
 + Q_4
Subject To
inventory_balance_0: I_0 - Q_0 = -24
inventory_balance_1: - I_0 + I_1 - Q_1 = -36
inventory_balance_2: - I_1 + I_2 - Q_2 = -21
inventory_balance_3: - I_2 + I_3 - Q_3 = -20
inventory_balance_4: - I_3 + I_4 - Q_4 = -39
End
