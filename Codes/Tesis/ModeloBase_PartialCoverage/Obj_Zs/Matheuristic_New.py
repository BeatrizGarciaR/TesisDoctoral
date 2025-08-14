#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 08:43:14 2025

@author: BeatrizGarcia
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:05:18 2024

@author: beatr
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:13:46 2024

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
import math
import xlwt

# tamaños_I = [168, 270, 500, 900, 1500] #Hasta aquí puede bien el modelo
# tamaños_L = [16, 30, 50, 70, 100]
# tamaños_S = [10, 50, 100, 150, 200]

tamaños_I = [1500] 
tamaños_L = [100]
tamaños_S = [10, 50, 100, 150, 200]

# tamaños_I = [168, 270, 500, 900, 1500] 
# tamaños_L = [16, 50, 100]
# tamaños_S = [10, 50, 100, 150, 200]

# tamaños_I = [270]
# tamaños_L = [16]
# tamaños_S = [100]

K = [1,2]
rates = [0.4]
verif = 0.4
sale = 1

#ambulance = [[10, 6], [20,11], [35,20]]
ambulance = [[35,20]]
t = 10
tmax = 30
wi = [0.65, 0.2, 0.1, 0.05]

countcsv = 1
countcsv1 = 1

timelim = 600 #10 min
time_limit_final = 3600 #60 min
time_limit_ls = 3600 # 60 min
#num_iteraciones = 20


##############################################
######## INSTANCIAS ORIGINALES (YA LOCALIZADO)
##############################################
       
book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('Tesis_Matheuristic_230325', cell_overwrite_ok=True)

book1 = xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet1 = book1.add_sheet('Tesis_Matheuristic1_230325', cell_overwrite_ok=True)

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



for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            for k in range(len(ambulance)):
            #for rep in range(repeticiones):
                
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
                #break                   
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
                
                g = open('Location_Obj_NewModel_Supuesto_280224_'
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
                for s in range(len(S)):
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                            #obj += 0
                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                model.setObjective(obj, GRB.MAXIMIZE)  
    
                
                # Add constraints
                
                for s in range(len(S)):
                    
                    # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                    # for k in K:
                    #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                    
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
                    # suma_alpha2 = gp.LinExpr()
                    # for i in I:
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
                            model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                    
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
                
                with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                              +str(len(L))+str('_')
                              #+str(len(K))+str('_')
                              #+str(len(N))+str('_')
                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(model._data)
                    
                
                
                #archivo = xlsxwriter.Workbook('tesis.csv')
                #hoja = archivo.add_worksheet()
                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time", "iteration"]
                for column in range(len(colnames)):
                    sheet.write(0, column, colnames[column])
                    sheet1.write(0, column, colnames[column])
                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                sheet.write(countcsv, 0, name)
                sheet1.write(countcsv1, 0, name)
                sheet.write(countcsv, 1, len(I))
                sheet1.write(countcsv1, 1, len(I))
                sheet.write(countcsv, 2, len(L))
                sheet1.write(countcsv1, 2, len(L))
                sheet.write(countcsv, 3, len(S))
                sheet1.write(countcsv1, 3, len(S))
                if len(model._data) != 0:
                    datos = model._data[len(model._data)-1]
                    for row in range(len(datos)):
                        sheet.write(countcsv, row+4, datos[row])
                        sheet1.write(countcsv1, row+4, datos[row])
                
                
                #Nombre: Resultados_I_L_M_N_S
                
                f = open ('Resultados_Matheuristic_230325_'
                              +str(len(I))+str('_')
                              +str(len(L))+str('_')
                              #+str(len(K))+str('_')
                              #+str(len(N))+str('_')
                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
  
            
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
                sheet1.write(countcsv1, 9, total_time)
                
                sheet.write(countcsv, 10, 0)
                sheet1.write(countcsv1, 10, 0)
                
                
                countcsv = countcsv + 1
                countcsv1 = countcsv1 + 1
                
                
                #book.save('Tesis_Matheuristic_230325_'+str(eta[0])+'_'+str(eta[1])+'.xls') 
                
                mejor = open('Best_Matheuristic_230325_'
                                  +str(tamaños_I[iconj])+str('_')
                                  +str(tamaños_L[jconj])+str('_')
                                  +str(tamaños_S[sconj])+'_'
                                  +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                
                mejor.write('Obj: %g' % model.objVal)
                mejor.write('\n')
                
                for l in L:
                    for k in K:
                        mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars[l,k]))
                        mejor.write('\n')
                mejor.write('-1')
                mejor.write('\n')
                
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
                            mejor.write('-1')
                            mejor.write('\n')
                            name_ind = name_ind + 1
                            new_name = names[name_ind]
                        mejor.write('%s %g' % (v.varName, v.x))
                        mejor.write('\n')
                    
                mejor.write('-1')
                
                mejor.close()
                
                
                mejor_obj = model.objVal
 
                ############################################################
                ###### VECINDARIO DE CAMBIOS ENTRE ACTIVOS Y ACTIVOS (BLS)
                ############################################################
                
                sale = 1
                while sale == 1:
                               
                    ############################################################
                    ###### LEE LA MEJOR HASTA AHORA
                    ############################################################

                    
                    soluciones = open('Solutions_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    
                    best = open('Mejoras_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    g = open('Best_Matheuristic_230325_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'
                              +str(eta[0])+'_'+str(eta[1])+'.txt', "r")
                    
                    
                    g.readline().strip().split()
                    
                    # Create variables #
                    x_vars_list = []
                    pares_cero = []
                    pares_nocero = []
                    impares_cero = []
                    impares_nocero = []
                    count = 0
                    for l in L:
                        for k in K:
                            line = g.readline().strip().split()
                            x_vars_list.append(int(line[len(line)-1]))
                            if int(line[len(line)-1]) == 0 and  count % 2 == 0:
                                pares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 == 0:
                                pares_nocero.append([l,k,count])
                            if int(line[len(line)-1]) == 0 and  count % 2 != 0:
                                impares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 != 0:
                                impares_nocero.append([l,k,count])
                            count = count + 1
                    g.close()
                    
                    soluciones.write('Obj: %g' % model.objVal + '\n')
                    soluciones.write(str(x_vars_list))
                    soluciones.write('\n')
                    
                    best.write('Obj: %g' % model.objVal + '\n')
                    best.write(str(x_vars_list))
                    best.write('\n')
                    
                    
                    ###########################################################
                    ######## FIRST FOUND
                    ############################################################
                    
                    sale = 0
                    for i1 in range(len(pares_nocero)):
                        cambio1 = pares_nocero[i1][2]
                        #print(cambio1)
                        for j in range(len(pares_nocero)):
                            cambio2 = pares_nocero[j][2]
                            #print(cambio2)
                            #print(x_vars[pares_nocero[j][0],pares_nocero[j][1]])
                            
                            if cambio1 != cambio2:
                                
                                x_vars_original_cambio1 = x_vars_list[pares_nocero[i1][2]]
                            
                                x_vars_list[cambio1] = x_vars_list[cambio1] - x_vars_original_cambio1
                                x_vars_list[cambio2] = x_vars_list[cambio2] + x_vars_original_cambio1
                                
                                
                                
                                # print("Original ", x_vars_original_cambio1)
                        
                                # print('\n')
                                # print("x_vars_list 1")
                                # print(x_vars_list)
                                # print('\n')
                                
                                presolve = 0
                                
                                model = gp.Model("Swap1")
                                
                                model.setParam('TimeLimit', timelim)
                                
                                model._obj = None
                                model._bd = None
                                model._data = []
                                model._start = time.time()        
                                
                                # Create variables #
                                x_vars = {}
                                cantVarX = 0
                                count = 0
                                for l in L:
                                    for k in K:
                                        x_vars[l,k] = int(x_vars_list[count])
                                        cantVarX += 1
                                        count = count + 1
                                
                                print(x_vars)
                                        
                                        
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
                                for s in range(len(S)):
                                    for i in I:
                                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                                            #obj += 0
                                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                model.setObjective(obj, GRB.MAXIMIZE)  
                                
                                
                                # Add constraints
                                
                                for s in range(len(S)):
                                    
                                    # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                                    # for k in K:
                                    #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                                    
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
                                    # suma_alpha2 = gp.LinExpr()
                                    # for i in I:
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
                                            model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                                    
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
                                
                                with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                                    writer = csv.writer(f)
                                    writer.writerows(model._data)
                                    
                                
                                
                                #archivo = xlsxwriter.Workbook('tesis.csv')
                                #hoja = archivo.add_worksheet()
                                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                for column in range(len(colnames)):
                                    sheet.write(0, column, colnames[column])
                                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                sheet.write(countcsv, 0, name)
                                sheet.write(countcsv, 1, len(I))
                                sheet.write(countcsv, 2, len(L))
                                sheet.write(countcsv, 3, len(S))
                                if len(model._data) != 0:
                                    datos = model._data[len(model._data)-1]
                                    for row in range(len(datos)):
                                        sheet.write(countcsv, row+4, datos[row])
                                
                                
                                #Nombre: Resultados_I_L_M_N_S
                                
                                f = open ('Resultados_Matheuristic_230325_New_'
                                              +str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                                
                                
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
                                        #print(v)
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
                                
                                sheet.write(countcsv, 10, "V1 BLS")
                                
                                countcsv = countcsv + 1
                                #countcsv1 = countcsv1 + 1
                                
                                soluciones.write('Obj (ACT VS ACT BLS): %g' % model.objVal +'\n')
                                soluciones.write(str(x_vars_list))
                                soluciones.write('\n')
                                
                                #sale = 0
                                
                                if model.objVal > mejor_obj:
                                    
                                    colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                    for column in range(len(colnames)):
                                        sheet1.write(0, column, colnames[column])
                                    name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                    sheet1.write(countcsv1, 0, name)
                                    sheet1.write(countcsv1, 1, len(I))
                                    sheet1.write(countcsv1, 2, len(L))
                                    sheet1.write(countcsv1, 3, len(S))
                                    if len(model._data) != 0:
                                        datos = model._data[len(model._data)-1]
                                        for row in range(len(datos)):
                                            sheet1.write(countcsv1, row+4, datos[row])
                                            
                                    sheet1.write(countcsv1, 9, total_time)
                                    
                                    sheet1.write(countcsv1, 10, "V1 BLS")
                                            
                                    countcsv1 = countcsv1 + 1
                                    
                                    best.write('Obj (ACT VS ACT BLS): %g' % model.objVal + '\n')
                                    best.write(str(x_vars_list))
                                    best.write('\n')
                                    mejor_obj = model.objVal
                                    
                                    mejor = open('Best_Matheuristic_230325_'
                                                      +str(tamaños_I[iconj])+str('_')
                                                      +str(tamaños_L[jconj])+str('_')
                                                      +str(tamaños_S[sconj])+'_'
                                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                        
                                    mejor.write('Obj (ACT VS ACT BLS): %g' % model.objVal)
                                    mejor.write('\n')
                                    
                                    cont = 0
                                    for l in L:
                                        for k in K:
                                            mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars_list[cont]))
                                            mejor.write('\n')
                                            cont = cont + 1
                                    mejor.write('-1')
                                    mejor.write('\n')
                        
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
                                                mejor.write('-1')
                                                mejor.write('\n')
                                                name_ind = name_ind + 1
                                                new_name = names[name_ind]
                                            mejor.write('%s %g' % (v.varName, v.x))
                                            mejor.write('\n')
                                        
                                    mejor.write('-1')
                        
                                    mejor.close()
                                    
                                    sale = 1
                    
                        
                                # print('\n')
                                # print("x_vars_list 2")
                                # print(str(x_vars_list))
                                # print('\n')
                                
                                if sale == 1:
                                    break
                                else:
                                    x_vars_list[cambio2] = x_vars_list[cambio2] - x_vars_original_cambio1
                                    x_vars_list[cambio1] = x_vars_list[cambio1] + x_vars_original_cambio1
                                
                                if total_time < time_limit_final:
                                    break
                                
                            
                            if sale == 1:
                                break
                            
                            if total_time < time_limit_final:
                                break
                            
                        
                        if sale == 1:
                            break
                        if total_time > time_limit_ls:
                            break
                    
                    
                # ###########################################################
                # ######## VECINDARIO ACTIVOS VS ACTIVOS (CAMBIOS PARA ALS)
                # ############################################################
                
                sale = 1
                while sale == 1:
                               
                    ############################################################
                    ###### LEE LA MEJOR HASTA AHORA
                    ############################################################
           
                    
                    soluciones = open('Solutions_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    
                    best = open('Mejoras_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    g = open('Best_Matheuristic_230325_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'
                              +str(eta[0])+'_'+str(eta[1])+'.txt', "r")
                    
                    
                    g.readline().strip().split()
                    
                    # Create variables #
                    x_vars_list = []
                    pares_cero = []
                    pares_nocero = []
                    impares_cero = []
                    impares_nocero = []
                    count = 0
                    for l in L:
                        for k in K:
                            line = g.readline().strip().split()
                            x_vars_list.append(int(line[len(line)-1]))
                            if int(line[len(line)-1]) == 0 and  count % 2 == 0:
                                pares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 == 0:
                                pares_nocero.append([l,k,count])
                            if int(line[len(line)-1]) == 0 and  count % 2 != 0:
                                impares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 != 0:
                                impares_nocero.append([l,k,count])
                            count = count + 1
                    g.close()
                    
                    soluciones.write('Obj: %g' % model.objVal + '\n')
                    soluciones.write(str(x_vars_list))
                    soluciones.write('\n')
                    
                    best.write('Obj: %g' % model.objVal + '\n')
                    best.write(str(x_vars_list))
                    best.write('\n')
                    
                    
                    ######################################
                    ####### FIRST FOUND 
                    ######################################
                    
                    sale = 0
                    for i1 in range(len(impares_nocero)):
                        cambio1 = impares_nocero[i1][2]
                        #print(cambio1)
                        for j in range(len(impares_nocero)):
                            cambio2 = impares_nocero[j][2]
                            #print(cambio2)
                            #print(x_vars[impares_nocero[j][0],impares_nocero[j][1]])
                            
                            if cambio1 != cambio2:
                                
                                x_vars_original_cambio1 = x_vars_list[impares_nocero[i1][2]]
                            
                                x_vars_list[cambio1] = x_vars_list[cambio1] - x_vars_original_cambio1
                                x_vars_list[cambio2] = x_vars_list[cambio2] + x_vars_original_cambio1
                                
                                
                                
                                print("Original ", x_vars_original_cambio1)
                        
                                print('\n')
                                print("x_vars_list 1")
                                print(x_vars_list)
                                print('\n')
                                
                                presolve = 0
                                
                                model = gp.Model("Swap1")
                                
                                model.setParam('TimeLimit', timelim)
                                
                                model._obj = None
                                model._bd = None
                                model._data = []
                                model._start = time.time()        
                                
                                # Create variables #
                                x_vars = {}
                                cantVarX = 0
                                count = 0
                                for l in L:
                                    for k in K:
                                        x_vars[l,k] = int(x_vars_list[count])
                                        cantVarX += 1
                                        count = count + 1
                                
                                print(x_vars)
                                        
                                        
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
                                for s in range(len(S)):
                                    for i in I:
                                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                                            #obj += 0
                                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                model.setObjective(obj, GRB.MAXIMIZE)  
                                
                                
                                # Add constraints
                                
                                for s in range(len(S)):
                                    
                                    # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                                    # for k in K:
                                    #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                                    
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
                                    # suma_alpha2 = gp.LinExpr()
                                    # for i in I:
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
                                            model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                                    
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
                                
                                with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                                    writer = csv.writer(f)
                                    writer.writerows(model._data)
                                    
                                
                                
                                #archivo = xlsxwriter.Workbook('tesis.csv')
                                #hoja = archivo.add_worksheet()
                                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                for column in range(len(colnames)):
                                    sheet.write(0, column, colnames[column])
                                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                sheet.write(countcsv, 0, name)
                                sheet.write(countcsv, 1, len(I))
                                sheet.write(countcsv, 2, len(L))
                                sheet.write(countcsv, 3, len(S))
                                if len(model._data) != 0:
                                    datos = model._data[len(model._data)-1]
                                    for row in range(len(datos)):
                                        sheet.write(countcsv, row+4, datos[row])
                                
                                
                                #Nombre: Resultados_I_L_M_N_S
                                
                                f = open ('Resultados_Matheuristic_230325_New_'
                                              +str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                                
                                
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
                                        #print(v)
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
                                
                                sheet.write(countcsv, 10, "V1 ALS")
                                
                                countcsv = countcsv + 1
                                #countcsv1 = countcsv1 + 1
                                
                                soluciones.write('Obj (ACT VS ACT ALS): %g' % model.objVal +'\n')
                                soluciones.write(str(x_vars_list))
                                soluciones.write('\n')
                                
                                #sale = 0
                                
                                if model.objVal > mejor_obj:
                                    
                                    colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                    for column in range(len(colnames)):
                                        sheet1.write(0, column, colnames[column])
                                    name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                    sheet1.write(countcsv1, 0, name)
                                    sheet1.write(countcsv1, 1, len(I))
                                    sheet1.write(countcsv1, 2, len(L))
                                    sheet1.write(countcsv1, 3, len(S))
                                    if len(model._data) != 0:
                                        datos = model._data[len(model._data)-1]
                                        for row in range(len(datos)):
                                            sheet1.write(countcsv1, row+4, datos[row])
                                            
                                    sheet1.write(countcsv1, 9, total_time)
                                    
                                    sheet1.write(countcsv1, 10, "V1 ALS")
                                            
                                    countcsv1 = countcsv1 + 1
                                    
                                    best.write('Obj (ACT VS ACT ALS): %g' % model.objVal + '\n')
                                    best.write(str(x_vars_list))
                                    best.write('\n')
                                    mejor_obj = model.objVal
                                    
                                    mejor = open('Best_Matheuristic_230325_'
                                                      +str(tamaños_I[iconj])+str('_')
                                                      +str(tamaños_L[jconj])+str('_')
                                                      +str(tamaños_S[sconj])+'_'
                                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                        
                                    mejor.write('Obj (ACT VS ACT ALS): %g' % model.objVal)
                                    mejor.write('\n')
                        
                                    cont = 0
                                    for l in L:
                                        for k in K:
                                            mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars_list[cont]))
                                            mejor.write('\n')
                                            cont = cont + 1
                                    mejor.write('-1')
                                    mejor.write('\n')
                        
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
                                                mejor.write('-1')
                                                mejor.write('\n')
                                                name_ind = name_ind + 1
                                                new_name = names[name_ind]
                                            mejor.write('%s %g' % (v.varName, v.x))
                                            mejor.write('\n')
                                        
                                    mejor.write('-1')
                        
                                    mejor.close()
                    
                                    sale = 1
                        
                                
                                
                        
                                # print('\n')
                                # print("x_vars_list 2")
                                # print(str(x_vars_list))
                                # print('\n')
                    
                                if sale == 1:
                                    break
                                else: 
                                    x_vars_list[cambio2] = x_vars_list[cambio2] - x_vars_original_cambio1
                                    x_vars_list[cambio1] = x_vars_list[cambio1] + x_vars_original_cambio1
                                
                                if total_time < time_limit_final:
                                    break
                              
                            if sale == 1:
                                break
                            
                            if total_time < time_limit_final:
                                break
                              
                        if sale == 1:
                            break
                        
                        if total_time > time_limit_ls:
                            break
                    
                    
                #####################################################################
                ######## VECINDARIO DE MEDIOS CAMBIOS ENTRE ACTIVOS Y NO ACTIVOS BLS
                #####################################################################

                sale = 1
                while sale == 1:
                               
                    ############################################################
                    ###### LEE LA MEJOR HASTA AHORA
                    ############################################################
              
                    soluciones = open('Solutions_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    
                    best = open('Mejoras_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    g = open('Best_Matheuristic_230325_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'
                              +str(eta[0])+'_'+str(eta[1])+'.txt', "r")
                    
                    
                    g.readline().strip().split()
                    
                    # Create variables #
                    x_vars_list = []
                    pares_cero = []
                    pares_nocero = []
                    impares_cero = []
                    impares_nocero = []
                    count = 0
                    for l in L:
                        for k in K:
                            line = g.readline().strip().split()
                            x_vars_list.append(int(line[len(line)-1]))
                            if int(line[len(line)-1]) == 0 and  count % 2 == 0:
                                pares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 == 0:
                                pares_nocero.append([l,k,count])
                            if int(line[len(line)-1]) == 0 and  count % 2 != 0:
                                impares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 != 0:
                                impares_nocero.append([l,k,count])
                            count = count + 1
                    g.close()
                    
                    soluciones.write('Obj: %g' % model.objVal + '\n')
                    soluciones.write(str(x_vars_list))
                    soluciones.write('\n')
                    
                    best.write('Obj: %g' % model.objVal + '\n')
                    best.write(str(x_vars_list))
                    best.write('\n')
                    
                    
                    ######################################
                    ####### FIRST FOUND 
                    ######################################
                    
                    sale = 0
                    if len(pares_cero) > 0:
                        for i1 in range(len(pares_nocero)):
                            cambio1 = pares_nocero[i1][2]
                            #print(cambio1)
                            for j in range(len(pares_cero)):
                                cambio2 = pares_cero[j][2]
                                #print(cambio2)
                                #print(x_vars[pares_nocero[j][0],pares_nocero[j][1]])
                                
                                if cambio1 != cambio2:
                                    
                                    x_vars_original_cambio1 = math.floor(x_vars_list[pares_nocero[i1][2]]/2)
                                
                                    x_vars_list[cambio1] = x_vars_list[cambio1] - x_vars_original_cambio1
                                    x_vars_list[cambio2] = x_vars_list[cambio2] + x_vars_original_cambio1
                                    
                                    
                                    
                                    # print("Original ", x_vars_original_cambio1)
                            
                                    # print('\n')
                                    # print("x_vars_list 1")
                                    # print(x_vars_list)
                                    # print('\n')
                                    
                                    presolve = 0
                                    
                                    model = gp.Model("Swap1")
                                    
                                    model.setParam('TimeLimit', timelim)
                                    
                                    model._obj = None
                                    model._bd = None
                                    model._data = []
                                    model._start = time.time()        
                                    
                                    # Create variables #
                                    x_vars = {}
                                    cantVarX = 0
                                    count = 0
                                    for l in L:
                                        for k in K:
                                            x_vars[l,k] = int(x_vars_list[count])
                                            cantVarX += 1
                                            count = count + 1
                                    
                                    print(x_vars)
                                            
                                            
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
                                    for s in range(len(S)):
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                                                #obj += 0
                                                obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                    model.setObjective(obj, GRB.MAXIMIZE)  
                                    
                                    
                                    # Add constraints
                                    
                                    for s in range(len(S)):
                                        
                                        # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                                        # for k in K:
                                        #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                                        
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
                                        # suma_alpha2 = gp.LinExpr()
                                        # for i in I:
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
                                                model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                                        
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
                                    
                                    with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  #+str(len(K))+str('_')
                                                  #+str(len(N))+str('_')
                                                  +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                                        writer = csv.writer(f)
                                        writer.writerows(model._data)
                                        
                                    
                                    
                                    #archivo = xlsxwriter.Workbook('tesis.csv')
                                    #hoja = archivo.add_worksheet()
                                    colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                    for column in range(len(colnames)):
                                        sheet.write(0, column, colnames[column])
                                    name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                    sheet.write(countcsv, 0, name)
                                    sheet.write(countcsv, 1, len(I))
                                    sheet.write(countcsv, 2, len(L))
                                    sheet.write(countcsv, 3, len(S))
                                    if len(model._data) != 0:
                                        datos = model._data[len(model._data)-1]
                                        for row in range(len(datos)):
                                            sheet.write(countcsv, row+4, datos[row])
                                    
                                    
                                    #Nombre: Resultados_I_L_M_N_S
                                    
                                    f = open ('Resultados_Matheuristic_230325_New_'
                                                  +str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  #+str(len(K))+str('_')
                                                  #+str(len(N))+str('_')
                                                  +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                                    
                                    
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
                                            #print(v)
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
                                    
                                    sheet.write(countcsv, 10, "V2 BLS")
                                    
                                    countcsv = countcsv + 1
                                    #countcsv1 = countcsv1 + 1
                                    
                                    soluciones.write('Obj (MEDIOS ACT VS NO ACT BLS): %g' % model.objVal +'\n')
                                    soluciones.write(str(x_vars_list))
                                    soluciones.write('\n')
                                    
                                    #sale = 0
                                    if model.objVal > mejor_obj:
                                        
                                        colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                        for column in range(len(colnames)):
                                            sheet1.write(0, column, colnames[column])
                                        name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                        sheet1.write(countcsv1, 0, name)
                                        sheet1.write(countcsv1, 1, len(I))
                                        sheet1.write(countcsv1, 2, len(L))
                                        sheet1.write(countcsv1, 3, len(S))
                                        if len(model._data) != 0:
                                            datos = model._data[len(model._data)-1]
                                            for row in range(len(datos)):
                                                sheet1.write(countcsv1, row+4, datos[row])
                                                
                                        sheet1.write(countcsv1, 9, total_time)
                                        sheet1.write(countcsv1, 10, "V2 BLS")
                                        countcsv1 = countcsv1 + 1
                                        
                                        best.write('Obj (MEDIOS ACT VS NO ACT BLS): %g' % model.objVal + '\n')
                                        best.write(str(x_vars_list))
                                        best.write('\n')
                                        mejor_obj = model.objVal
                                        
                                        mejor = open('Best_Matheuristic_230325_'
                                                          +str(tamaños_I[iconj])+str('_')
                                                          +str(tamaños_L[jconj])+str('_')
                                                          +str(tamaños_S[sconj])+'_'
                                                          +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                            
                                        mejor.write('Obj (MEDIOS ACT VS NO ACT BLS): %g' % model.objVal)
                                        mejor.write('\n')
                                        
                                        cont = 0
                                        for l in L:
                                            for k in K:
                                                mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars_list[cont]))
                                                mejor.write('\n')
                                                cont = cont + 1
                                        mejor.write('-1')
                                        mejor.write('\n')
                                        
                            
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
                                                    mejor.write('-1')
                                                    mejor.write('\n')
                                                    name_ind = name_ind + 1
                                                    new_name = names[name_ind]
                                                mejor.write('%s %g' % (v.varName, v.x))
                                                mejor.write('\n')
                                            
                                        mejor.write('-1')
                            
                                        mejor.close()
                                        
                                        sale = 1
    
                                    # print('\n')
                                    # print("x_vars_list 2")
                                    # print(str(x_vars_list))
                                    # print('\n')
                                    
                                    if sale == 1:
                                        break
                                    else:
                                        x_vars_list[cambio2] = x_vars_list[cambio2] - x_vars_original_cambio1
                                        x_vars_list[cambio1] = x_vars_list[cambio1] + x_vars_original_cambio1
                                    
                                    if total_time < time_limit_final:
                                        break
                                    
                                
                                if sale == 1:
                                    break
                                
                                if total_time < time_limit_final:
                                    break
                                
                            if sale == 1:
                                break
                            
                            if total_time > time_limit_ls:
                                break
                                
                                
                            
                #################################################################
                ######## VECINDARIO DE MEDIOS CAMBIOS ENTRE ACTIVOS Y ACTIVOS BLS
                #################################################################
    
                sale = 1            
                while sale == 1:
                               
                    ############################################################
                    ###### LEE LA MEJOR HASTA AHORA
                    ############################################################
                    
                    
                    soluciones = open('Solutions_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    
                    best = open('Mejoras_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    g = open('Best_Matheuristic_230325_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'
                              +str(eta[0])+'_'+str(eta[1])+'.txt', "r")
                    
                    
                    g.readline().strip().split()
                    
                    # Create variables #
                    x_vars_list = []
                    pares_cero = []
                    pares_nocero = []
                    impares_cero = []
                    impares_nocero = []
                    count = 0
                    for l in L:
                        for k in K:
                            line = g.readline().strip().split()
                            x_vars_list.append(int(line[len(line)-1]))
                            if int(line[len(line)-1]) == 0 and  count % 2 == 0:
                                pares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 == 0:
                                pares_nocero.append([l,k,count])
                            if int(line[len(line)-1]) == 0 and  count % 2 != 0:
                                impares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 != 0:
                                impares_nocero.append([l,k,count])
                            count = count + 1
                    g.close()
                    
                    soluciones.write('Obj: %g' % model.objVal + '\n')
                    soluciones.write(str(x_vars_list))
                    soluciones.write('\n')
                    
                    best.write('Obj: %g' % model.objVal + '\n')
                    best.write(str(x_vars_list))
                    best.write('\n')
                    
                    
                    ######################################
                    ####### FIRST FOUND 
                    ######################################
                    
                    sale = 0
                    for i1 in range(len(pares_nocero)):
                        cambio1 = pares_nocero[i1][2]
                        #print(cambio1)
                        for j in range(len(pares_nocero)):
                            cambio2 = pares_nocero[j][2]
                            #print(cambio2)
                            #print(x_vars[pares_nocero[j][0],pares_nocero[j][1]])
                            
                            if cambio1 != cambio2:
                                
                                x_vars_original_cambio1 = math.floor(x_vars_list[pares_nocero[i1][2]]/2)
                            
                                x_vars_list[cambio1] = x_vars_list[cambio1] - x_vars_original_cambio1
                                x_vars_list[cambio2] = x_vars_list[cambio2] + x_vars_original_cambio1
                                
                                
                                
                                # print("Original ", x_vars_original_cambio1)
                        
                                # print('\n')
                                # print("x_vars_list 1")
                                # print(x_vars_list)
                                # print('\n')
                                
                                presolve = 0
                                
                                model = gp.Model("Swap1")
                                
                                model.setParam('TimeLimit', timelim)
                                
                                model._obj = None
                                model._bd = None
                                model._data = []
                                model._start = time.time()        
                                
                                # Create variables #
                                x_vars = {}
                                cantVarX = 0
                                count = 0
                                for l in L:
                                    for k in K:
                                        x_vars[l,k] = int(x_vars_list[count])
                                        cantVarX += 1
                                        count = count + 1
                                
                                print(x_vars)
                                        
                                        
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
                                for s in range(len(S)):
                                    for i in I:
                                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                                            #obj += 0
                                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                model.setObjective(obj, GRB.MAXIMIZE)  
                                
                                
                                # Add constraints
                                
                                for s in range(len(S)):
                                    
                                    # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                                    # for k in K:
                                    #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                                    
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
                                    # suma_alpha2 = gp.LinExpr()
                                    # for i in I:
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
                                            model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                                    
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
                                
                                with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                                    writer = csv.writer(f)
                                    writer.writerows(model._data)
                                    
                                
                                
                                #archivo = xlsxwriter.Workbook('tesis.csv')
                                #hoja = archivo.add_worksheet()
                                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                for column in range(len(colnames)):
                                    sheet.write(0, column, colnames[column])
                                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                sheet.write(countcsv, 0, name)
                                sheet.write(countcsv, 1, len(I))
                                sheet.write(countcsv, 2, len(L))
                                sheet.write(countcsv, 3, len(S))
                                if len(model._data) != 0:
                                    datos = model._data[len(model._data)-1]
                                    for row in range(len(datos)):
                                        sheet.write(countcsv, row+4, datos[row])
                                
                                
                                #Nombre: Resultados_I_L_M_N_S
                                
                                f = open ('Resultados_Matheuristic_230325_New_'
                                              +str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                                
                                
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
                                        #print(v)
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
                                sheet.write(countcsv, 10, "V3 BLS")
                                
                                countcsv = countcsv + 1
                                #countcsv1 = countcsv1 + 1
                                
                                soluciones.write('Obj (MEDIOS ACT VS ACT BLS): %g' % model.objVal +'\n')
                                soluciones.write(str(x_vars_list))
                                soluciones.write('\n')
                                
                                #sale = 0
                                if model.objVal > mejor_obj:
                                    
                                    colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                    for column in range(len(colnames)):
                                        sheet1.write(0, column, colnames[column])
                                    name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                    sheet1.write(countcsv1, 0, name)
                                    sheet1.write(countcsv1, 1, len(I))
                                    sheet1.write(countcsv1, 2, len(L))
                                    sheet1.write(countcsv1, 3, len(S))
                                    if len(model._data) != 0:
                                        datos = model._data[len(model._data)-1]
                                        for row in range(len(datos)):
                                            sheet1.write(countcsv1, row+4, datos[row])
                                            
                                    sheet1.write(countcsv1, 9, total_time)
                                    sheet1.write(countcsv1, 10, "V3 BLS")
                                    countcsv1 = countcsv1 + 1
                                    
                                    best.write('Obj (MEDIOS ACT VS ACT BLS): %g' % model.objVal + '\n')
                                    best.write(str(x_vars_list))
                                    best.write('\n')
                                    mejor_obj = model.objVal
                                    
                                    mejor = open('Best_Matheuristic_230325_'
                                                      +str(tamaños_I[iconj])+str('_')
                                                      +str(tamaños_L[jconj])+str('_')
                                                      +str(tamaños_S[sconj])+'_'
                                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                        
                                    mejor.write('Obj (MEDIOS ACT VS ACT BLS): %g' % model.objVal)
                                    mejor.write('\n')
                                    
                                    cont = 0
                                    for l in L:
                                        for k in K:
                                            mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars_list[cont]))
                                            mejor.write('\n')
                                            cont = cont + 1
                                    mejor.write('-1')
                                    mejor.write('\n')
                        
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
                                                mejor.write('-1')
                                                mejor.write('\n')
                                                name_ind = name_ind + 1
                                                new_name = names[name_ind]
                                            mejor.write('%s %g' % (v.varName, v.x))
                                            mejor.write('\n')
                                        
                                    mejor.write('-1')
                        
                                    mejor.close()
                                    
                                    sale = 1
            
                                # print('\n')
                                # print("x_vars_list 2")
                                # print(str(x_vars_list))
                                # print('\n')
                                
                                if sale == 1:
                                    break
                                else:
                                    x_vars_list[cambio2] = x_vars_list[cambio2] - x_vars_original_cambio1
                                    x_vars_list[cambio1] = x_vars_list[cambio1] + x_vars_original_cambio1
                                
                                if total_time < time_limit_final:
                                    break
                                
                            
                            if sale == 1:
                                break
                            
                            if total_time < time_limit_final:
                                break
                        
                        if sale == 1:
                            break
                        
                        if total_time > time_limit_ls:
                            break
                    
                    
                ##############################################################
                ######## VECINDARIO DE CAMBIOS ENTRE ACTIVOS Y NO ACTIVOS BLS
                ##############################################################
            
                sale = 1
                while sale == 1:
                               
                    ############################################################
                    ###### LEE LA MEJOR HASTA AHORA
                    ############################################################
                    
                    
                    soluciones = open('Solutions_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    
                    best = open('Mejoras_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    g = open('Best_Matheuristic_230325_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'
                              +str(eta[0])+'_'+str(eta[1])+'.txt', "r")
                    
                    
                    g.readline().strip().split()
                    
                    # Create variables #
                    x_vars_list = []
                    pares_cero = []
                    pares_nocero = []
                    impares_cero = []
                    impares_nocero = []
                    count = 0
                    for l in L:
                        for k in K:
                            line = g.readline().strip().split()
                            x_vars_list.append(int(line[len(line)-1]))
                            if int(line[len(line)-1]) == 0 and  count % 2 == 0:
                                pares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 == 0:
                                pares_nocero.append([l,k,count])
                            if int(line[len(line)-1]) == 0 and  count % 2 != 0:
                                impares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 != 0:
                                impares_nocero.append([l,k,count])
                            count = count + 1
                    g.close()
                    
                    soluciones.write('Obj: %g' % model.objVal + '\n')
                    soluciones.write(str(x_vars_list))
                    soluciones.write('\n')
                    
                    best.write('Obj: %g' % model.objVal + '\n')
                    best.write(str(x_vars_list))
                    best.write('\n')
                    
                    
                    ######################################
                    ####### FIRST FOUND 
                    ######################################
                    
                    sale = 0
                    if len(pares_cero) > 0:
                        for i in range(len(pares_cero)):
                            cambio1 = pares_cero[i][2]
                            #print(cambio1)
                            for j in range(len(pares_nocero)):
                                cambio2 = pares_nocero[j][2]
                                #print(cambio2)
                                #print(x_vars[pares_nocero[j][0],pares_nocero[j][1]])
                                
                                x_vars_list[cambio1] = x_vars[pares_nocero[j][0],pares_nocero[j][1]]
                                x_vars_list[cambio2] = 0
                        
                                #print('\n')
                                #print("x_vars_list 1")
                                #print(x_vars_list)
                                #print('\n')
                                
                                presolve = 0
                                
                                model = gp.Model("Swap1")
                                
                                model.setParam('TimeLimit', timelim)
                                
                                model._obj = None
                                model._bd = None
                                model._data = []
                                model._start = time.time()        
                                
                                # Create variables #
                                x_vars = {}
                                cantVarX = 0
                                count = 0
                                for l in L:
                                    for k in K:
                                        x_vars[l,k] = int(x_vars_list[count])
                                        cantVarX += 1
                                        count = count + 1
                                
                                print(x_vars)
                                        
                                        
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
                                for s in range(len(S)):
                                    for i in I:
                                        if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                                            #obj += 0
                                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                model.setObjective(obj, GRB.MAXIMIZE)  
                                
                                
                                # Add constraints
                                
                                for s in range(len(S)):
                                    
                                    # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                                    # for k in K:
                                    #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                                    
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
                                    # suma_alpha2 = gp.LinExpr()
                                    # for i in I:
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
                                            model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                                    
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
                                
                                with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                                    writer = csv.writer(f)
                                    writer.writerows(model._data)
                                    
                                
                                
                                #archivo = xlsxwriter.Workbook('tesis.csv')
                                #hoja = archivo.add_worksheet()
                                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                for column in range(len(colnames)):
                                    sheet.write(0, column, colnames[column])
                                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                sheet.write(countcsv, 0, name)
                                sheet.write(countcsv, 1, len(I))
                                sheet.write(countcsv, 2, len(L))
                                sheet.write(countcsv, 3, len(S))
                                if len(model._data) != 0:
                                    datos = model._data[len(model._data)-1]
                                    for row in range(len(datos)):
                                        sheet.write(countcsv, row+4, datos[row])
                                
                                
                                #Nombre: Resultados_I_L_M_N_S
                                
                                f = open ('Resultados_Matheuristic_230325_New_'
                                              +str(len(I))+str('_')
                                              +str(len(L))+str('_')
                                              #+str(len(K))+str('_')
                                              #+str(len(N))+str('_')
                                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                                
                                
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
                                        #print(v)
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
                                sheet.write(countcsv, 10, "V4 BLS")
                                
                                countcsv = countcsv + 1
                                #countcsv1 = countcsv1 + 1
                                
                                soluciones.write('Obj (ACT VS NO ACT BLS): %g' % model.objVal +'\n')
                                soluciones.write(str(x_vars_list))
                                soluciones.write('\n')
                                
                                #sale = 0
                                if model.objVal > mejor_obj:
                                    
                                    colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                    for column in range(len(colnames)):
                                        sheet1.write(0, column, colnames[column])
                                    name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                    sheet1.write(countcsv1, 0, name)
                                    sheet1.write(countcsv1, 1, len(I))
                                    sheet1.write(countcsv1, 2, len(L))
                                    sheet1.write(countcsv1, 3, len(S))
                                    if len(model._data) != 0:
                                        datos = model._data[len(model._data)-1]
                                        for row in range(len(datos)):
                                            sheet1.write(countcsv1, row+4, datos[row])
                                            
                                    sheet1.write(countcsv1, 9, total_time)
                                    sheet1.write(countcsv1, 10, "V4 BLS")
                                    countcsv1 = countcsv1 + 1
                                    
                                    best.write('Obj (ACT VS NO ACT BLS): %g' % model.objVal + '\n')
                                    best.write(str(x_vars_list))
                                    best.write('\n')
                                    mejor_obj = model.objVal
                                    
                                    mejor = open('Best_Matheuristic_230325_'
                                                      +str(tamaños_I[iconj])+str('_')
                                                      +str(tamaños_L[jconj])+str('_')
                                                      +str(tamaños_S[sconj])+'_'
                                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                        
                                    mejor.write('Obj (ACT VS NO ACT BLS): %g' % model.objVal)
                                    mejor.write('\n')
                        
                                    cont = 0
                                    for l in L:
                                        for k in K:
                                            mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars_list[cont]))
                                            mejor.write('\n')
                                            cont = cont + 1
                                    mejor.write('-1')
                                    mejor.write('\n')
                        
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
                                                mejor.write('-1')
                                                mejor.write('\n')
                                                name_ind = name_ind + 1
                                                new_name = names[name_ind]
                                            mejor.write('%s %g' % (v.varName, v.x))
                                            mejor.write('\n')
                                        
                                    mejor.write('-1')
                        
                                    mejor.close()
                                    
                                    sale = 1
                        
                                
                                
                        
                                #print('\n')
                                #print("x_vars_list 2")
                                #print(str(x_vars_list))
                                #print('\n')
                                
                                if sale == 1:
                                    break
                                else:
                                    x_vars_list[cambio2] = x_vars_list[cambio1]
                                    x_vars_list[cambio1] = 0
                                
                                if total_time < time_limit_final:
                                    break
                                
                            if sale == 1:
                                break
                            
                            if total_time < time_limit_final:
                                break
                        
                        if sale == 1:
                            break
                        
                        if total_time > time_limit_ls:
                            break
                        
                    
                ##########################################################
                ######## VECINDARIO ACTIVOS VS NO ACTIVOS (CAMBIOS EN ALS)
                ##########################################################
               
                sale = 1
                while sale == 1:
                               
                    ############################################################
                    ###### LEE LA MEJOR HASTA AHORA
                    ############################################################
                    
                    soluciones = open('Solutions_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    
                    best = open('Mejoras_Matheuristic_230325_'
                                      +str(tamaños_I[iconj])+str('_')
                                      +str(tamaños_L[jconj])+str('_')
                                      +str(tamaños_S[sconj])+'_'
                                      +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                    g = open('Best_Matheuristic_230325_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'
                              +str(eta[0])+'_'+str(eta[1])+'.txt', "r")
                    
                    
                    g.readline().strip().split()
                    
                    # Create variables #
                    x_vars_list = []
                    pares_cero = []
                    pares_nocero = []
                    impares_cero = []
                    impares_nocero = []
                    count = 0
                    for l in L:
                        for k in K:
                            line = g.readline().strip().split()
                            x_vars_list.append(int(line[len(line)-1]))
                            if int(line[len(line)-1]) == 0 and  count % 2 == 0:
                                pares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 == 0:
                                pares_nocero.append([l,k,count])
                            if int(line[len(line)-1]) == 0 and  count % 2 != 0:
                                impares_cero.append([l,k,count])
                            if int(line[len(line)-1]) != 0 and  count % 2 != 0:
                                impares_nocero.append([l,k,count])
                            count = count + 1
                    g.close()
                    
                    soluciones.write('Obj: %g' % model.objVal + '\n')
                    soluciones.write(str(x_vars_list))
                    soluciones.write('\n')
                    
                    best.write('Obj: %g' % model.objVal + '\n')
                    best.write(str(x_vars_list))
                    best.write('\n')
                    
                    
                    ######################################
                    ####### FIRST FOUND 
                    ######################################
                    
                    sale = 0
                    for i in range(len(impares_cero)):
                        cambio1 = impares_cero[i][2]
                        #print(cambio1)
                        for j in range(len(impares_nocero)):
                            cambio2 = impares_nocero[j][2]
                            #print(cambio2)
                            #print(x_vars[pares_nocero[j][0],pares_nocero[j][1]])
                            
                            x_vars_list[cambio1] = x_vars[impares_nocero[j][0],impares_nocero[j][1]]
                            x_vars_list[cambio2] = 0
                    
                            #print('\n')
                            #print("x_vars_list 1")
                            #print(x_vars_list)
                            #print('\n')
                            
                            presolve = 0
                            
                            model = gp.Model("Swap1")
                            
                            model.setParam('TimeLimit', timelim)
                            
                            model._obj = None
                            model._bd = None
                            model._data = []
                            model._start = time.time()        
                            
                            # Create variables #
                            x_vars = {}
                            cantVarX = 0
                            count = 0
                            for l in L:
                                for k in K:
                                    x_vars[l,k] = int(x_vars_list[count])
                                    cantVarX += 1
                                    count = count + 1
                            
                            #print(x_vars)
                                    
                                    
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
                            for s in range(len(S)):
                                for i in I:
                                    if (S[s][i-1][0] + S[s][i-1][1]) > 0:
                                        #obj += 0
                                        obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                            model.setObjective(obj, GRB.MAXIMIZE)  
                            
                            
                            # Add constraints
                            
                            for s in range(len(S)):
                                
                                # # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                                # for k in K:
                                #     model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                                
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
                                # suma_alpha2 = gp.LinExpr()
                                # for i in I:
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
                                        model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                                
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
                            
                            with open('data_Matheuristic_230325_'+str(len(I))+str('_')
                                          +str(len(L))+str('_')
                                          #+str(len(K))+str('_')
                                          #+str(len(N))+str('_')
                                          +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.csv', 'w') as f:
                                writer = csv.writer(f)
                                writer.writerows(model._data)
                                
                            
                            
                            #archivo = xlsxwriter.Workbook('tesis.csv')
                            #hoja = archivo.add_worksheet()
                            colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                            for column in range(len(colnames)):
                                sheet.write(0, column, colnames[column])
                            name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                            sheet.write(countcsv, 0, name)
                            sheet.write(countcsv, 1, len(I))
                            sheet.write(countcsv, 2, len(L))
                            sheet.write(countcsv, 3, len(S))
                            if len(model._data) != 0:
                                datos = model._data[len(model._data)-1]
                                for row in range(len(datos)):
                                    sheet.write(countcsv, row+4, datos[row])
                            
                            
                            #Nombre: Resultados_I_L_M_N_S
                            
                            f = open ('Resultados_Matheuristic_230325_New_'
                                          +str(len(I))+str('_')
                                          +str(len(L))+str('_')
                                          #+str(len(K))+str('_')
                                          #+str(len(N))+str('_')
                                          +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                            
                            
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
                                    #print(v)
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
                            sheet.write(countcsv, 10, "V4 ALS")
                            
                            countcsv = countcsv + 1
                            #countcsv1 = countcsv1 + 1
                            
                            soluciones.write('Obj (ACT VS NO ACT ALS): %g' % model.objVal +'\n')
                            soluciones.write(str(x_vars_list))
                            soluciones.write('\n')
                            
                            #sale = 0
                            if model.objVal > mejor_obj:
                                
                                colnames = ["name", "I size", "L size", "S size", "model time", "best obj", "best bound", "gap %", "status", "total time"]
                                for column in range(len(colnames)):
                                    sheet1.write(0, column, colnames[column])
                                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')
                                sheet1.write(countcsv1, 0, name)
                                sheet1.write(countcsv1, 1, len(I))
                                sheet1.write(countcsv1, 2, len(L))
                                sheet1.write(countcsv1, 3, len(S))
                                if len(model._data) != 0:
                                    datos = model._data[len(model._data)-1]
                                    for row in range(len(datos)):
                                        sheet1.write(countcsv1, row+4, datos[row])
                                        
                                sheet1.write(countcsv1, 9, total_time)
                                sheet1.write(countcsv1, 10, "V4 ALS")
                                countcsv1 = countcsv1 + 1
                                
                                best.write('Obj (ACT VS NO ACT ALS): %g' % model.objVal + '\n')
                                best.write(str(x_vars_list))
                                best.write('\n')
                                mejor_obj = model.objVal
                                
                                mejor = open('Best_Matheuristic_230325_'
                                                  +str(tamaños_I[iconj])+str('_')
                                                  +str(tamaños_L[jconj])+str('_')
                                                  +str(tamaños_S[sconj])+'_'
                                                  +str(eta[0])+'_'+str(eta[1])+'.txt', "w")
                    
                                mejor.write('Obj (ACT VS NO ACT ALS): %g' % model.objVal)
                                mejor.write('\n')
                    
                                cont = 0
                                for l in L:
                                    for k in K:
                                        mejor.write("located "+str(l)+str(' ')+str(k)+str(' ')+str(x_vars_list[cont]))
                                        mejor.write('\n')
                                        cont = cont + 1
                                mejor.write('-1')
                                mejor.write('\n')
                    
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
                                            mejor.write('-1')
                                            mejor.write('\n')
                                            name_ind = name_ind + 1
                                            new_name = names[name_ind]
                                        mejor.write('%s %g' % (v.varName, v.x))
                                        mejor.write('\n')
                                    
                                mejor.write('-1')
                    
                                mejor.close()
                    
                                sale = 1
                    
                            
                            
                    
                            #print('\n')
                            #print("x_vars_list 2")
                            #print(str(x_vars_list))
                            #print('\n')
                    
                            if sale == 1:
                                break
                            else:
                                x_vars_list[cambio2] = x_vars_list[cambio1]
                                x_vars_list[cambio1] = 0
                            
                            if total_time < time_limit_final:
                                break
                                
                        if sale == 1:
                            break
                        
                        if total_time < time_limit_final:
                            break
                         
                    if sale == 1:
                        break
                    
                    if total_time > time_limit_ls:
                        break
                    
                    
                
                soluciones.close()
                best.close()
                mejor.close()
                g.close()
                    
                book.save('Tesis_Matheuristic_230325_'+str(eta[0])+'_'+str(eta[1])+'.xls') 
                book1.save('Tesis_Matheuristic_Mejoras_230325_'+str(eta[0])+'_'+str(eta[1])+'.xls') 
#book.save('Tesis_Matheuristic_230325_'+str(eta[0])+'_'+str(eta[1])+'.xls') 


                
                

