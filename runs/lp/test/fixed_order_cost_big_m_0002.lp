\* fixed_order_cost_big_m *\
Minimize
total_cost: I_0 + I_1 + I_2 + I_3 + I_4 + 4 Q_0 + 4 Q_1 + 4 Q_2 + 4 Q_3
 + 4 Q_4 + 27 Y_0 + 27 Y_1 + 27 Y_2 + 27 Y_3 + 27 Y_4
Subject To
big_m_0: Q_0 - 190 Y_0 <= 0
big_m_1: Q_1 - 190 Y_1 <= 0
big_m_2: Q_2 - 190 Y_2 <= 0
big_m_3: Q_3 - 190 Y_3 <= 0
big_m_4: Q_4 - 190 Y_4 <= 0
inventory_balance_0: I_0 - Q_0 = -15
inventory_balance_1: - I_0 + I_1 - Q_1 = -49
inventory_balance_2: - I_1 + I_2 - Q_2 = -48
inventory_balance_3: - I_2 + I_3 - Q_3 = -15
inventory_balance_4: - I_3 + I_4 - Q_4 = -53
Binaries
Y_0
Y_1
Y_2
Y_3
Y_4
End
