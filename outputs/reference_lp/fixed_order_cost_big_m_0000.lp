\* fixed_order_cost_big_m *\
Minimize
total_cost: I_0 + I_1 + I_2 + I_3 + I_4 + 3 Q_0 + 3 Q_1 + 3 Q_2 + 3 Q_3
 + 3 Q_4 + 74 Y_0 + 74 Y_1 + 74 Y_2 + 74 Y_3 + 74 Y_4
Subject To
big_m_0: Q_0 - 174 Y_0 <= 0
big_m_1: Q_1 - 174 Y_1 <= 0
big_m_2: Q_2 - 174 Y_2 <= 0
big_m_3: Q_3 - 174 Y_3 <= 0
big_m_4: Q_4 - 174 Y_4 <= 0
inventory_balance_0: I_0 - Q_0 = -44
inventory_balance_1: - I_0 + I_1 - Q_1 = -27
inventory_balance_2: - I_1 + I_2 - Q_2 = -60
inventory_balance_3: - I_2 + I_3 - Q_3 = -19
inventory_balance_4: - I_3 + I_4 - Q_4 = -17
Binaries
Y_0
Y_1
Y_2
Y_3
Y_4
End
