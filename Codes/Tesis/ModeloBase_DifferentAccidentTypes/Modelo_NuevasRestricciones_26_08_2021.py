# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:35:06 2021

@author: beatr
"""
######### NUEVO MODELO, AGREGANDO VARIABLE PARTIAL' ########


######################################################################
######################  INSTANCES ####################################
######################################################################

import gurobipy as gp
from gurobipy import GRB

tamaños_I = [10, 50, 100]
tamaños_L = [5, 20, 40]
tamaños_S = [10, 50, 100]


for i in range(3):
    archivo = open('Instancias_'
              +str(tamaños_I[i])+str('_')
              +str(tamaños_L[i])+str('_')
              +'3'+str('_')
              +str(tamaños_S[i])
              +'.txt', "r")
    
    len_I = int(archivo.readline())
    len_L = int(archivo.readline())
    len_N = int(archivo.readline())+1
    len_S = int(archivo.readline())
    
    # Sets #
    I = []
    line = archivo.readline().strip().split()
    for i in range(len_I):
        I.append(int(line[i]))
        
    L = []
    line = archivo.readline().strip().split()
    for i in range(len_L):
        L.append(int(line[i]))
        
    N = []
    line = archivo.readline().strip().split()
    for i in range(len_N):
        N.append(int(line[i]))
        
    
    #Scenarios
    S = []
    for l in range(len_S):
        line = archivo.readline().strip().split()
        S.append([])
        for i in range(len(I)):
            S[l].append(int(line[i]))   
            
    
    #Response times
    r_li = []
    for l in range(len(L)):
        line = archivo.readline().strip().split()
        r_li.append([])
        for i in range(len(I)):
            r_li[l].append(int(line[i]))   
    
    
    
    # Other parameters #
    wn_full = [0, 1, 1, 1]
    wn_partial = [0, 0, 0.5, 0.65]
    w3_partial1 = 0.3
    pn_null = [0, 1, 0.5, 0.4]
    eta = 11
    tau_r = 25
    a_i = 0
    
    ######################################################################
    ######################    MODEL   ####################################
    ######################################################################
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
                                         name="dispatched_"+str(s+1)+str('_')+str(l)+str('_')+str(i)+str('_')+str(n))
    
    zfull_vars = {}
    for s in range(len(S)):
        for i in I:
            for n in N:
                zfull_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                         name="full_"+str(s+1)+str('_')+str(i)+str('_')+str(n))
    
    zpartial_vars = {}
    for s in range(len(S)):
        for i in I:
            for n in N:
                zpartial_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                          name="partial_"+str(s+1)+str('_')+str(i)+str('_')+str(n))
    
    zpartiall_vars = {}
    for s in range(len(S)):
        for i in I:
            n = 3
            zpartiall_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                          name="partial1_"+str(s+1)+str('_')+str(i)+str('_')+str(n))
                
    znull_vars = {}
    for s in range(len(S)):
        for i in I:
            for n in N:
                znull_vars[s+1,i,n] = m.addVar(vtype=GRB.BINARY, 
                                         name="null_"+str(s+1)+str('_')+str(i)+str('_')+str(n))
    
    # Set objective
    m.setObjective(gp.quicksum(gp.quicksum(wn_full[n]*zfull_vars[s+1,i,n] for i in I for n in N) 
                               + gp.quicksum(wn_partial[n]*zpartial_vars[s+1,i,n] for i in I for n in N) 
                               + gp.quicksum(w3_partial1*zpartiall_vars[s+1,i,3] for i in I ) 
                               - gp.quicksum(pn_null[n]*znull_vars[s+1,i,n] for i in I for n in N) 
                                for s in range(len(S)))/len(S), 
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
            a_i = accidents[i-1]
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,a_i]
                                        for l in L) >= a_i * zfull_vars[s+1,i,a_i], "c4")
            for n in N:
                if n != a_i:
                    m.addConstr(zfull_vars[s+1,i,n] == 0, "c4_1")
    
        for i in I:
            a_i = accidents[i-1]
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,a_i]
                                        for l in L) >= a_i * zfull_vars[s+1,i,a_i] + (a_i - 1) * zpartial_vars[s+1,i,a_i], "c5")
            for n in N:
                if n != a_i:
                    m.addConstr(zpartial_vars[s+1,i,n] == 0, "c5_1")
    
        for i in I:
            a_i = accidents[i-1]
            if a_i == 3:
                m.addConstr(gp.quicksum(y_vars[s+1,l,i,a_i]
                                        for l in L) >= a_i * zfull_vars[s+1,i,a_i] + + (a_i - 1) * zpartial_vars[s+1,i,a_i] + zpartiall_vars[s+1,i,a_i], "c6")    
            for n in N:
                if n != a_i and n == 3:
                    m.addConstr(zpartiall_vars[s+1,i,n] == 0, "c6_1")
    
        for i in I:
            a_i = accidents[i-1]
            if a_i == 3:
                m.addConstr(zpartial_vars[s+1,i,a_i] + zpartiall_vars[s+1,i,a_i] <= 1, "c7")
        
        for i in I:
            a_i = accidents[i-1]
            m.addConstr(zfull_vars[s+1,i,a_i] + zpartial_vars[s+1,i,a_i] <= 1, "c8")
        
        for i in I:
            a_i = accidents[i-1]
            m.addConstr(gp.quicksum(y_vars[s+1,l,i,a_i]
                                            for l in L) + znull_vars[s+1,i,a_i] >= 1, "c8")
        
        for l in L:
            for i in I:
                a_i = accidents[i-1]
                m.addConstr(int(r_li[l-1][i-1]) * y_vars[s+1,l,i,a_i] <= tau_r , "c9")
    
    # Optimize model
    m.optimize()
    
    #imprimir variables 
    
    f = open ('Resultados_'
                  +str(len_I)+str('_')
                  +str(len_L)+str('_')
                  +str(len_N-1)+str('_')
                  +str(len_S)
                  +'.txt','w')
    
    for v in m.getVars():
        f.write('%s %g' % (v.varName, v.x))
        f.write('\n')
    f.close()
    
    m.write('model'+str(len_I)+str('_')
                  +str(len_L)+str('_')
                  +str(len_N-1)+str('_')
                  +str(len_S)+'.lp')
    m.write('model'+str(len_I)+str('_')
                  +str(len_L)+str('_')
                  +str(len_N-1)+str('_')
                  +str(len_S)+'.mps')
        
    #imprimir el valor objetivo
    print('Obj: %g' % m.objVal)
    print("Finished")
    print(" ")
