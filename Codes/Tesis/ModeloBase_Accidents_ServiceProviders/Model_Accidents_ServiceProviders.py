# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:10:34 2021

@author: beatr
"""
######### NUEVO MODELO, AGREGANDO VARIABLE PARTIAL' ########


######################################################################
######################  INSTANCES ####################################
######################################################################

import gurobipy as gp
from gurobipy import GRB


tamaños_I = [20, 50, 100]
tamaños_L = [8, 20, 40]
tamaños_S = [5, 20, 50]
repeticiones = 5

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            for rep in range(repeticiones):
    
                #Nombre: Instancias_Prueba_I_L_M_N_S_Rep
                
                archivo = open('Instancias_Prueba_'
                          +str(tamaños_I[iconj])+str('_')
                          +str(tamaños_L[jconj])+str('_')
                          +'2'+str('_')
                          +'3'+str('_')
                          +str(tamaños_S[sconj])+str('_')
                          +str(rep+1)
                          +'_.txt', "r")
                
                len_I = int(archivo.readline())
                len_L = int(archivo.readline())
                len_M = int(archivo.readline())
                len_N = int(archivo.readline())
                len_S = int(archivo.readline())
                repite = int(archivo.readline())
                
                # Sets #
                I = []
                line = archivo.readline().strip().split()
                for i in range(len_I):
                    I.append(int(line[i]))
                    
                L = []
                line = archivo.readline().strip().split()
                for i in range(len_L):
                    L.append(int(line[i]))
                
                len_L1 = int(archivo.readline())
                L1 = []
                line = archivo.readline().strip().split()
                for i in range(len_L1):
                    L1.append(int(line[i]))
            
                len_L2 = int(archivo.readline())
                L2 = []
                line = archivo.readline().strip().split()
                for i in range(len_L2):
                    L2.append(int(line[i]))
                    
                M = []
                line = archivo.readline().strip().split()
                for i in range(len_M):
                    M.append(int(line[i]))
                    
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
                        
                
                # CRUM Response times
                r_li1 = []
                for l in range(len(L)):
                    line = archivo.readline().strip().split()
                    r_li1.append([])
                    for i in range(len(I)):
                        r_li1[l].append(int(line[i]))   
                  
                # Red Cross Response times
                r_li2 = []
                for l in range(len(L)):
                    line = archivo.readline().strip().split()
                    r_li2.append([])
                    for i in range(len(I)):
                        r_li2[l].append(int(line[i]))
                
                
                # Other parameters #
                wn_partial = [0, 0.5, 0.65]
                w3_partial1 = 0.3
                pn_null = [1, 0.5, 0.4]
                eta = [5, 3]
                tau_r = 25
                a_i = 0
                
                ######################################################################
                ######################    MODEL   ####################################
                ######################################################################
                
                model = gp.Model("Different accident types")
                
                # Create variables #
                x_vars = {}
                for l in L:
                    for m in M:
                        x_vars[l,m] = model.addVar(vtype=GRB.INTEGER, 
                                         name="located "+str(l)+" "+str(m))
                
                y_vars = {}
                for s in range(len(S)):
                    for l in L:
                        for i in I:
                            for m in M:
                                for n in N:
                                    y_vars[s+1,l,i,m,n] = model.addVar(vtype=GRB.BINARY, 
                                                     name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(i)+str(' ')+str(m)+str(' ')+str(n))
                
                zfull_vars = {}
                for s in range(len(S)):
                    for i in I:
                        for n in N:
                            zfull_vars[s+1,i,n] = model.addVar(vtype=GRB.BINARY, 
                                                     name="full "+str(s+1)+str(' ')+str(i)+str(' ')+str(n))
                
                zpartial_vars = {}
                for s in range(len(S)):
                    for i in I:
                        for n in N:
                            zpartial_vars[s+1,i,n] = model.addVar(vtype=GRB.BINARY, 
                                                      name="partial "+str(s+1)+str(' ')+str(i)+str(' ')+str(n))
                
                zpartiall_vars = {}
                for s in range(len(S)):
                    for i in I:
                        n = 3
                        zpartiall_vars[s+1,i,n] = model.addVar(vtype=GRB.BINARY, 
                                                      name="partial1 "+str(s+1)+str(' ')+str(i)+str(' ')+str(n))
                            
                znull_vars = {}
                for s in range(len(S)):
                    for i in I:
                        for n in N:
                            znull_vars[s+1,i,n] = model.addVar(vtype=GRB.BINARY, 
                                                     name="null "+str(s+1)+str(' ')+str(i)+str(' ')+str(n))
                
                # Set objective
                model.setObjective(gp.quicksum
                                   (gp.quicksum
                                   (gp.quicksum(zfull_vars[s+1,i,n] - pn_null[n-1]*znull_vars[s+1,i,n] for n in N)
                                    + gp.quicksum(wn_partial[n-1]*zpartial_vars[s+1,i,n-1] for n in [2,3])
                                    + w3_partial1*zpartiall_vars[s+1,i,3]
                                    for i in I)
                                   for s in range(len(S)))/len(S), 
                                   GRB.MAXIMIZE)
                
                
                # Add constraints
                
                for s in range(len(S)):
                    
                    accidents = S[s]
                    
                    model.addConstr(gp.quicksum(x_vars[l,1]
                                            for l in L1) <= eta[0], "c2")
            
                    model.addConstr(gp.quicksum(x_vars[l,2]
                                            for l in L2) <= eta[1], "c3")
                    
                    for l in L:
                        if l in L1:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,1,n]
                                                        for i in I
                                                        for n in [1,2,3]) <= x_vars[l,1], "c4")
            
                        else:
                            for i in I:
                                for n in N:
                                    model.addConstr(y_vars[s+1, l, i, 1, n] == 0, "c4_1")
            
                    for l in L:
                        if l in L2:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,2,n]
                                                        for i in I
                                                        for n in N) <= x_vars[l,2], "c5")
                                
                        else:
                            for i in I:
                                for n in N:
                                    model.addConstr(y_vars[s+1, l, i, 2, n] == 0, "c5_1")
                            
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i != 0:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,m,a_i]
                                                        for l in L
                                                        for m in M) >= a_i * zfull_vars[s+1,i,a_i], "c6")
                            for n in N:
                                if n != a_i:
                                    model.addConstr(zfull_vars[s+1,i,n] == 0, "c6_1")
                        else:
                            for n in N:
                                model.addConstr(zfull_vars[s+1,i,n] == 0, "c6_2")
                
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i != 0 and a_i != 1:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,m,a_i]
                                                        for l in L
                                                        for m in M) >= a_i * zfull_vars[s+1,i,a_i] + (a_i - 1) * zpartial_vars[s+1,i,a_i], "c7")
                            for n in N:
                                if n != a_i:
                                    model.addConstr(zpartial_vars[s+1,i,n] == 0, "c7_1")
                        else:
                            for n in N:
                                model.addConstr(zpartial_vars[s+1,i,n] == 0, "c7_2")
                
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i == 3:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,m,a_i]
                                                    for l in L
                                                    for m in M) >= a_i * zfull_vars[s+1,i,a_i] + + (a_i - 1) * zpartial_vars[s+1,i,a_i] + zpartiall_vars[s+1,i,a_i], "c8")    
                        for n in N:
                            if n != a_i and n == 3:
                                model.addConstr(zpartiall_vars[s+1,i,n] == 0, "c8_1")
                        
                
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i == 3:
                            model.addConstr(zfull_vars[s+1,i,a_i] + zpartial_vars[s+1,i,a_i] + zpartiall_vars[s+1,i,a_i] <= 1, "c9")
                    
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i != 0:
                            model.addConstr(zfull_vars[s+1,i,a_i] + zpartial_vars[s+1,i,a_i] <= 1, "c_10")
                    
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i != 0:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,m,a_i]
                                                            for l in L
                                                            for m in M) + znull_vars[s+1,i,a_i] >= 1, "c_11")
                    
                    for l in L:
                        for i in I:
                            a_i = accidents[i-1]
                            if a_i != 0:
                                model.addConstr(int(r_li1[l-1][i-1]) * y_vars[s+1,l,i,1,a_i] <= tau_r , "c_12")
             
                    for l in L:
                        for i in I:
                            a_i = accidents[i-1]
                            if a_i != 0:
                                model.addConstr(int(r_li2[l-1][i-1]) * y_vars[s+1,l,i,2,a_i] <= tau_r , "c_12_1")
                    
                    for i in I:
                        a_i = accidents[i-1]
                        if a_i != 0:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,i,m,a_i]
                                                        for l in L
                                                        for m in M) <= a_i, "c_13")
                        
                            
                # Optimize model
                model.optimize()
                
                #imprimir variables 
                
                #Nombre: Resultados_Prueba_I_L_M_N_S
                
                f = open ('Resultados_Prueba_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                f.write('Obj: %g' % model.objVal)
                f.write('\n')
                
                for v in model.getVars():
                    f.write('%s %g' % (v.varName, v.x))
                    f.write('\n')
                    
                #imprimir el valor objetivo
                print('Obj: %g' % model.objVal)
                print("Finished")
                print(" ")
            
                f.close()
                
                model.write('model_'+str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)+'_.lp')
                model.write('model_'+str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)+'_.mps')
            
            
                archivo.close()
                
                resultados = open ('Resultados_Prueba_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','r')
                
                line = resultados.readline()
                
                # Funcion Objetivo
                
                fobj = open ('FObj_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                fobj.write(str(len_I)+str(' ')
                           +str(len_L)+str(' ')
                           +str(len_S)+str(' ')
                           +str(rep+1)+str(' ')
                           +line)
                
                fobj.close()
                
                #Located
                  
                located = open ('Located_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                
                count = 0
                for i in range(len(x_vars)):
                    aux = []
                    line = resultados.readline().strip().split()
                    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
                        count = count + 1
                        for i in range(len(line)):
                            if i == 0:
                                aux.append(line[i])
                            else:
                                aux.append(int(line[i]))
                    
                        located.write(str(len_I)+str(' ')
                                      +str(len_L)+str(' ')
                                      +str(len_S)+str(' ')
                                      +str(rep+1)+str(' '))
                        for j in range(len(aux)):
                            located.write(str(aux[j])+str(" "))
                        located.write("\n")
                if count == 0:
                    for j in range(8):
                        located.write("NA"+str(' '))
                    
                located.close()
                
                # Dispatched
                
                dispatched = open ('Dispatched_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                count = 0
                for i in range(len(y_vars)):
                    aux = []
                    line = resultados.readline().strip().split()
                    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
                        count = count + 1
                        for i in range(len(line)):
                            if i == 0:
                                aux.append(line[i])
                            else:
                                aux.append(int(line[i]))
                        dispatched.write(str(len_I)+str(' ')
                                      +str(len_L)+str(' ')
                                      +str(len_S)+str(' ')
                                      +str(rep+1)+str(' '))
                        for j in range(len(aux)):
                            dispatched.write(str(aux[j])+str(" "))
                        dispatched.write("\n")
                if count == 0:
                    for j in range(11):
                        dispatched.write("NA"+str(' '))
                
                dispatched.close()
                
                # Full
                
                full = open ('Full_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                
                count = 0
                for i in range(len(zfull_vars)):
                    aux = []
                    line = resultados.readline().strip().split()
                    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
                        count = count + 1
                        for i in range(len(line)):
                            if i == 0:
                                aux.append(line[i])
                            else:
                                aux.append(int(line[i]))
                        full.write(str(len_I)+str(' ')
                                      +str(len_L)+str(' ')
                                      +str(len_S)+str(' ')
                                      +str(rep+1)+str(' '))
                        for j in range(len(aux)):
                            full.write(str(aux[j])+str(" "))
                        full.write("\n")
                if count == 0:
                    for j in range(9):
                        full.write("NA"+str(' '))
                
                full.close()
                
                # Partial
                
                partial = open ('Partial_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                
                count = 0
                for i in range(len(zpartial_vars)):
                    aux = []
                    line = resultados.readline().strip().split()
                    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
                        count = count + 1
                        for i in range(len(line)):
                            if i == 0:
                                aux.append(line[i])
                            else:
                                aux.append(int(line[i]))
                        partial.write(str(len_I)+str(' ')
                                      +str(len_L)+str(' ')
                                      +str(len_S)+str(' ')
                                      +str(rep+1)+str(' '))
                        for j in range(len(aux)):
                            partial.write(str(aux[j])+str(" "))
                        partial.write("\n")
                if count == 0:
                    for j in range(9):
                        partial.write("NA"+str(' '))
                
                partial.close()
                
                # Partial_1
                
                partial1 = open ('Partial1_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                
                count = 0
                for i in range(len(zpartiall_vars)):
                    aux = []
                    line = resultados.readline().strip().split()
                    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
                        count = count + 1
                        for i in range(len(line)):
                            if i == 0:
                                aux.append(line[i])
                            else:
                                aux.append(int(line[i]))
                        partial1.write(str(len_I)+str(' ')
                                      +str(len_L)+str(' ')
                                      +str(len_S)+str(' ')
                                      +str(rep+1)+str(' '))
                        for j in range(len(aux)):
                            partial1.write(str(aux[j])+str(" "))
                        partial1.write("\n")
                if count == 0:
                    for j in range(9):
                        partial1.write("NA"+str(' '))
            
                
                partial1.close()
            
                # Null
                
                null = open ('Null_'
                              +str(len_I)+str('_')
                              +str(len_L)+str('_')
                              +str(len_M)+str('_')
                              +str(len_N)+str('_')
                              +str(len_S)+str('_')
                              +str(repite)
                              +'_.txt','w')
                
                
                count = 0
                for i in range(len(zfull_vars)):
                    aux = []
                    line = resultados.readline().strip().split()
                    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
                        count = count + 1
                        for i in range(len(line)):
                            if i == 0:
                                aux.append(line[i])
                            else:
                                aux.append(int(line[i]))
                        null.write(str(len_I)+str(' ')
                                      +str(len_L)+str(' ')
                                      +str(len_S)+str(' ')
                                      +str(rep+1)+str(' '))
                        for j in range(len(aux)):
                            null.write(str(aux[j])+str(" "))
                        null.write("\n")
                if count == 0:
                    for j in range(9):
                        null.write("NA"+str(' '))
                
                null.close()
                
                resultados.close()