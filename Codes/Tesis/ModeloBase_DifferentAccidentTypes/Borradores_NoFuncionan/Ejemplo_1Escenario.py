# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 18:03:44 2021

@author: beatr
"""
import gurobipy as gp
from gurobipy import GRB

# Sets #
I = [1, 2, 3, 4, 5, 6, 7, 8]
L = [1, 2, 3, 4, 5]
N = [1, 2, 3]

# Scenarios #
S = [[1, 0, 0, 2, 0, 0, 0, 0]]

#Response times

r_il = [[24, 19, 31, 29, 22],
        [29, 15, 9, 16, 10],
        [13, 12, 23, 25, 26],
        [17, 28, 15, 28, 12],
        [29, 13, 13, 13, 9],
        [25, 12, 30, 9, 17],
        [24, 31, 32, 13, 24],
        [12, 28, 20, 13, 13]]


# Other parameters #
wn_partial = [0, 0.4, 0.3]
pn_null = [1, 0.5, 0.3]
eta = 2
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
            for n in N:
                if n != k:
                    m.addConstr(zfull_vars[s+1,i,n] == 0, "c4_1")
        else:
            for n in N:
                m.addConstr(zfull_vars[s+1,i,n] == 0, "c4_2")
    
    for i in I:
        k = accidents[i-1]
        if k != 0:
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,k]
                                    for l in L) == k * zfull_vars[s+1,i,k] + (k-1) * zpartial_vars[s+1,i,k], "c5")
            for n in N:
                if n != k:
                    m.addConstr(zpartial_vars[s+1,i,n] == 0, "c5_1")
        else:
            for n in N:
                m.addConstr(zpartial_vars[s+1,i,n] == 0, "c5_2")
            
    # for i in I:
    #     k = accidents[i-1]
    #     if k != 0:
    #         m.addConstr(gp.quicksum(y_vars[s+1,l,i,k]
    #                                 for l in L) == k * zfull_vars[s+1,i,k] 
    #                                     + (k-1)*zpartial_vars[s+1,i,k]
    #                                     + (k-2)*zpartial_vars[s+1,i,k], "c6")
    #         for n in N:
    #             if n != k:
    #                 m.addConstr(zpartial_vars[s+1,i,n] == 0, "c6_1")
    #     else:
    #         for n in N:
    #             m.addConstr(zpartial_vars[s+1,i,n] == 0, "c6_2")    
            
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
                m.addConstr(int(r_il[i-1][l-1]) * y_vars[s+1,l,i,n] <= tau_r , "c9")


# Optimize model
m.optimize()

#imprimir variables 

f = open ('Resultados_1Escenario.txt','w')
for v in m.getVars():
    f.write('%s %g' % (v.varName, v.x))
    f.write('\n')
f.close()
    
#imprimir el valor objetivo
print('Obj: %g' % m.objVal)
print("Finished")
print(" ")