# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 16:20:09 2021

@author: beatr
"""
import gurobipy as gp
from gurobipy import GRB

P = [1, 2]
S = [1, 2]
I = [1, 2, 3]
C = [5, 6, 8, 7, 4, 9]

# Create a new model
m = gp.Model("TrafficAndDemand")

# Create variables
x_vars = {}
for p in range(len(P)):
    for i in range(len(I)):
        x_vars[i,p] = m.addVar(vtype=GRB.BINARY,
                               name="number_amb_"+str(i)+str(p))

y_vars = {}
for p in range(len(P)):
    for s in range(len(S)):
        for i in range(len(I)):
            for c in range(len(C)):
                y_vars[s,i,p,c] = m.addVar(vtype=GRB.BINARY, 
                         name="dispatched_"+str(s)+"_"+str(p)+str(i)+str(c))
                
zc_vars = {}
for s in range(len(S)):
    for c in range(len(C)):
        zc_vars[s,c] = m.addVar(vtype=GRB.BINARY,
                                name="covered_"+str(s)+str(c))

zac_vars = {}
for s in range(len(S)):
    for c in range(len(C)):
        zac_vars[s,c] = m.addVar(vtype=GRB.BINARY,
                                 name="ALS_"+str(s)+str(c))

zbc_vars = {}
for s in range(len(S)):
    for c in range(len(C)):
        zbc_vars[s,c] = m.addVar(vtype=GRB.BINARY,
                                 name="BLS_"+str(s)+str(c))

v_vars = {}
for s in range(len(S)):
    for c in range(len(C)):
        v_vars[s,c] = m.addVar(vtype=GRB.BINARY,
                                 name="no_dispatched_"+str(s)+str(c))

