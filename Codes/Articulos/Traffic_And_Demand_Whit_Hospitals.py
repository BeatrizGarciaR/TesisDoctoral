# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 19:41:56 2021

@author: beatriz
"""

import gurobipy as gp
from gurobipy import GRB


S = [1, 2]
L = [1, 2, 3, 4]
P = [1, 2, 3, 4, 5, 6, 7, 8]
K = [1, 2]
H = [1,2,3,4,5]

rslp = [[[7, 10, 12, 8, 14, 20, 7, 10],
        [12, 9, 11, 10, 17, 8, 9, 10],
        [13, 7, 10, 9, 22, 15, 10, 15],
        [10, 15, 8, 12, 9, 10, 16, 17]],
        [[13, 7, 10, 9, 22, 15, 10, 15],
        [10, 15, 8, 12, 9, 10, 16, 17],
        [7, 10, 12, 8, 14, 20, 7, 10],
        [12, 9, 11, 10, 17, 8, 9, 10]]]

rsph = [[[12, 10, 15, 20, 18],
          [8, 22, 11, 13, 19],
          [15, 7, 10, 21, 11],
          [21, 16, 9, 8, 11],
          [9, 11, 15, 9, 10],
          [13, 12, 11, 10, 9],
          [8, 9, 10, 11, 12],
          [7, 6, 8, 9, 11]],
        [[13, 11, 10, 9, 8],
          [12, 7, 10, 15, 14],
          [20, 21, 15, 16, 8],
          [14, 9, 8, 15, 16],
          [12, 23, 17, 14, 13],
          [15, 16, 15, 14, 13],
          [10, 11, 12, 13, 14],
          [15, 14, 13, 12, 11]]]

f = [
     [[[13, 5, 6, 42, 9, 0, 15, 3],
       [2, 16, 3, 25, 10, 30, 14, 9],
       [21, 6, 19, 23, 7, 10, 8, 15],
       [9, 8, 7, 6, 10, 11, 12, 13]],
      [[31, 7, 15, 4, 17, 20, 10, 6],
       [6, 5, 12, 22, 0, 23, 18, 11],
       [14, 16, 29, 20, 17, 31, 18, 5],
       [9, 10, 6, 6, 15, 12, 12, 18]]],
     [[[1, 5, 6, 40, 9, 10, 16, 13],
       [21, 6, 33, 5, 12, 3, 4, 19],
       [21, 6, 19, 23, 7, 10, 8, 15],
       [9, 18, 17, 6, 13, 10, 12, 3]],
      [[1, 35, 6, 10, 19, 30, 13, 13],
       [22, 15, 3, 25, 10, 3, 14, 19],
       [21, 6, 19, 23, 7, 10, 8, 15],
       [9, 8, 10, 16, 10, 11, 22, 13]]]
     ]


esp = [[5, 3, 2, 7, 8, 9, 5, 4],
       [3, 6, 5, 4, 6, 7, 8, 6]]

csh = [[9, 8, 7, 3, 11],
       [12, 3, 6, 9, 11]]

Mr = 10
Ml = 4
Mh = 16


# Create a new model
m = gp.Model("TrafficAndDemand")

# Create variables
x_vars = {}
for l in range(len(L)):
    x_vars[l] = m.addVar(vtype=GRB.BINARY, 
                         name="located_"+str(l))

y_vars = {}
for s in range(len(S)):
    for l in range(len(L)):
        for p in range(len(P)):
            for h in range(len(H)):
                y_vars[s,l,p,h] = m.addVar(vtype=GRB.BINARY, 
                                     name="served_"+str(s)+str(l)+str(p)+str(h))


# Set objective
m.setObjective(gp.quicksum(y_vars[s,l,p,h]*esp[s][p]*f[k][s][l][p]
                    for k in range(len(K))
                    for s in range(len(S))
                    for l in range(len(L))
                    for p in range(len(P))
                    for h in range(len(H))
                    ), 
                GRB.MAXIMIZE)

# Add constraints
for s in range(len(S)):
    for p in range(len(P)):
        m.addConstr(gp.quicksum(y_vars[s,l,p,h]*rslp[s][l][p] 
                                for l in range(len(L))
                                for h in range(len(H))) <= Mr, "c0")

for s in range(len(S)):
    for p in range(len(P)):
        m.addConstr(gp.quicksum(y_vars[s,l,p,h]
                for l in range(len(L))
                for h in range(len(H))) <= 1 , "c1")

for s in range(len(S)):
    for p in range(len(P)):
        for l in range(len(L)): 
            for h in range(len(H)):
                m.addConstr(y_vars[s,l,p,h] <= x_vars[l], "c2")
            
            
m.addConstr(gp.quicksum(x_vars[l] for l in range(len(L))) <= Ml, "c3")


# New constraints

for s in range(len(S)):
    for l in range(len(L)):
        for p in range(len(P)):
            for h in range(len(H)):
                m.addConstr(y_vars[s,l,p,h]*rsph[s][p][h]  <= Mh, "c4")

                   

for s in range(len(S)):
    for h in range(len(H)):
        m.addConstr(gp.quicksum(y_vars[s,l,p,h]*esp[s][p] 
                                for p in range(len(P))
                                for l in range(len(L))) <= csh[s][h], "c5")


# Optimize model
m.optimize()

#imprimir variables 
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
    
#imprimir el valor objetivo
print('Obj: %g' % m.objVal)
print("Finished")
print(" ")

