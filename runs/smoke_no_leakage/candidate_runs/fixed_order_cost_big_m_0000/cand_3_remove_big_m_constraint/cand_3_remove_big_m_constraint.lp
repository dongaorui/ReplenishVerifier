\* remove_big_m_constraint *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + 2 I_3 + 2 I_4 + 3 Q_0 + 3 Q_1 + 3 Q_2
 + 3 Q_3 + 3 Q_4 + 52 Y_0 + 52 Y_1 + 52 Y_2 + 52 Y_3 + 52 Y_4
Subject To
inventory_balance_0: I_0 - Q_0 = -22
inventory_balance_1: - I_0 + I_1 - Q_1 = -33
inventory_balance_2: - I_1 + I_2 - Q_2 = -42
inventory_balance_3: - I_2 + I_3 - Q_3 = -25
inventory_balance_4: - I_3 + I_4 - Q_4 = -44
Binaries
Y_0
Y_1
Y_2
Y_3
Y_4
End
