\* fixed_order_cost_big_m *\
Minimize
total_cost: 3 I_0 + 3 I_1 + 3 I_2 + 3 I_3 + 5 Q_0 + 5 Q_1 + 5 Q_2 + 5 Q_3
 + 80 Y_0 + 80 Y_1 + 80 Y_2 + 80 Y_3
Subject To
big_m_0: Q_0 - 133 Y_0 <= 0
big_m_1: Q_1 - 133 Y_1 <= 0
big_m_2: Q_2 - 133 Y_2 <= 0
big_m_3: Q_3 - 133 Y_3 <= 0
inventory_balance_0: I_0 - Q_0 = -6
inventory_balance_1: - I_0 + I_1 - Q_1 = -44
inventory_balance_2: - I_1 + I_2 - Q_2 = -23
inventory_balance_3: - I_2 + I_3 - Q_3 = -44
Binaries
Y_0
Y_1
Y_2
Y_3
End
