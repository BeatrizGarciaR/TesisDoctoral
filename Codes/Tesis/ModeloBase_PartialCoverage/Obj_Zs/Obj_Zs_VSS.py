#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 21 15:46:54 2025

@author: BeatrizGarcia
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

import math

# tamaños_I = [168, 270, 500, 900, 1500] #Hasta aquí puede bien el modelo
# tamaños_L = [16, 30, 50, 70, 100]
# tamaños_S = [10, 50, 100, 150, 200]


tamaños_I = [168, 270, 500, 900, 1500]
tamaños_L = [16]
tamaños_S = [50]

K = [1,2]

timelim = 7200 #2 horas 
rates = [0.4]
verif = 0.4

#ambulance = [[10,6], [20,11]]
ambulance = [[35,20]]
t = 10
tmax = 30
wi = [0.65, 0.2, 0.1, 0.05]

countcsv = 1
       
book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('Tesis_ObjZs_Scenarios_210525', cell_overwrite_ok=True)

def data_cb(m, where):
    if where == gp.GRB.Callback.MIPSOL:
        cur_obj = m.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
        cur_bd = m.cbGet(gp.GRB.Callback.MIPSOL_OBJBND)
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



# for iconj in range(len(tamaños_I)):
#     for jconj in range(len(tamaños_L)):
#         for sconj in range(len(tamaños_S)):
#             for k in range(len(ambulance)):
#             #for rep in range(repeticiones):
                
#                 initial_time = time.time()
                
#                 eta = ambulance[k]
    
#                 #Nombre: Instancias_Prueba_I_L_M_N_S_Rep
                
                
#                 archivo = open('Instances_DemandFixed_'
#                           +str(tamaños_I[iconj])+str('_')
#                           +str(tamaños_L[jconj])+str('_')
#                           +str(tamaños_S[sconj])
#                           + '_' + str(verif) + '_'
#                           +'.txt', "r")
                
#                 len_I = int(archivo.readline())
#                 len_L = int(archivo.readline())
#                 len_S = int(archivo.readline())
                
#                 # Sets #
#                 I = []
#                 for i in range(len_I):
#                     I.append(int(i+1))
                    
#                 L = []
#                 for i in range(len_L):
#                     L.append(int(i+1))
                    
#                 Demand = []
#                 for s in range(len_S):
#                     Demand.append([])
#                     line = archivo.readline().strip().split()
#                     for i in range(len_I):
#                         Demand[s].append(int(line[i]))
                
#                 #Scenarios
#                 S = []
#                 TotalAccidentes = 0
#                 auxI = [0, 0]
#                 for l in range(len_S):
#                     count = 0
#                     line = archivo.readline().strip().split()
#                     #print("line", line)
#                     S.append([])
#                     for i in range(len(I)):
#                         #print("line[i]", line[count])
#                         #print("line[i]", line)
#                         S[l].append([])
#                         for k in range(len(K)):
#                             #print("line[count]", line[count])
#                             S[l][i].append(int(line[count]))
#                             if k == 0:
#                                 auxI[0] = int(line[count])
#                             else:
#                                 auxI[1] = int(line[count])
#                             if count < len(line)-1:
#                                 count += 1
#                         if any(auxI):
#                             TotalAccidentes += 1
#                             #S[l][i].append(int(line[i+1]))
                            
#                 #Response times
#                 r_li = []
#                 for l in range(len(L)):
#                     line = archivo.readline().strip().split()
#                     r_li.append([])
#                     for i in range(len(I)):
#                         r_li[l].append(int(line[i]))   
                    
                     
#                 cli = []
#                 for l in range(len(L)):
#                     line = archivo.readline().strip().split()
#                     cli.append([])
#                     for i in range(len(I)):
#                         cli[l].append(float(line[i])) 
                
                
#                 # Other parameters #
#                 #pi = 100
#                 pi = np.amax(cli)/len(S) + 0.005
#                 V = [1,2]
                            
#                 ########################################
#                 ############# agregado para promediar S
#                 ###########################################
                
#                 escenario_nuevo = []
                
#                 for i in range(len(I)):
#                     escenario_nuevo.append([])
                    
#                     suma = 0
#                     for s in range(len_S):
#                         suma = suma + S[s][i][0]
#                     prom = suma/len_S
#                     escenario_nuevo[i].append(math.ceil(prom))
                    
#                     suma = 0
#                     for s in range(len_S):
#                         suma = suma + S[s][i][1]
#                     prom = suma/len_S
#                     escenario_nuevo[i].append(math.ceil(prom))
                
#                 print(escenario_nuevo)
                
#                 S = [escenario_nuevo]
                
#                 #break                   

                    
#                 ######################################################################
#                 ######################    MODEL   ####################################
#                 ######################################################################
                
#                 presolve = 0
        
#                 model = gp.Model("PartialRateCoverage")
                
#                 model.setParam('TimeLimit', timelim)
                
#                 model._obj = None
#                 model._bd = None
#                 model._data = []
#                 model._start = time.time()
                
#                 # Create variables #
#                 x_vars = {}
#                 cantVarX = 0
#                 for l in L:
#                     for k in K:
#                         x_vars[l,k] = model.addVar(vtype=GRB.INTEGER, 
#                                          name="located "+str(l)+str(' ')+str(k))
#                         cantVarX += 1
                        
                        
#                 y_vars = {}    
#                 cantVarY = 0
#                 for s in range(1):        
#                     for l in L:
#                         for i in I:
#                             if S[s][i-1][0] != 0:
#                                 y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
#                                                 name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
#                                 cantVarY += 1
                                
#                                 y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
#                                                 name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
#                                 cantVarY += 1
                                
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
#                                                 name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
#                                 cantVarY += 1
    
                
#                 alpha_vars = {}  ## z full
#                 cantVarAlpha = 0
#                 for s in range(1):
#                     for i in I:
#                         if (S[s][i-1][0] + S[s][i-1][1]) > 0:
#                             #alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, ub=0, 
#                             alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY,                                  
#                                                            name="Full "+str(s+1)+str(' ')+str(i))
#                             cantVarAlpha += 1
                            
                
#                 beta_vars = {}  ## z partial 1
#                 cantVarBeta = 0
#                 for s in range(1):
#                     for i in I:
#                         if (S[s][i-1][0] + S[s][i-1][1]) > 0:
#                             beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
#                                                       name="Partial1 "+str(s+1)+str(' ')+str(i))
#                             cantVarBeta += 1
                            
                
#                 delta_vars = {}  ## z partial 2
#                 cantVarDelta = 0
#                 for s in range(1):
#                     for i in I:
#                         if (S[s][i-1][0] + S[s][i-1][1]) > 0:
#                             #delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, ub = 0,
#                             delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
#                                                       name="Partial2 "+str(s+1)+str(' ')+str(i))
#                             cantVarDelta += 1
                       
                
#                 phi_vars = {}   ## z partial 3
#                 cantVarPhi = 0
#                 for s in range(1):
#                     for i in I:
#                         if (S[s][i-1][0] + S[s][i-1][1]) > 0:
#                             #phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, ub=0, 
#                             phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY,
#                                                       name="Partial3 "+str(s+1)+str(' ')+str(i))
#                             cantVarPhi += 1
                       
                
#                 gamma_vars = {} ## z null
#                 cantVarGamma = 0
#                 for s in range(1):
#                     for i in I:
#                         if (S[s][i-1][0] + S[s][i-1][1]) > 0:
#                             gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY,  
#                                                      name="Null "+str(s+1)+str(' ')+str(i))
#                             cantVarGamma += 1
                       
                            
#                 obj = gp.LinExpr()
#                 for s in range(1):
#                     for i in I:
#                         if (S[s][i-1][0] + S[s][i-1][1]) > 0:
#                             #obj += 0
#                             obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/1)
#                 model.setObjective(obj, GRB.MAXIMIZE)  
    
                
#                 # Add constraints
                
#                 for s in range(1):
                    
#                     # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
#                     for k in K:
#                         model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                    
#                     # Restricción 4: No enviar más ambulancias de las localizadas para k = 1
                    
#                     for l in L:
#                         amb1 = gp.LinExpr()
#                         for i in I:
#                             if S[s][i-1][0] != 0:                            
#                                 amb1 += y_vars[s+1,l,1,i]
#                         model.addConstr(amb1 <= x_vars[l,1], "c4")
                    
#                     # Restricción 4_1: No enviar más ambulancias de las localizadas para k = 2
                    
#                     for l in L:
#                         amb2 = gp.LinExpr()
#                         for i in I:
#                             if S[s][i-1][0] != 0:
#                                 amb2 += y_vars[s+1,l,2,i] 
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 amb2 += y_vars[s+1,l,2,i] 
#                         model.addConstr(amb2 <= x_vars[l,2], "c4_1")
                        
                    
#                     # # Restricción 5: Desactivar alpha (cobertura total)
                    
#                     # for i in I:
#                     #     suma_alpha2 = gp.LinExpr()
#                     #     if S[s][i-1][0] + S[s][i-1][1] > 0:
#                     #         if S[s][i-1][0] != 0:
#                     #             suma_alpha2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                     #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                     #             suma_alpha2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                     #         model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma_alpha2, "c5")
                    
                    
#                     # Restricción 6: Desactivar alpha (cobertura total)
                    
#                     for i in I:
#                         suma_alpha2 = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_alpha2 += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_alpha2 += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma_alpha2, "c6")
                    
                    
#                     # # Restricción 6: Activar alpha (cobertura total) 
#                     # suma_alpha = gp.LinExpr()
#                     # for i in I: 
#                     #     if S[s][i-1][0] + S[s][i-1][1] > 0:
#                     #         if S[s][i-1][0] != 0:
#                     #             suma_alpha += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i]  for l in L) 
#                     #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                     #             suma_alpha += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i]  for l in L) 
#                     #         model.addConstr(suma_alpha - (S[s][i-1][0]+S[s][i-1][1]) <= alpha_vars[s+1,i] - 1, "c6")
    
                    
    
#                     # Restricción 7: Desactivar beta (cobertura parcial 1)
                    
#                     for i in I:
#                         suma_beta2 = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_beta2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_beta2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma_beta2, "c7")
                            
                            
                            
#                     # Restricción 8: Desactivar beta (cobertura parcial 1)
                    
#                     for i in I:
#                         suma_beta = gp.LinExpr()
#                         suma_beta_aux = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_beta += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                                 suma_beta_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_beta += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                                 suma_beta_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr(beta_vars[s+1,i] <= 100000000*(suma_beta - suma_beta_aux), "c8" )
           
                    
           
#                     # Restricción 9: Desactivar delta (cobertura parcial 2)
                    
#                     for i in I:
#                         suma_delta2 = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_delta2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_delta2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr(delta_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma_delta2, "c_9")
                           
                                
                        
#                     # # Restricción 10: Activar delta (cobertura parcial 2)
#                     # suma_delta = gp.LinExpr()
#                     # for i in I:
#                     #     if S[s][i-1][0] + S[s][i-1][1] > 0:
#                     #         if S[s][i-1][0] != 0:
#                     #             suma_delta += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                     #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                     #             suma_delta += gp.quicksum(y_vars[s+1,l,2,i] for l in L) 
#                     #         model.addConstr(suma_delta - 1 <= (S[s][i-1][0]+S[s][i-1][1])*delta_vars[s+1,i], "c_10")
                       
                              
#                     # Restricción 10: Desactivar delta (cobertura parcial 2)   
                    
#                     for i in I:
#                         suma_delta3 = gp.LinExpr()
#                         suma_delta3_aux = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_delta3 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                                 suma_delta3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0  and S[s][i-1][0] == 0:
#                                 suma_delta3 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                                 suma_delta3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr(suma_delta3*delta_vars[s+1,i] <= suma_delta3_aux, "c_10")
                            
                    
#                     # Restricción 11: Desactivar phi (cobertura parcial 3)
                    
#                     for i in I:
#                         suma_phi2 = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_phi2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_phi2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr(phi_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma_phi2, "c_11")
                       
                            
#                     # # Restricción 13: Activar phi (cobertura parcial 3)
#                     # suma_phi = gp.LinExpr()
#                     # suma_phi_aux = gp.LinExpr()
#                     # for i in I:
#                     #     if S[s][i-1][0] + S[s][i-1][1] > 0:
#                     #         if S[s][i-1][0] != 0:
#                     #             suma_phi += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                     #             suma_phi_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                     #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                     #             suma_phi += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                     #             suma_phi_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)               
#                     #         model.addConstr(suma_phi - suma_phi_aux <= (S[s][i-1][0]+S[s][i-1][1])*phi_vars[s+1,i], "c_13")
                      
                    
               
#                     # Restricción 12: Desactivar phi (cobertura parcial 3)
                    
#                     for i in I:
#                         suma_phi3 = gp.LinExpr()
#                         suma_phi3_aux = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_phi3 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                                 suma_phi3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_phi3 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                                 suma_phi3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr(phi_vars[s+1,i] <= 1000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                    
#                     # Restricción 13: Activar gamma (cobertura nula)
                    
#                     for i in I:
#                         suma_gamma = gp.LinExpr()
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             if S[s][i-1][0] != 0:
#                                 suma_gamma += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
#                             if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
#                                 suma_gamma += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
#                             model.addConstr(suma_gamma + gamma_vars[s+1,i] >= 1, "c_13")
                            
#                     #Restricción 14: Solo se puede activar un tipo de cobertura     
#                     for i in I:
#                         if S[s][i-1][0] + S[s][i-1][1] > 0:
#                             model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_14")
                    
                    
#                 # objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
#                 # objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
#                 # gap = abs((objbst - objbnd) / objbst)     
    
#                 # Optimize model
#                 model.optimize(callback=data_cb)
                
#                 end_time = time.time()
                
#                 elapsed_time = end_time - model._start 
                
#                 #imprimir variables 
                
#                 with open('data_ObjZs_Scenarios_210525_'+str(len(I))+str('_')
#                               +str(len(L))+str('_')
#                               #+str(len(K))+str('_')
#                               #+str(len(N))+str('_')
#                               +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
#                     writer = csv.writer(f)
#                     writer.writerows(model._data)
                    
                
                
#                 # #archivo = xlsxwriter.Workbook('tesis.csv')
#                 # #hoja = archivo.add_worksheet()
#                 # colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
#                 # for column in range(len(colnames)):
#                 #     sheet.write(0, column, colnames[column])
#                 # name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
#                 # sheet.write(countcsv, 0, name)
#                 # sheet.write(countcsv, 1, len(I))
#                 # sheet.write(countcsv, 2, len(L))
#                 # sheet.write(countcsv, 3, 1)
#                 # if len(model._data) != 0:
#                 #     datos = model._data[len(model._data)-1]
#                 #     for row in range(len(datos)):
#                 #         sheet.write(countcsv, row+4, datos[row])
                
                
#                 # with open('tesis.csv', 'a') as f:
#                 #     writer = csv.writer(f)
#                 #     name = str('Instance')+str(len(I))+str('_')+str(len(L))+str('_')+str(1)
#                 #     f.write(str(name))
#                 #     f.write('\n')
#                 #     for row in range(len(model._data[len(model._data)-1])):
#                 #         f.write(countcsv, row, str(model._data[len(model._data)-1][row]))
#                 #     countcsv = countcsv + 1 
                
#                 #Nombre: Resultados_I_L_M_N_S
                
#                 f = open ('Resultados_Prueba_ObjZs_Scenarios_210525_'
#                               +str(len(I))+str('_')
#                               +str(len(L))+str('_')
#                               #+str(len(K))+str('_')
#                               #+str(len(N))+str('_')
#                               +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
#                 #f.write("Start time: ")
#                 #f.write(str(start_time))
#                 #f.write('\n')
#                 #f.write("End time: ")
#                 #f.write(str(end_time))
#                 #f.write('\n')
            
#                 f.write("Elapsed time: ")
#                 f.write(str(elapsed_time))
#                 f.write('\n')
    
#                 # f.write("bst: ")
#                 # f.write(str(objbst))
#                 # f.write('\n')
                
#                 # f.write("bnd: ")
#                 # f.write(str(objbnd))
#                 # f.write('\n')
                
#                 # f.write("Gap: ")
#                 # f.write(str(gap))
#                 # f.write('\n')
                
#                 # f.write("exp 1 ")
#                 # cur_obj = model.cbGet(gp.GRB.Callback.MIP_OBJBND)
#                 # f.write(cur_obj)
#                 # f.write('\n')
#                 # f.write("exp 2 ")
#                 # f.write(str(model.cbGet(gp.GRB.Callback.MIP_OBJBND)))
#                 # f.write('\n')
                        
#                 f.write('Obj: %g' % model.objVal)
#                 f.write('\n')
                
#                 if model.objVal != float("-inf"):
#                     for v in model.getVars():
#                         f.write('%s %g' % (v.varName, v.x))
#                         f.write('\n')
                
#                 #imprimir el valor objetivo
#                 print('Obj: %g' % model.objVal)
#                 print("Finished")
#                 print(" ")
#                 print(" ")
                
#                 f.close()
                
                
#                 end_time = time.time()
#                 total_time = end_time - initial_time 
                
#                 #sheet.write(countcsv, 9, total_time)
                
#                 #countcsv = countcsv + 1
                
                

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            for k in range(len(ambulance)):
            #for rep in range(repeticiones):
                
                eta = ambulance[k]

                # archivo = open('Resultados_Prueba_ObjZs_Scenarios__Modif_121024_'
                #           +str(tamaños_I[iconj])+str('_')
                #           +str(tamaños_L[jconj])+str('_')
                #           +str(tamaños_S[sconj])
                #           +'_'+str(eta[0])+'_'+str(eta[1])
                #           +'.txt', "r")

                archivo = open('Resultados_Prueba_ObjZs_Scenarios_210525_'
                          +str(tamaños_I[iconj])+str('_')
                          +str(tamaños_L[jconj])+str('_')
                          +str(tamaños_S[sconj])
                          +'_'+str(eta[0])+'_'+str(eta[1])
                          +'.txt', "r")
                
                line = archivo.readline().strip().split()
                line = archivo.readline().strip().split()
                
                f = open ('Location_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                for i in range(tamaños_L[jconj]*2):
                    line = archivo.readline()
                    f.write(line)
                    
                f.close()
                
                
                line = archivo.readline()
                g = open ('Dispatch_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while len(line) > 15:
                    g.write(line)
                    line = archivo.readline()
                        
                g.close()
                
                line = archivo.readline()
                
                #print(line)
                count_assigned = 0
                h = open ('Full_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Full" in line:
                    h.write(line)
                    line = archivo.readline()
                    if line != '':
                        if line[len(line)-2] == '1':
                            count_assigned = count_assigned + 1
                        
                h.close()
                
                line = archivo.readline()
                
                o = open ('Partial1_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Partial1" in line:
                    o.write(line)
                    line = archivo.readline()
                        
                o.close()
                
                line = archivo.readline()
                
                p = open ('Partial2_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Partial2" in line:
                    p.write(line)
                    line = archivo.readline()
                        
                p.close()
                
                line = archivo.readline()
                
                q = open ('Partial3_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Partial3" in line:
                    q.write(line)
                    line = archivo.readline()
                        
                q.close()
                    
                line = archivo.readline()
                
                count_notassigned = 0
                r = open ('Null_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Null" in line:
                    r.write(line)
                    line = archivo.readline()
                    if line != '':
                        if line[len(line)-2] == '1':
                            count_notassigned = count_notassigned + 1
                        
                r.close()
                
                print("new", tamaños_I[iconj], " ", tamaños_L[jconj], " ", tamaños_S[sconj])
                print("assigned = ", count_assigned/tamaños_S[sconj])
                print("not assigned = ", count_notassigned/tamaños_S[sconj])
                print("\n")
                
                # verif=0.4
                h = open('Instances_DemandFixed_'
                          +str(tamaños_I[iconj])+str('_')
                          +str(tamaños_L[jconj])+str('_')
                          +str(tamaños_S[sconj])
                          + '_' + str(verif) + '_'
                          +'.txt', "r")
                
                line_1 = h.readline()
                line_1 = h.readline()
                line_1 = h.readline()
                
                for cant in range(tamaños_S[sconj]):
                    line_1 = h.readline()
                
                
                un = open ('ScAccidents_ObjZs_Scenarios__Modif_121024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'.txt','w')
                
                u = open ('Accidents_ObjZs_Scenarios__Modif_121024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'.txt','w')
                        
                
                accidentes = []
                for cant in range(tamaños_S[sconj]):
                    line_1 = h.readline().strip().split()
                    un.write(str(line_1))
                    accident = 0
                    total_accidents = 0
                    for a in range(tamaños_I[iconj]):
                        if int(line_1[accident])!=0 or int(line_1[accident+1])!=0:
                            total_accidents += 1 
                        accident += 2
                    accidentes.append(total_accidents)
                    u.write(str(total_accidents))
                    u.write(' ')
                
                u.close()
                    
                un.close()
                
                
                initial_time = time.time()
                
                eta = ambulance[k]
    
                #Nombre: Instancias_Prueba_I_L_M_N_S_Rep
                
                
                archivo = open('Instances_DemandFixed_'
                          +str(tamaños_I[iconj])+str('_')
                          +str(tamaños_L[jconj])+str('_')
                          +str(tamaños_S[sconj])
                          + '_' + str(verif) + '_'
                          +'.txt', "r")
                
                len_I = int(archivo.readline())
                len_L = int(archivo.readline())
                len_S = int(archivo.readline())
                
                # Sets #
                I = []
                for i in range(len_I):
                    I.append(int(i+1))
                    
                L = []
                for i in range(len_L):
                    L.append(int(i+1))
                    
                Demand = []
                for s in range(len_S):
                    Demand.append([])
                    line = archivo.readline().strip().split()
                    for i in range(len_I):
                        Demand[s].append(int(line[i]))
                
                #Scenarios
                S = []
                TotalAccidentes = 0
                auxI = [0, 0]
                for l in range(len_S):
                    count = 0
                    line = archivo.readline().strip().split()
                    #print("line", line)
                    S.append([])
                    for i in range(len(I)):
                        #print("line[i]", line[count])
                        #print("line[i]", line)
                        S[l].append([])
                        for k in range(len(K)):
                            #print("line[count]", line[count])
                            S[l][i].append(int(line[count]))
                            if k == 0:
                                auxI[0] = int(line[count])
                            else:
                                auxI[1] = int(line[count])
                            if count < len(line)-1:
                                count += 1
                        if any(auxI):
                            TotalAccidentes += 1
                            #S[l][i].append(int(line[i+1]))
                            
                #Response times
                r_li = []
                for l in range(len(L)):
                    line = archivo.readline().strip().split()
                    r_li.append([])
                    for i in range(len(I)):
                        r_li[l].append(int(line[i]))   
                    
                     
                cli = []
                for l in range(len(L)):
                    line = archivo.readline().strip().split()
                    cli.append([])
                    for i in range(len(I)):
                        cli[l].append(float(line[i])) 
                
                
                # Other parameters #
                #pi = 100
                pi = np.amax(cli)/len(S) + 0.005
                V = [1,2]
                
                
                ######################################################################
                ######################    MODEL   ####################################
                ######################################################################
                
                presolve = 0
        
                model = gp.Model("PartialRateCoverage")
                
                model.setParam('TimeLimit', timelim)
                
                model._obj = None
                model._bd = None
                model._data = []
                model._start = time.time()
                
                g = open('Location_ObjZs_210525_'
                         +str(tamaños_I[iconj])+str('_')
                         +str(tamaños_L[jconj])+str('_')
                         +str(tamaños_S[sconj])+'_'
                         +str(eta[0])+'_'+str(eta[1])+'.txt')
            
                
                
                # Create variables #
                x_vars = {}
                cantVarX = 0
                for l in L:
                    for k in K:
                        line = g.readline().strip().split()
                        #print(line)
                        #x_vars[l,k] = model.addVar(name="located "+str(l)+str(' ')+str(k))
                        #print(int(line[len(line)-1]))
                        x_vars[l,k] = int(line[len(line)-1])
                        #print(x_vars[l,k])
                        cantVarX += 1
                        
                
                g.close()
                        
                        
                y_vars = {}    
                cantVarY = 0
                for s in range(len(S)):        
                    for l in L:
                        for i in I:
                            if S[s][i-1][0] != 0:
                                y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                cantVarY += 1
                                
                                y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                cantVarY += 1
                                
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                cantVarY += 1
    
                
                alpha_vars = {}  ## z full
                cantVarAlpha = 0
                for s in range(len(S)):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            #alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, ub=0, 
                            alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY,                                  
                                                           name="Full "+str(s+1)+str(' ')+str(i))
                            cantVarAlpha += 1
                            
                
                beta_vars = {}  ## z partial 1
                cantVarBeta = 0
                for s in range(len(S)):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial1 "+str(s+1)+str(' ')+str(i))
                            cantVarBeta += 1
                            
                
                delta_vars = {}  ## z partial 2
                cantVarDelta = 0
                for s in range(len(S)):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            #delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, ub = 0,
                            delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial2 "+str(s+1)+str(' ')+str(i))
                            cantVarDelta += 1
                       
                
                phi_vars = {}   ## z partial 3
                cantVarPhi = 0
                for s in range(len(S)):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            #phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, ub=0, 
                            phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY,
                                                      name="Partial3 "+str(s+1)+str(' ')+str(i))
                            cantVarPhi += 1
                       
                
                gamma_vars = {} ## z null
                cantVarGamma = 0
                for s in range(len(S)):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY,  
                                                     name="Null "+str(s+1)+str(' ')+str(i))
                            cantVarGamma += 1
                       
                            
                obj = gp.LinExpr()
                for s in range(1):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            #obj += 0
                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/1)
                model.setObjective(obj, GRB.MAXIMIZE)  
    
                
                # Add constraints
                
                for s in range(1):
                    
                    # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                    for k in K:
                        model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                    
                    # Restricción 4: No enviar más ambulancias de las localizadas para k = 1
                    
                    for l in L:
                        amb1 = gp.LinExpr()
                        for i in I:
                            if S[s][i-1][0] != 0:                            
                                amb1 += y_vars[s+1,l,1,i]
                        model.addConstr(amb1 <= x_vars[l,1], "c4")
                    
                    # Restricción 4_1: No enviar más ambulancias de las localizadas para k = 2
                    
                    for l in L:
                        amb2 = gp.LinExpr()
                        for i in I:
                            if S[s][i-1][0] != 0:
                                amb2 += y_vars[s+1,l,2,i] 
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                amb2 += y_vars[s+1,l,2,i] 
                        model.addConstr(amb2 <= x_vars[l,2], "c4_1")
                        
                    
                    # # Restricción 5: Desactivar alpha (cobertura total)
                    
                    # for i in I:
                    #     suma_alpha2 = gp.LinExpr()
                    #     if S[s][i-1][0] + S[s][i-1][1] > 0:
                    #         if S[s][i-1][0] != 0:
                    #             suma_alpha2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                    #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                    #             suma_alpha2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                    #         model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma_alpha2, "c5")
                    
                    
                    # Restricción 6: Desactivar alpha (cobertura total)
                    
                    for i in I:
                        suma_alpha2 = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_alpha2 += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_alpha2 += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma_alpha2, "c6")
                    
                    
                    # # Restricción 6: Activar alpha (cobertura total) 
                    # suma_alpha = gp.LinExpr()
                    # for i in I: 
                    #     if S[s][i-1][0] + S[s][i-1][1] > 0:
                    #         if S[s][i-1][0] != 0:
                    #             suma_alpha += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i]  for l in L) 
                    #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                    #             suma_alpha += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i]  for l in L) 
                    #         model.addConstr(suma_alpha - (S[s][i-1][0]+S[s][i-1][1]) <= alpha_vars[s+1,i] - 1, "c6")
    
                    
    
                    # Restricción 7: Desactivar beta (cobertura parcial 1)
                    
                    for i in I:
                        suma_beta2 = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_beta2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_beta2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma_beta2, "c7")
                            
                            
                            
                    # Restricción 8: Desactivar beta (cobertura parcial 1)
                    
                    for i in I:
                        suma_beta = gp.LinExpr()
                        suma_beta_aux = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_beta += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                                suma_beta_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_beta += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                                suma_beta_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(beta_vars[s+1,i] <= 100000000*(suma_beta - suma_beta_aux), "c8" )
           
                    
           
                    # Restricción 9: Desactivar delta (cobertura parcial 2)
                    
                    for i in I:
                        suma_delta2 = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_delta2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_delta2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(delta_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma_delta2, "c_9")
                           
                                
                        
                    # # Restricción 10: Activar delta (cobertura parcial 2)
                    # suma_delta = gp.LinExpr()
                    # for i in I:
                    #     if S[s][i-1][0] + S[s][i-1][1] > 0:
                    #         if S[s][i-1][0] != 0:
                    #             suma_delta += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                    #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                    #             suma_delta += gp.quicksum(y_vars[s+1,l,2,i] for l in L) 
                    #         model.addConstr(suma_delta - 1 <= (S[s][i-1][0]+S[s][i-1][1])*delta_vars[s+1,i], "c_10")
                       
                              
                    # Restricción 10: Desactivar delta (cobertura parcial 2)   
                    
                    for i in I:
                        suma_delta3 = gp.LinExpr()
                        suma_delta3_aux = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_delta3 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                                suma_delta3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0  and S[s][i-1][0] == 0:
                                suma_delta3 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                                suma_delta3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(suma_delta3*delta_vars[s+1,i] <= suma_delta3_aux, "c_10")
                            
                    
                    # Restricción 11: Desactivar phi (cobertura parcial 3)
                    
                    for i in I:
                        suma_phi2 = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_phi2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_phi2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(phi_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma_phi2, "c_11")
                       
                            
                    # # Restricción 13: Activar phi (cobertura parcial 3)
                    # suma_phi = gp.LinExpr()
                    # suma_phi_aux = gp.LinExpr()
                    # for i in I:
                    #     if S[s][i-1][0] + S[s][i-1][1] > 0:
                    #         if S[s][i-1][0] != 0:
                    #             suma_phi += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                    #             suma_phi_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                    #         if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                    #             suma_phi += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                    #             suma_phi_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)               
                    #         model.addConstr(suma_phi - suma_phi_aux <= (S[s][i-1][0]+S[s][i-1][1])*phi_vars[s+1,i], "c_13")
                      
                    
               
                    # Restricción 12: Desactivar phi (cobertura parcial 3)
                    
                    for i in I:
                        suma_phi3 = gp.LinExpr()
                        suma_phi3_aux = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_phi3 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                                suma_phi3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_phi3 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                                suma_phi3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(phi_vars[s+1,i] <= 1000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                    
                    # Restricción 13: Activar gamma (cobertura nula)
                    
                    for i in I:
                        suma_gamma = gp.LinExpr()
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_gamma += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_gamma += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(suma_gamma + gamma_vars[s+1,i] >= 1, "c_13")
                            
                    #Restricción 14: Solo se puede activar un tipo de cobertura     
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_14")
                    
                    
                
                # Optimize model
                model.optimize(callback=data_cb)
                
                end_time = time.time()
                
                elapsed_time = end_time - model._start 
                
                #imprimir variables 
                
                with open('data_ObjZs_210525_'+str(len(I))+str('_')
                              +str(len(L))+str('_')
                              #+str(len(K))+str('_')
                              #+str(len(N))+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(model._data)
                    
                
                
                #archivo = xlsxwriter.Workbook('tesis.csv')
                #hoja = archivo.add_worksheet()
                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                for column in range(len(colnames)):
                    sheet.write(0, column, colnames[column])
                    #sheet1.write(0, column, colnames[column])
                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                sheet.write(countcsv, 0, name)
                #sheet1.write(countcsv1, 0, name)
                sheet.write(countcsv, 1, len(I))
                #sheet1.write(countcsv1, 1, len(I))
                sheet.write(countcsv, 2, len(L))
                #sheet1.write(countcsv1, 2, len(L))
                sheet.write(countcsv, 3, len(S))
                #sheet1.write(countcsv1, 3, len(S))
                if len(model._data) != 0:
                    datos = model._data[len(model._data)-1]
                    for row in range(len(datos)):
                        sheet.write(countcsv, row+4, datos[row])
                        #sheet1.write(countcsv1, row+4, datos[row])
                
                
                #Nombre: Resultados_I_L_M_N_S
                
                f = open ('Resultados_ObjZs_210525_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(len(L))+str('_')
                              #+str(len(K))+str('_')
                              #+str(len(N))+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
  
            
                f.write("Elapsed time: ")
                f.write(str(elapsed_time))
                f.write('\n')
    
                        
                f.write('Obj: %g' % model.objVal)
                f.write('\n')
                
                for l in L:
                    for k in K:
                        f.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars[l,k]))
                        f.write('\n')
                f.write('-1')
                f.write('\n')
                
                names = ['dispatched', 'Full', 'Partial1', 'Partial2', 'Partial3', 'Null']
                name_ind = 0
                new_name = names[name_ind]
                
                
                if model.objVal != float("-inf"):
                    for v in model.getVars():
                        # if new_name == 'located':
                        #     print(str(v) + '\n')
                        #     print('%s %g' % (v.varName, v.x))
                        if new_name not in v.varName:
                            #print("entra new name \n")
                            #print(new_name+'\n')
                            f.write('-1')
                            f.write('\n')
                            name_ind = name_ind + 1
                            new_name = names[name_ind]
                        f.write('%s %g' % (v.varName, v.x))
                        f.write('\n')
                    
                f.write('-1')
                    
                
                #imprimir el valor objetivo
                print('Obj: %g' % model.objVal)
                print("Finished")
                print(" ")
                print(" ")
                
                f.close()
                
                
                end_time = time.time()
                total_time = end_time - initial_time 
                
                sheet.write(countcsv, 9, total_time)
                #sheet1.write(countcsv1, 9, total_time)
                
                countcsv = countcsv + 1
                #countcsv1 = countcsv1 + 1
                
                
                book.save('Tesis_ObjZs_Scenarios_210525_'+str(eta[0])+'_'+str(eta[1])+'.xls') 
