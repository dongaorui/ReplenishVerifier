\* fixed_order_cost_big_m *\
Minimize
total_cost: 4 I_0 + 4 I_1 + 4 I_2 + 4 I_3 + 4 I_4 + 4 I_5 + 4 Q_0 + 4 Q_1
 + 4 Q_2 + 4 Q_3 + 4 Q_4 + 4 Q_5 + 77 Y_0 + 77 Y_1 + 77 Y_2 + 77 Y_3 + 77 Y_4
 + 77 Y_5
Subject To
big_m_0: Q_0 - 229 Y_0 <= 0
big_m_1: Q_1 - 229 Y_1 <= 0
big_m_2: Q_2 - 229 Y_2 <= 0
big_m_3: Q_3 - 229 Y_3 <= 0
big_m_4: Q_4 - 229 Y_4 <= 0
big_m_5: Q_5 - 229 Y_5 <= 0
inventory_balance_0: I_0 - Q_0 = -35
inventory_balance_1: - I_0 + I_1 - Q_1 = -36
inventory_balance_2: - I_1 + I_2 - Q_2 = -49
inventory_balance_3: - I_2 + I_3 - Q_3 = -44
inventory_balance_4: - I_3 + I_4 - Q_4 = -41
inventory_balance_5: - I_4 + I_5 - Q_5 = -18
Binaries
Y_0
Y_1
Y_2
Y_3
Y_4
Y_5
End
