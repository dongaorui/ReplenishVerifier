\* remove_big_m_constraint *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + 5 Q_0 + 5 Q_1 + 5 Q_2 + 29 Y_0 + 29 Y_1
 + 29 Y_2
Subject To
inventory_balance_0: I_0 - Q_0 = -39
inventory_balance_1: - I_0 + I_1 - Q_1 = -34
inventory_balance_2: - I_1 + I_2 - Q_2 = -55
Binaries
Y_0
Y_1
Y_2
End
