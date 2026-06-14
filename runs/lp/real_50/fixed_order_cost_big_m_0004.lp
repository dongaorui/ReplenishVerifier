\* fixed_order_cost_big_m *\
Minimize
total_cost: 3 I_0 + 3 I_1 + 3 I_2 + 3 I_3 + 3 I_4 + 3 I_5 + 4 Q_0 + 4 Q_1
 + 4 Q_2 + 4 Q_3 + 4 Q_4 + 4 Q_5 + 68 Y_0 + 68 Y_1 + 68 Y_2 + 68 Y_3 + 68 Y_4
 + 68 Y_5
Subject To
big_m_0: Q_0 - 261 Y_0 <= 0
big_m_1: Q_1 - 261 Y_1 <= 0
big_m_2: Q_2 - 261 Y_2 <= 0
big_m_3: Q_3 - 261 Y_3 <= 0
big_m_4: Q_4 - 261 Y_4 <= 0
big_m_5: Q_5 - 261 Y_5 <= 0
inventory_balance_0: I_0 - Q_0 = -39
inventory_balance_1: - I_0 + I_1 - Q_1 = -47
inventory_balance_2: - I_1 + I_2 - Q_2 = -42
inventory_balance_3: - I_2 + I_3 - Q_3 = -50
inventory_balance_4: - I_3 + I_4 - Q_4 = -43
inventory_balance_5: - I_4 + I_5 - Q_5 = -25
Binaries
Y_0
Y_1
Y_2
Y_3
Y_4
Y_5
End
