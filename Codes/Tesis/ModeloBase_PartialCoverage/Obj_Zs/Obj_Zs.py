# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 03:26:13 2022

@author: beatr
"""

######################################################################
######################  INSTANCES ####################################
######################################################################

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import csv
import time
#import xlsxwriter 

import xlwt


# tamaños_I = [100, 500, 1000]
# tamaños_L = [30, 45, 70]
# tamaños_S = [50, 100, 500]

# tamaños_I = [20, 50, 100]
# tamaños_L = [8, 20, 40]
# tamaños_S = [5, 20, 50]
#repeticiones = 5

# tamaños_I = [20, 50, 80, 95]
# tamaños_L = [40, 50, 70, 85]
# tamaños_S = [12, 25, 30, 40]

# tamaños_I = [50, 200, 350]
# tamaños_L = [20, 40, 55]
# tamaños_S = [15, 50, 75]

# tamaños_I = [100, 300, 500, 1000]
# tamaños_L = [70, 100, 200, 500]
# tamaños_S = [1000]

tamaños_I = [100, 300, 500, 1000]
tamaños_L = [70, 100, 200, 500]
tamaños_S = [50, 100, 500]


# tamaños_I = [1000]
# tamaños_L = [40]
# tamaños_S = [50]

K = [1,2]

countcsv = 1

book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('Tesis', cell_overwrite_ok=True)

def data_cb(m, where):
    if where == gp.GRB.Callback.MIP:
        cur_obj = m.cbGet(gp.GRB.Callback.MIP_OBJBST)
        cur_bd = m.cbGet(gp.GRB.Callback.MIP_OBJBND)
        #sepa = model.cbGet(GRB.callback.MIP_NODCNT)
        #sepa2 = model.cbGet(GRB.callback.MIP_ITRCNT)
        gap = abs((cur_obj - cur_bd) / cur_obj)*100  
        status = gp.GRB.OPTIMAL
        #gap = cur_obj - cur_bd
        # Did objective value or best bound change?
        # if m._obj != cur_obj or m._bd != cur_bd:
        #     m._obj = cur_obj
        #     m._bd = cur_bd
        #     m._data.append([time.time() - model._start, cur_obj, cur_bd])
        m._data.append(["time", "best", "best bound", "gap %", "status"])
        m._data.append([time.time() - model._start, cur_obj, cur_bd, gap, status])


for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            #for rep in range(repeticiones):
    
                #Nombre: Instancias_Prueba_I_L_M_N_S_Rep
                
                
            # archivo = open('Instancias_Prueba_'
            #           +str(tamaños_I[iconj])+str('_')
            #           +str(tamaños_L[jconj])+str('_')
            #           +'2'+str('_')
            #           +'3'+str('_')
            #           +str(tamaños_S[sconj])+str('_')
            #           #+str(rep+1)
            #           +'_.txt', "r")
            
            archivo = open('Instancias_Prueba_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')+"2"+"_"+"3"+"_"
                      +str(tamaños_S[sconj])+"__"
                      +'.txt', "r")
            
            len_I = int(archivo.readline())
            len_L = int(archivo.readline())
            len_M = int(archivo.readline())
            len_N = int(archivo.readline())
            len_S = int(archivo.readline())
            #repite = int(archivo.readline())
            
            # Sets #
            
            I = []
            for i in range(len_I):
                I.append(int(i+1))
                
            L = []
            for i in range(len_L):
                L.append(int(i+1))
            
            # I = []
            # line = archivo.readline().strip().split()
            # for i in range(len_I):
            #     I.append(int(line[i]))
                
            # L = []
            # line = archivo.readline().strip().split()
            # for i in range(len_L):
            #     L.append(int(line[i]))
            
            # len_L1 = int(archivo.readline())
            # L1 = []
            # line = archivo.readline().strip().split()
            # for i in range(len_L1):
            #     L1.append(int(line[i]))
        
            # len_L2 = int(archivo.readline())
            # L2 = []
            # line = archivo.readline().strip().split()
            # for i in range(len_L2):
            #     L2.append(int(line[i]))
                
            # M = []
            # line = archivo.readline().strip().split()
            # for i in range(len_M):
            #     M.append(int(line[i]))
                
            # N = []
            # line = archivo.readline().strip().split()
            # for i in range(len_N):
            #     N.append(int(line[i]))
                
            
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
              
            #Red Cross Response times
            r_li2 = []
            for l in range(len(L)):
                line = archivo.readline().strip().split()
                r_li2.append([])
                for i in range(len(I)):
                    r_li2[l].append(int(line[i]))
                    
            cli = []
            for l in range(len(L)):
                line = archivo.readline().strip().split()
                cli.append([])
                for i in range(len(I)):
                    cli[l].append(float(line[i]))   
            
            
            # Other parameters #
            p = np.amax(cli)/len(S) + 0.005
            eta = [20, 11]
            t = 10
            tmax = 25
            wi = [1, 0.85, 0.6, 0.3]
            
            V = [1,2,3]
                
            ######################################################################
            ######################    MODEL   ####################################
            ######################################################################
            
            
            
            model = gp.Model("PartialRateCoverage")
            
            model.setParam('TimeLimit', 60*60)
            
            model._obj = None
            model._bd = None
            model._data = []
            model._start = time.time()
            
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
                        for v in V:
                            y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                                                 name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
             
 
            zfull_vars = {}
            for s in range(len(S)):
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        zfull_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Full "+str(s+1)+str(' ')+str(i))
                    else:
                        zfull_vars[s+1,i] = 0
            
            zpartial1_vars = {}
            for s in range(len(S)):
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        zpartial1_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial1 "+str(s+1)+str(' ')+str(i))
                    else:
                        zpartial1_vars[s+1,i] = 0
            
            zpartial2_vars = {}
            for s in range(len(S)):
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        zpartial2_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial2 "+str(s+1)+str(' ')+str(i))
                    else:
                        zpartial2_vars[s+1,i] = 0
            
            
            zpartial3_vars = {}
            for s in range(len(S)):
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        zpartial3_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial3 "+str(s+1)+str(' ')+str(i))
                    else:
                        zpartial3_vars[s+1,i] = 0
            
            
            gamma_vars = {} ## znull
            for s in range(len(S)):
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                 name="Null "+str(s+1)+str(' ')+str(i))
                    else:
                        gamma_vars[s+1,i] = 0

            obj = gp.LinExpr()
            for s in range(len(S)):
                for i in I:
                    obj += (wi[0]*zfull_vars[s+1,i] + wi[1]*zpartial1_vars[s+1,i] + wi[2]*zpartial2_vars[s+1,i] + wi[3]*zpartial3_vars[s+1,i] - p*gamma_vars[s+1,i]) * (1/len(S))
            model.setObjective(obj, GRB.MAXIMIZE)  
            
            
            # Add constraints
            
            for s in range(len(S)):
                
                for k in K:
                    model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c2")
                
                for l in L:
                    for k in K:
                        if k == 1:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,1,i] for i in I) <= x_vars[l,k], "c3")
                        else:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,2,i] + y_vars[s+1,l,3,i] for i in I) <= x_vars[l,k], "c4")
                            
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,3,i] for l in L) <= S[s][i-1][0], "c5")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,2,i] for l in L) <= S[s][i-1][1], "c6")
                
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L) - (S[s][i-1][0]+S[s][i-1][1]) <= zfull_vars[s+1,i] - 1, "c7")
                
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr((S[s][i-1][0]+S[s][i-1][1])*zfull_vars[s+1,i] <= gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,v,i] for v in V for l in L), "c8")
                
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(2*gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L) - gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,v,i] for v in V for l in L) - (S[s][i-1][0]+S[s][i-1][1]) <= (S[s][i-1][0]+S[s][i-1][1])*zpartial1_vars[s+1,i], "c9" )
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr((S[s][i-1][0]+S[s][i-1][1])*zpartial1_vars[s+1,i] <= gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L), "c_10")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L) - 1 <= (S[s][i-1][0]+S[s][i-1][1])*zpartial2_vars[s+1,i], "c_11")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(zpartial2_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L), "c_12")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L)*zpartial2_vars[s+1,i] <= gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,v,i] for v in V for l in L), "c_13")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L) - gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,v,i] for v in V for l in L) <= (S[s][i-1][0]+S[s][i-1][1])*zpartial3_vars[s+1,i], "c_14")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(zpartial3_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L), "c_15")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(np.amin(cli)*zpartial3_vars[s+1,i] <= gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L) - gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,v,i] for v in V for l in L), "c_16")
                    
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(gp.quicksum(y_vars[s+1,l,v,i] for v in V for l in L) + gamma_vars[s+1,i] >= 1, "c_17")
                        
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(zfull_vars[s+1,i] + zpartial1_vars[s+1,i] + zpartial2_vars[s+1,i] + zpartial3_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_18")
                
                    
                
            # objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
            # objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
            # gap = abs((objbst - objbnd) / objbst)     

            # Optimize model
            model.optimize(callback=data_cb)
            
            end_time = time.time()
            
            elapsed_time = end_time - model._start 
            
            #imprimir variables 
            
            with open('data'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          #+str(len(K))+str('_')
                          #+str(len(N))+str('_')
                          +str(len(S))+'.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(model._data)
                
            
            
            #archivo = xlsxwriter.Workbook('tesis.csv')
            #hoja = archivo.add_worksheet()
            colnames = ["name", "I size", "L size", "S size", "time", "best obj", "best bound", "gap %"]
            for column in range(len(colnames)):
                sheet.write(0, column, colnames[column])
            name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')+str(len(S))
            sheet.write(countcsv, 0, name)
            sheet.write(countcsv, 1, len(I))
            sheet.write(countcsv, 2, len(L))
            sheet.write(countcsv, 3, len(S))
            if len(model._data) != 0:
                datos = model._data[len(model._data)-1]
                for row in range(len(datos)):
                    sheet.write(countcsv, row+4, datos[row])
            countcsv = countcsv + 1
            
            # with open('tesis.csv', 'a') as f:
            #     writer = csv.writer(f)
            #     name = str('Instance')+str(len(I))+str('_')+str(len(L))+str('_')+str(len(S))
            #     f.write(str(name))
            #     f.write('\n')
            #     for row in range(len(model._data[len(model._data)-1])):
            #         f.write(countcsv, row, str(model._data[len(model._data)-1][row]))
            #     countcsv = countcsv + 1 
            
            #Nombre: Resultados_Prueba_I_L_M_N_S
            
            f = open ('Resultados_Prueba_'
                          +str(len(I))+str('_')
                          +str(len(L))+str('_')
                          #+str(len(K))+str('_')
                          #+str(len(N))+str('_')
                          +str(len(S))+'.txt','w')
            
            #f.write("Start time: ")
            #f.write(str(start_time))
            #f.write('\n')
            #f.write("End time: ")
            #f.write(str(end_time))
            #f.write('\n')
        
            f.write("Elapsed time: ")
            f.write(str(elapsed_time))
            f.write('\n')

            # f.write("bst: ")
            # f.write(str(objbst))
            # f.write('\n')
            
            # f.write("bnd: ")
            # f.write(str(objbnd))
            # f.write('\n')
            
            # f.write("Gap: ")
            # f.write(str(gap))
            # f.write('\n')
            
            # f.write("exp 1 ")
            # cur_obj = model.cbGet(gp.GRB.Callback.MIP_OBJBND)
            # f.write(cur_obj)
            # f.write('\n')
            # f.write("exp 2 ")
            # f.write(str(model.cbGet(gp.GRB.Callback.MIP_OBJBND)))
            # f.write('\n')
                    
            f.write('Obj: %g' % model.objVal)
            f.write('\n')
            
            for v in model.getVars():
                f.write('%s %g' % (v.varName, v.x))
                f.write('\n')
            
            #imprimir el valor objetivo
            print('Obj: %g' % model.objVal)
            print("Finished")
            print(" ")
            print(" ")
            
            f.close()
            
#             ########################################
#             # VERIFICANDO SI LA SOLUCION ES FACTIBLE 
#             ########################################
            
#             feasible = open ('Feasible_'
#                           +str(len(I))+str('_')
#                           +str(len(L))+str('_')
#                           +str(len(S))+'.sol','w')
            
#             # Guardando la información de x
#             ambulancesNumber = []
#             for k in K:
#                 conteo = 0
#                 for l in L:
#                     a = x_vars[l,k]
#                     if (a.x != 0):
#                         conteo = conteo + a.x
#                         #print(a.varName, a.x)
#                 ambulancesNumber.append(conteo)
#             #print(ambulancenNumber)
#             #print()
            
            
#             # VERIFICANDO QUE NO SE SOBREPASE LA CANTIDAD DE AMBULANCIAS LOCALIZADAS
#             ambulanceLocation = []
#             for k in K:
#                 if(ambulancesNumber[k-1] == eta[k-1]):
#                     ambulanceLocation.append("equal to eta")
                    
#                 if(ambulancesNumber[k-1] < eta[k-1]):
#                     ambulanceLocation.append("less than eta")
                    
#                 if(ambulancesNumber[k-1] > eta[k-1]):
#                     ambulanceLocation.append("more to eta")
#             #print(ambulanceLocation)
#             #print()
            
#             for k in K:
#                 if(ambulanceLocation[k-1] == 'more than eta'):
#                     feasible.write("MORE AMBULANCE THAN AVAILABLE")
#                     feasible.write("\n")
#                     print("MORE AMBULANCE THAN AVAILABLE")
#                     print()
            
#             # Guardando la información de y
#             dispatches_original = []
#             for s in range(len(S)):
#                 dispatches_original.append([])
#                 for i in I: 
#                     dispatches_original[s].append([])
#                     for k in K: 
#                         conteo = 0
#                         for l in L:
#                             a = y_vars[s+1,l,k,i] 
#                             if (a.x == 1):
#                                 conteo = conteo + 1
#                                 #print("ver si acomoda por i", a, a.x)
#                         dispatches_original[s][i-1].append(conteo)

#             # dispatches_copia = []
#             # for s in range(len(S)):
#             #     dispatches_copia.append([])
#             #     for i in I: 
#             #         dispatches_copia[s].append([])
#             #         for k in K: 
#             #             conteo = 0
#             #             if k == 1:
#             #                 dispatches_copia[s][i-1].append(0)  
#             #             else:
#             #                 for l in L:
#             #                     a = ycopia_vars[s+1,l,2,i] 
#             #                     if (a.x == 1):
#             #                         conteo = conteo + 1
#             #                         #print("ver si acomoda por i", a, a.x)
#             #                 dispatches_copia[s][i-1].append(conteo)         
                        
#             dispatches = []
#             for s in range(len(S)):
#                 dispatches.append([])
#                 for i in I: 
#                     dispatches[s].append([])
#                     for k in K: 
#                         dispatches[s][i-1].append(dispatches_original[s][i-1][k-1])
#             #print(dispatches)
#             #print()
            
        
#             # VERIFICANDO LAS COBERTURAS
#             ###################################
# ##################### CHECAR BIEN ESTO PORQUE NO ESTA BIEN
# ########################################

#             coverage = []
#             for s in range(len(S)):
#                 coverage.append([])
#                 for i in I: 
#                     coverage[s].append([])
#                     for k in K: 
#                         if k == 1:
#                             if S[s][i-1][0] == 0:
#                                 coverage[s][i-1].append("no accident")
                                
#                             if S[s][i-1][0] != 0:
#                                 if dispatches[s][i-1][1] != 0:
#                                     if dispatches[s][i-1][0] + dispatches[s][i-1][1] - S[s][i-1][1] == S[s][i-1][0]:
#                                         coverage[s][i-1].append("full")
#                                 else:
#                                     if dispatches[s][i-1][0] == S[s][i-1][0]:
#                                         coverage[s][i-1].append("full")
                                    
#                                 if dispatches[s][i-1][0] + dispatches[s][i-1][1] - S[s][i-1][1] < S[s][i-1][0] and dispatches[s][i-1][0] + dispatches[s][i-1][1] != 0:
#                                     coverage[s][i-1].append("partial")
                                
#                                 if dispatches[s][i-1][0] + dispatches[s][i-1][1] - S[s][i-1][1] == 0 or dispatches[s][i-1][0] + dispatches[s][i-1][1] == 0:
#                                     coverage[s][i-1].append("null")
                                
#                                 if dispatches[s][i-1][0] + dispatches[s][i-1][1] - S[s][i-1][1] > S[s][i-1][0]:
#                                     coverage[s][i-1].append("over serviced")
                                
#                         if k == 2:
#                             if S[s][i-1][1] == 0:
#                                 coverage[s][i-1].append("no accident")
                                
#                             if S[s][i-1][1] != 0:
#                                 if dispatches[s][i-1][1] == S[s][i-1][1]:
#                                     coverage[s][i-1].append("full")
                                
#                                 if dispatches[s][i-1][1] < S[s][i-1][1] and dispatches[s][i-1][1] != 0:
#                                     coverage[s][i-1].append("partial")
                                
#                                 if dispatches[s][i-1][1] == 0:
#                                     coverage[s][i-1].append("null")
                                    
#                                 if dispatches[s][i-1][1] > S[s][i-1][1]:
#                                     coverage[s][i-1].append("over serviced")
                            
#             #for s in range(len(S)):
#             #    print(coverage[s]) 
#             #print()
            
            
#             # VERIFICANDO QUE NO HAYA SOBRE COBERTURA
#             for s in range(len(S)):
#                 for i in I: 
#                     for k in K:
#                         if (coverage[s][i-1][k-1] == 'over serviced'):
#                             feasible.write("MODEL OVER SERVICED")
#                             feasible.write("\n")
#                             print("MODEL OVER SERVICED")
#                             print()
              
#             # Número de ambulancias despachadas
#             numberDispatched = []
#             for s in range(len(S)):
#                 numberDispatched.append([])
#                 for l in L:
#                     numberDispatched[s].append([])
#                     for k in K:
#                         conteo = 0
#                         for i in I:
#                             a = y_vars[s+1,l,k,i]
#                             if (a.x == 1):
#                                 conteo = conteo + 1
#                         numberDispatched[s][l-1].append(conteo)
                    
#             #print(numberDispatched)
#             #print(" ")
            
#             #Número de ambulancias localizadas 
#             locationQuantity = []
#             for l in L:
#                 locationQuantity.append([])
#                 for k in K:
#                     a = x_vars[l,k]
#                     if(a.x == -0.0):
#                         locationQuantity[l-1].append(0)
#                     else:
#                         locationQuantity[l-1].append(int(a.x))
            
#             #print(locationQuantity)
#             #print(" ")
                    
            
#             # Verificando que se despachen la cantidad de ambulancias que están localizadas
#             feasibleDispatched = []
#             for s in range(len(S)):
#                 feasibleDispatched.append([])
#                 for l in L:
#                     feasibleDispatched[s].append([])
#                     for k in K:
#                         if(numberDispatched[s][l-1][k-1] == locationQuantity[l-1][k-1] and locationQuantity[l-1][k-1] != 0):
#                             feasibleDispatched[s][l-1].append("all used")
                        
#                         if(numberDispatched[s][l-1][k-1] == locationQuantity[l-1][k-1] and locationQuantity[l-1][k-1] == 0):
#                             feasibleDispatched[s][l-1].append("not located")
                        
#                         if(numberDispatched[s][l-1][k-1] < locationQuantity[l-1][k-1] and numberDispatched[s][l-1][k-1] == 0):
#                             feasibleDispatched[s][l-1].append("not used")
                        
#                         if(numberDispatched[s][l-1][k-1] < locationQuantity[l-1][k-1] and numberDispatched[s][l-1][k-1] != 0):
#                             feasibleDispatched[s][l-1].append("not all used")
                            
#                         if(numberDispatched[s][l-1][k-1] > locationQuantity[l-1][k-1]):
#                             feasibleDispatched[s][l-1].append("over used")
#             #print(feasibleDispatched)
#             #print(" ")
                        
#             # VERIFICANDO QUE NO SE DESPACHEN DE MÁS LAS AMBULANCIAS}
#             for s in range(len(S)):
#                 for l in L:
#                     for k in K:
#                          if (feasibleDispatched[s][l-1][k-1] == 'over used'):
#                             feasible.write("MODEL OVER USED")
#                             feasible.write("\n")
#                             print("MODEL OVER USED")
#                             print()
                        
            
             
#             feasible.write("Objective value")
#             feasible.write("\n")
#             feasible.write('%g' % model.objVal)
#             feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.write("Eta")
#             feasible.write("\n")
#             feasible.write(str(eta))
#             feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.write("Ambulance located")
#             feasible.write("\n")
#             feasible.write(str(ambulancesNumber))
#             feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.write("Ambulance location")
#             feasible.write("\n")
#             feasible.write(str(ambulanceLocation))
#             feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.write("Scnenario")
#             feasible.write("\n")
#             for s in range(len(S)):
#                 feasible.write(str(S[s]))
#                 feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.write("Dispatches")
#             feasible.write("\n")
#             for s in range(len(S)):
#                 feasible.write(str(dispatches[s]))
#                 feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.write("Coverage")
#             feasible.write("\n")
#             for s in range(len(S)):
#                 feasible.write(str(coverage[s]))
#                 feasible.write("\n")
#             feasible.write("\n")
            
#             feasible.close()
            
            
            
            model.write('model_'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          #+str(len(K))+str('_')
                          #+str(len(N))+str('_')
                          +str(len(S))+'.lp')
            model.write('model_'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(S))+'.mps')
            
            
            # resultados = open ('Resultados_Prueba_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','r')
            
            # line = resultados.readline()
            
            # # Funcion Objetivo
            
            # fobj = open ('FObj_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','w')
            
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
            #               +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','w')
            
            
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
            #               +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','w')
            
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
            
            # Null
            
            # null = open ('Null_'
            #               +str(len(I))+str('_')
            #               +str(len(L))+str('_')
            #               +str(len(K))+str('_')
            #               +str(len(N))+str('_')
            #               +str(len(S))+str('_')+'_.txt','w')
            
            
            # count = 0
            # for i in range(len(zfull_vars)):
            #     aux = []
            #     line = resultados.readline().strip().split()
            #     if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
            #         count = count + 1
            #         for i in range(len(line)):
            #             if i == 0:
            #                 aux.append(line[i])
            #             else:
            #                 aux.append(int(line[i]))
            #         null.write(str(len_I)+str(' ')
            #                       +str(len_L)+str(' ')
            #                       +str(len_S)+str(' ')
            #                       +str(rep+1)+str(' '))
            #         for j in range(len(aux)):
            #             null.write(str(aux[j])+str(" "))
            #         null.write("\n")
            # if count == 0:
            #     for j in range(9):
            #         null.write("NA"+str(' '))
            
            # null.close()
            
            #resultados.close()
archivo.close()

book.save('Tesis.xls') 
