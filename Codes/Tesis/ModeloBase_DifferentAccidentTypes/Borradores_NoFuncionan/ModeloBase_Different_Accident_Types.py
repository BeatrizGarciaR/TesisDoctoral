# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 19:34:44 2021

@author: beatr
"""

import gurobipy as gp
from gurobipy import GRB
import random

# Sets #
I = [1, 2, 3, 4, 5, 6, 7, 8]
L = [1, 2, 3, 4, 5]
N = [1, 2, 3]

# Scenarios #
S = []
len_S = 3
elementos_S = [0, 1, 2, 3]
#probabilidades_S = [0.6, 0.8, 0.4, 0.1]
probabilidades_S = [0.6, 0.1, 0.4, 0.8]
opciones_S = []

for e, p in zip(elementos_S, probabilidades_S):
    opciones_S += [e]*int(p*10000)

for i in range(len_S):
    S.append([])
    for j in range(len(I)):
        a = int(random.choice(opciones_S))
        S[i].append(a)
print (S)
print()

#Response times

r_li = [[17, 23, 25, 25, 21, 23, 25, 22],
        [28, 20, 25, 9, 11, 26, 9, 25],
        [18, 13, 17, 28, 18, 20, 32, 19],
        [32, 20, 10, 32, 28, 29, 9, 26],
        [16, 30, 12, 30, 17, 27, 12, 18]]


# Other parameters #
wn_partial = [0, 0.5, 0.4]
pn_null = [1, 0.5, 0.3]
eta = 4
tau_r = 25

# Create a new model #
m = gp.Model("Different accident types")

# Create variables #
x_vars = {}
for l in L:
    x_vars[l] = m.addVar(vtype=GRB.INTEGER, 
                         name="located_"+str(l))

y_vars = {}
for s in range(len(S)):
    for l in L:
        for i in I:
            for n in N:
                y_vars[s+1,l,i,n] = m.addVar(vtype=GRB.BINARY, 
                                     name="dispatched_"+str(s+1)+str(l)+str(i)+str(n))

zfull_vars = {}
for s in range(len(S)):
    for i in I:
        for n in N:
            zfull_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                     name="full_"+str(s+1)+str(i)+str(n))

zpartial_vars = {}
for s in range(len(S)):
    for i in I:
        for n in N:
            zpartial_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                      name="partial_"+str(s+1)+str(i)+str(n))
            
znull_vars = {}
for s in range(len(S)):
    for i in I:
        for n in N:
            znull_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                     name="null_"+str(s+1)+str(i)+str(n))

# Set objective
m.setObjective(gp.quicksum(zfull_vars[s+1,i,n] + wn_partial[n-1]*zpartial_vars[s+1,i,n] - pn_null[n-1]*znull_vars[s+1,i,n]
                    for s in range(len(S))
                    for i in I
                    for n in N
                    )/len(S), 
                GRB.MAXIMIZE)

# m.setObjective(gp.quicksum(zfull_vars[s+1,i,n]  - pn_null[n-1]*znull_vars[s+1,i,n]
#                     for s in range(len(S))
#                     for i in I
#                     for n in N
#                     )/len(S), 
#                 GRB.MAXIMIZE)

# Add constraints

for s in range(len(S)):
    
    accidents = S[s]
    
    m.addConstr(gp.quicksum(x_vars[l]
                            for l in L) <= eta, "c2")
    
    for l in L:
        m.addConstr(gp.quicksum(y_vars[s+1,l,i,n]
                            for i in I
                            for n in N) <= x_vars[l], "c3")
    
    for i in I:
        k = accidents[i-1]
        if k != 0:
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,k]
                            for l in L) == k * zfull_vars[s+1,i,k], "c4")
    
    for i in I:
        k = accidents[i-1]
        if k != 0:
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,k]
                                    for l in L) == k*zfull_vars[s+1,i,k] + (k-1)*zpartial_vars[s+1,i,k], "c5")
            
    # for i in I:
    #     m.addConstr(gp.quicksum(y_vars[s+1,l,i,3]
    #                             for l in L) <= zpartial_vars[s+1,i,3], "c6")
            
    for i in I:
        for n in N:
            m.addConstr(zfull_vars[s+1,i,n] + zpartial_vars[s+1,i,n] <= 1, "c7")
                
    
    for i in I:
        k = accidents[i-1]
        if k != 0:
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,k]
                                        for l in L) + znull_vars[s+1,i,k] >= 1, "c8")
    
    for l in L:
        for i in I:
            for n in N:
                m.addConstr(int(r_li[l-1][i-1]) * y_vars[s+1,l,i,n] <= tau_r , "c9")

# Optimize model
m.optimize()

#imprimir variables 

f = open ('Resultados_Correctos.txt','w')
for v in m.getVars():
    f.write('%s %g' % (v.varName, v.x))
    f.write('\n')
f.close()
    
#imprimir el valor objetivo
print('Obj: %g' % m.objVal)
print("Finished")
print(" ")