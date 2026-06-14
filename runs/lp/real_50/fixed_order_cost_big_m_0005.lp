\* fixed_order_cost_big_m *\
Minimize
total_cost: 3 I_0 + 3 I_1 + 3 I_2 + 3 I_3 + 2 Q_0 + 2 Q_1 + 2 Q_2 + 2 Q_3
 + 48 Y_0 + 48 Y_1 + 48 Y_2 + 48 Y_3
Subject To
big_m_0: Q_0 - 181 Y_0 <= 0
big_m_1: Q_1 - 181 Y_1 <= 0
big_m_2: Q_2 - 181 Y_2 <= 0
big_m_3: Q_3 - 181 Y_3 <= 0
inventory_balance_0: I_0 - Q_0 = -35
inventory_balance_1: - I_0 + I_1 - Q_1 = -32
inventory_balance_2: - I_1 + I_2 - Q_2 = -48
inventory_balance_3: - I_2 + I_3 - Q_3 = -46
Binaries
Y_0
Y_1
Y_2
Y_3
End
