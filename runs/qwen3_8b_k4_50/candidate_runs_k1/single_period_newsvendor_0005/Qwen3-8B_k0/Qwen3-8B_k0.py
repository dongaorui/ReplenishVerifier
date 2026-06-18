import pulp
import os

def build_model():
    prob = pulp.LpProblem("Single_Period_Newsvendor", pulp.LpMinimize)
    demand = 55
    unit_order_cost = 5
    holding_cost = 4
    shortage_cost = 8
