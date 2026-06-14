\* fixed_order_cost_big_m *\
Minimize
total_cost: 2 I_0 + 2 I_1 + 2 I_2 + Q_0 + Q_1 + Q_2 + 43 Y_0 + 43 Y_1 + 43 Y_2
Subject To
big_m_0: Q_0 - 135 Y_0 <= 0
big_m_1: Q_1 - 135 Y_1 <= 0
big_m_2: Q_2 - 135 Y_2 <= 0
inventory_balance_0: I_0 - Q_0 = -46
inventory_balance_1: - I_0 + I_1 - Q_1 = -34
inventory_balance_2: - I_1 + I_2 - Q_2 = -50
Binaries
Y_0
Y_1
Y_2
End
