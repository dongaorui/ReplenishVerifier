\* fixed_order_cost_big_m *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + 2 I_3 + 2 I_4 + 2 I_5 + 4 Q_0 + 4 Q_1
 + 4 Q_2 + 4 Q_3 + 4 Q_4 + 4 Q_5 + 29 Y_0 + 29 Y_1 + 29 Y_2 + 29 Y_3 + 29 Y_4
 + 29 Y_5
Subject To
big_m_0: Q_0 - 291 Y_0 <= 0
big_m_1: Q_1 - 291 Y_1 <= 0
big_m_2: Q_2 - 291 Y_2 <= 0
big_m_3: Q_3 - 291 Y_3 <= 0
big_m_4: Q_4 - 291 Y_4 <= 0
big_m_5: Q_5 - 291 Y_5 <= 0
inventory_balance_0: I_0 - Q_0 = -40
inventory_balance_1: - I_0 + I_1 - Q_1 = -51
inventory_balance_2: - I_1 + I_2 - Q_2 = -27
inventory_balance_3: - I_2 + I_3 - Q_3 = -60
inventory_balance_4: - I_3 + I_4 - Q_4 = -59
inventory_balance_5: - I_4 + I_5 - Q_5 = -39
Binaries
Y_0
Y_1
Y_2
Y_3
Y_4
Y_5
End
