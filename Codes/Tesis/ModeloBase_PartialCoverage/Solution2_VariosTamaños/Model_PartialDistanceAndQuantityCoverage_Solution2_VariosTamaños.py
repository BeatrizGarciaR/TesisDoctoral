# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 01:33:45 2022

@author: beatr
"""
######################################################################
######################  INSTANCES ####################################
######################################################################

import gurobipy as gp
from gurobipy import GRB

# tamaños_I = [20, 50, 100]
# tamaños_L = [8, 20, 40]
# tamaños_S = [5, 20, 50]
#repeticiones = 5

tamaños_I = [5, 10, 20]
tamaños_L = [10, 25, 40]
tamaños_S = [3, 7, 12]
K = [1,2]


for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            #for rep in range(repeticiones):
    
            #Nombre: Instancias_Prueba_I_L_M_N_S_Rep
                
            archivo = open('Instancias_Prueba_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')
                      +'2'+str('_')
                      +'3'+str('_')
                      +str(tamaños_S[sconj])+str('_')
                      #+str(rep+1)
                      +'_.txt', "r")
            
            len_I = int(archivo.readline())
            len_L = int(archivo.readline())
            len_M = int(archivo.readline())
            len_N = int(archivo.readline())
            len_S = int(archivo.readline())
            #repite = int(archivo.readline())
            
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
                count = 0
                line = archivo.readline().strip().split()
                #print("line", line)
                S.append([])
                for i in range(len(I)):
                    #print("line[i]", line[count])
                    S[l].append([])
                    for k in range(len(K)):
                        #print("line[count]", line[count])
                        S[l][i].append(int(line[count]))
                        if count < len(line)-1:
                            count += 1
                        #S[l][i].append(int(line[i+1]))
                    
            
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
                    
            cil = []
            for i in range(len(I)):
                line = archivo.readline().strip().split()
                cil.append([])
                for l in range(len(L)):
                    cil[i].append(float(line[l]))   
            
            
            # Other parameters #
            p = 0.3
            eta = [7, 4]
            t = 10
            tmax = 25
                
            ######################################################################
            ######################    MODEL   ####################################
            ######################################################################
            
            model = gp.Model("PartialRateCoverage")
            
            # Create variables #
            x_vars = {}
            for l in L:
                for k in K:
                    x_vars[l,k] = model.addVar(vtype=GRB.INTEGER, 
                                     name="located "+str(l)+str(' ')+str(k))
            
            y_vars = {}
            for s in range(len(S)):
                for l in L:
                    for i in I:
                        for k in K:
                            y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                                                 name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(k)+str(' ')+str(i))
                       

            obj = gp.LinExpr()
            for s in range(len(S)):
                for i in I:
                    if S[s][i-1][0] + S[s][i-1][1] != 0:
                        obj += gp.quicksum(cil[i-1][l-1]*y_vars[s+1,l,k,i] for l in L for k in K)/(len(S)*(S[s][i-1][0] + S[s][i-1][1]))
            
            model.setObjective(obj, GRB.MAXIMIZE)        
            
            # Add constraints
            
            for s in range(len(S)):
                
                for k in K:
                    model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c2")
                
                for l in L:
                    for k in K:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,k,i] for i in I) <= x_vars[l,k], "c3")
      
                for i in I:
                    for k in K:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,k,i] for l in L) <= S[s][i-1][k-1], "c4")
                

                        
            # Optimize model
            model.optimize()
            
            #imprimir variables 
            
            #Nombre: Resultados_Prueba_I_L_M_N_S
            
            f = open ('Resultados_Prueba_'
                          +str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(K))+str('_')
                          +str(len(N))+str('_')
                          +str(len(S))+str('_')
                          +str('Solution2_aik=0_soloi')+'_.txt','w')
            
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
            
            model.write('model_'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(K))+str('_')
                          +str(len(N))+str('_')
                          +str(len(S))+str('_')+str('Solution2_aik=0_soloi')+'_.lp')
            model.write('model_'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(K))+str('_')
                          +str(len(N))+str('_')
                          +str(len(S))+str('_')+str('Solution2_aik=0_soloi')+'_.mps')
            
            

            ########################################
            # VERIFICANDO SI LA SOLUCION ES FACTIBLE 
            ########################################
            
            feasible = open ('Feasible_'
                          +str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(K))+str('_')
                          +str(len(N))+str('_')
                          +str(len(S))+str('_')
                          +str('Solution2_aik=0_soloi')+'_.sol','w')
            
            # Guardando la información de x
            ambulancesNumber = []
            for k in K:
                conteo = 0
                for l in L:
                    a = x_vars[l,k]
                    if (a.x == 1):
                        conteo = conteo + 1
                        #print(a.varName, a.x)
                ambulancesNumber.append(conteo)
            #print(ambulancenNumber)
            #print()
            
            
            # VERIFICANDO QUE NO SE SOBREPASE LA CANTIDAD DE AMBULANCIAS LOCALIZADAS
            ambulanceLocation = []
            for k in K:
                if(ambulancesNumber[k-1] == eta[k-1]):
                    ambulanceLocation.append("equal to eta")
                    
                if(ambulancesNumber[k-1] < eta[k-1]):
                    ambulanceLocation.append("less than eta")
                    
                if(ambulancesNumber[k-1] > eta[k-1]):
                    ambulanceLocation.append("more to eta")
            #print(ambulanceLocation)
            #print()
            
            for k in K:
                if(ambulanceLocation[k-1] == 'more than eta'):
                    feasible.write("MORE AMBULANCE THAN AVAILABLE")
                    feasible.write("\n")
                    print("MORE AMBULANCE THAN AVAILABLE")
                    
            
            # Guardando la información de y
            dispatches = []
            for s in range(len(S)):
                dispatches.append([])
                for i in I: 
                    dispatches[s].append([])
                    for k in K: 
                        conteo = 0
                        for l in L:
                            a = y_vars[s+1,l,k,i]
                            if (a.x == 1):
                                conteo = conteo + 1
                                #print("ver si acomoda por i", a, a.x)
                        dispatches[s][i-1].append(conteo)                         
            #print(dispatches)
            #print()
            
        
            # VERIFICANDO LAS COBERTURAS
            coverage = []
            for s in range(len(S)):
                coverage.append([])
                for i in I: 
                    coverage[s].append([])
                    for k in K: 
                        if(S[s][i-1][k-1] == dispatches[s][i-1][k-1] and S[s][i-1][k-1] == 0):
                            coverage[s][i-1].append("no accident")
                            
                        if(S[s][i-1][k-1] == dispatches[s][i-1][k-1] and S[s][i-1][k-1] != 0):
                            coverage[s][i-1].append("full")
                            
                        if(S[s][i-1][k-1] > dispatches[s][i-1][k-1] and S[s][i-1][k-1] != 0 and dispatches[s][i-1][k-1] != 0):
                            coverage[s][i-1].append("partial")
                            
                        if(S[s][i-1][k-1] > 0 and dispatches[s][i-1][k-1] == 0):
                            coverage[s][i-1].append("null")
                    
                        if(S[s][i-1][k-1] < dispatches[s][i-1][k-1]):
                            coverage[s][i-1].append("over serviced")
                            
            #for s in range(len(S)):
            #    print(coverage[s]) 
            #print()
            
            
            # VERIFICANDO QUE NO HAYA SOBRE COBERTURA
            for s in range(len(S)):
                for i in I: 
                    for k in K:
                        if (coverage[s][i-1][k-1] == 'over serviced'):
                            feasible.write("MODEL OVER SERVICED")
                            feasible.write("\n")
                            print("MODEL OVER SERVICED")
              
            # Número de ambulancias despachadas
            numberDispatched = []
            for s in range(len(S)):
                numberDispatched.append([])
                for l in L:
                    numberDispatched[s].append([])
                    for k in K:
                        conteo = 0
                        for i in I:
                            a = y_vars[s+1,l,k,i]
                            if (a.x == 1):
                                conteo = conteo + 1
                        numberDispatched[s][l-1].append(conteo)
                    
            #print(numberDispatched)
            #print(" ")
            
            #Número de ambulancias localizadas 
            locationQuantity = []
            for l in L:
                locationQuantity.append([])
                for k in K:
                    a = x_vars[l,k]
                    if(a.x == -0.0):
                        locationQuantity[l-1].append(0)
                    else:
                        locationQuantity[l-1].append(int(a.x))
            
            #print(locationQuantity)
            #print(" ")
                    
            
            # Verificando que se despachen la cantidad de ambulancias que están localizadas
            feasibleDispatched = []
            for s in range(len(S)):
                feasibleDispatched.append([])
                for l in L:
                    feasibleDispatched[s].append([])
                    for k in K:
                        if(numberDispatched[s][l-1][k-1] == locationQuantity[l-1][k-1] and locationQuantity[l-1][k-1] != 0):
                            feasibleDispatched[s][l-1].append("all used")
                        
                        if(numberDispatched[s][l-1][k-1] == locationQuantity[l-1][k-1] and locationQuantity[l-1][k-1] == 0):
                            feasibleDispatched[s][l-1].append("not located")
                        
                        if(numberDispatched[s][l-1][k-1] < locationQuantity[l-1][k-1] and numberDispatched[s][l-1][k-1] == 0):
                            feasibleDispatched[s][l-1].append("not used")
                        
                        if(numberDispatched[s][l-1][k-1] < locationQuantity[l-1][k-1] and numberDispatched[s][l-1][k-1] != 0):
                            feasibleDispatched[s][l-1].append("not all used")
                            
                        if(numberDispatched[s][l-1][k-1] > locationQuantity[l-1][k-1]):
                            feasibleDispatched[s][l-1].append("over used")
            #print(feasibleDispatched)
            #print(" ")
                        
            # VERIFICANDO QUE NO SE DESPACHEN DE MÁS LAS AMBULANCIAS}
            for s in range(len(S)):
                for l in L:
                    for k in K:
                         if (feasibleDispatched[s][l-1][k-1] == 'over used'):
                            feasible.write("MODEL OVER USED")
                            feasible.write("\n")
                            print("MODEL OVER USED")
                        
            
             
            feasible.write("Objective value")
            feasible.write("\n")
            feasible.write('%g' % model.objVal)
            feasible.write("\n")
            feasible.write("\n")
            
            feasible.write("Eta")
            feasible.write("\n")
            feasible.write(str(eta))
            feasible.write("\n")
            feasible.write("\n")
            
            feasible.write("Ambulance located")
            feasible.write("\n")
            feasible.write(str(ambulancesNumber))
            feasible.write("\n")
            feasible.write("\n")
            
            feasible.write("Ambulance location")
            feasible.write("\n")
            feasible.write(str(ambulanceLocation))
            feasible.write("\n")
            feasible.write("\n")
            
            feasible.write("Scnenario")
            feasible.write("\n")
            for s in range(len(S)):
                feasible.write(str(S[s]))
                feasible.write("\n")
            feasible.write("\n")
            
            feasible.write("Dispatches")
            feasible.write("\n")
            for s in range(len(S)):
                feasible.write(str(dispatches[s]))
                feasible.write("\n")
            feasible.write("\n")
            
            feasible.write("Coverage")
            feasible.write("\n")
            for s in range(len(S)):
                feasible.write(str(coverage[s]))
                feasible.write("\n")
            feasible.write("\n")
            
            feasible.close()
            
            
            # resultados = open ('Resultados_Prueba_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str('Solution2_aik=0_soloi')+'_.txt','r')
            
            # line = resultados.readline()
            
            # # Funcion Objetivo
            
            # fobj = open ('FObj_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str('Solution2_aik=0_soloi')+'_.txt','w')
            
            # fobj.write(str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str(' ')
            #               +line)
            
            # fobj.close()
            
            # #Located
              
            # located = open ('Located_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str('Solution2_aik=0_soloi')+'_.txt','w')
            
            
            # count = 0
            # for i in range(len(x_vars)):
            #     aux = []
            #     line = resultados.readline().strip().split()
            #     if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
            #         count = count + 1
            #         for i in range(len(line)):
            #             if i == 0:
            #                 aux.append(line[i])
            #             else:
            #                 aux.append(int(line[i]))
                
            #         # located.write(str(len(I))+str('_')
            #         #       +str(len(L))+str('_')
            #         #       +str(len(K))+str('_')
            #         #       +str(len(N))+str('_')
            #         #       +str(len(S))+str('_'))
            #         for j in range(len(aux)):
            #             located.write(str(aux[j])+str(" "))
            #         located.write("\n")
            # if count == 0:
            #     for j in range(8):
            #         located.write("NA"+str(' '))
                
            # located.close()
            
            # # Dispatched
            
            # dispatched = open ('Dispatched_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str('Solution2_aik=0_soloi')+'_.txt','w')
            
            # count = 0
            # for i in range(len(y_vars)):
            #     aux = []
            #     line = resultados.readline().strip().split()
            #     if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
            #         count = count + 1
            #         for i in range(len(line)):
            #             if i == 0:
            #                 aux.append(line[i])
            #             else:
            #                 aux.append(int(line[i]))
            #         # dispatched.write(str(len(I))+str('_')
            #         #       +str(len(L))+str('_')
            #         #       +str(len(K))+str('_')
            #         #       +str(len(N))+str('_')
            #         #       +str(len(S))+str('_'))
            #         for j in range(len(aux)):
            #             dispatched.write(str(aux[j])+str(" "))
            #         dispatched.write("\n")
            # if count == 0:
            #     for j in range(11):
            #         dispatched.write("NA"+str(' '))
            
            # dispatched.close()
            
            # # Null
            
            # # null = open ('Null_'
            # #               +str(len(I))+str('_')
            # #               +str(len(L))+str('_')
            # #               +str(len(K))+str('_')
            # #               +str(len(N))+str('_')
            # #               +str(len(S))+str('_')+'_.txt','w')
            
            
            # # count = 0
            # # for i in range(len(zfull_vars)):
            # #     aux = []
            # #     line = resultados.readline().strip().split()
            # #     if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
            # #         count = count + 1
            # #         for i in range(len(line)):
            # #             if i == 0:
            # #                 aux.append(line[i])
            # #             else:
            # #                 aux.append(int(line[i]))
            # #         null.write(str(len_I)+str(' ')
            # #                       +str(len_L)+str(' ')
            # #                       +str(len_S)+str(' ')
            # #                       +str(rep+1)+str(' '))
            # #         for j in range(len(aux)):
            # #             null.write(str(aux[j])+str(" "))
            # #         null.write("\n")
            # # if count == 0:
            # #     for j in range(9):
            # #         null.write("NA"+str(' '))
            
            # # null.close()
            
            # resultados.close()