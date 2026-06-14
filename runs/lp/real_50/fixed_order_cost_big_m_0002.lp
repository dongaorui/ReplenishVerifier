\* fixed_order_cost_big_m *\
Minimize
total_cost: 4 I_0 + 4 I_1 + 4 I_2 + 5 Q_0 + 5 Q_1 + 5 Q_2 + 23 Y_0 + 23 Y_1
 + 23 Y_2
Subject To
big_m_0: Q_0 - 92 Y_0 <= 0
big_m_1: Q_1 - 92 Y_1 <= 0
big_m_2: Q_2 - 92 Y_2 <= 0
inventory_balance_0: I_0 - Q_0 = -16
inventory_balance_1: - I_0 + I_1 - Q_1 = -42
inventory_balance_2: - I_1 + I_2 - Q_2 = -29
Binaries
Y_0
Y_1
Y_2
End
