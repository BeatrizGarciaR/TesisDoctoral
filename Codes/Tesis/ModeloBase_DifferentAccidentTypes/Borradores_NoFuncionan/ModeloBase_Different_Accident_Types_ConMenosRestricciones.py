# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 23:00:57 2021

@author: beatr
"""
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
probabilidades_S = [0.6, 0.8, 0.4, 0.1]
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

# Response time from potential site to demand point #
r_il = []
for i in range(len(I)):
    r_il.append([])
    for j in range(len(L)):
        b = random.randint(9, 32)
        r_il[i].append(b)
print (r_il)

# Other parameters #
wn_partial = [0, 0.5, 0.4]
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
    for i in I:
        for l in L:
            for n in N:
                y_vars[s+1,i,l,n] = m.addVar(vtype=GRB.BINARY, 
                                     name="dispatched_"+str(s+1)+str(i)+str(l)+str(n))

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

m.addConstr(gp.quicksum(x_vars[l]
                        for l in L) <= eta, "c2")

for s in range(len(S)):
    for l in L:
        m.addConstr(gp.quicksum(y_vars[s+1,i,l,n]
                                for i in I
                                for n in N) <= x_vars[l], "c3")
            

for s in range(len(S)):
    
    accidents = S[s]
    
    for i in I:
        
        k = accidents[i-1]
        if k != 0 :
            
            for n in N:
                if n == k:
                    print("entra n == k", n)
                    m.addConstr(gp.quicksum(y_vars[s+1,i,l,n]
                                    for l in L) <= k*zfull_vars[s+1,i,n], "c4")
                else:
                    m.addConstr(zfull_vars[s+1,i,n] <= 0,  "c_4_1")
            
            if k != 1:
                m.addConstr(gp.quicksum(y_vars[s+1,i,l,k]
                                        for l in L) <= (k-1)*zpartial_vars[s+1,i,k], "c5")
            
            if k == 3:
                m.addConstr(gp.quicksum(y_vars[s+1,i,l,k]
                                        for l in L) <= zpartial_vars[s+1,i,k], "c6")
                    
            m.addConstr(gp.quicksum(zfull_vars[s+1,i,n] + zpartial_vars[s+1,i,n] 
                                     for n in N) <= 1, "c7")
            
            m.addConstr(gp.quicksum(y_vars[s+1,i,l,k]
                                    for l in L) + znull_vars[s+1,i,k] >= 1, "c8")
            
            m.addConstr(r_il[i-1][l-1] * y_vars[s+1,i,l,k] <= tau_r , "c9")
        
        else:
            for n in N:
                m.addConstr(zfull_vars[s+1,i,n] <= 0,  "c_10_1")
                m.addConstr(zpartial_vars[s+1,i,n] <= 0,  "c_10_2")
                m.addConstr(znull_vars[s+1,i,n] <= 0,  "c_10_3")

# Optimize model
m.optimize()

#imprimir variables 

f = open ('Resultados_menosRestricciones.txt','w')
for v in m.getVars():
    f.write('%s %g' % (v.varName, v.x))
    f.write('\n')
f.close()
    
#imprimir el valor objetivo
print('Obj: %g' % m.objVal)
print("Finished")
print(" ")
    
