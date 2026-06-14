\* fixed_order_cost_big_m *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + 5 Q_0 + 5 Q_1 + 5 Q_2 + 29 Y_0 + 29 Y_1
 + 29 Y_2
Subject To
big_m_0: Q_0 - 144 Y_0 <= 0
big_m_1: Q_1 - 144 Y_1 <= 0
big_m_2: Q_2 - 144 Y_2 <= 0
inventory_balance_0: I_0 - Q_0 = -39
inventory_balance_1: - I_0 + I_1 - Q_1 = -34
inventory_balance_2: - I_1 + I_2 - Q_2 = -55
Binaries
Y_0
Y_1
Y_2
End
