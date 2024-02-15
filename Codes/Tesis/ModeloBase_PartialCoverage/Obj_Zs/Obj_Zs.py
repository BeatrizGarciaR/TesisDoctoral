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

# tamaños_I = [168, 270, 500, 900, 1500] #Hasta aquí puede bien el modelo
# tamaños_L = [16, 30, 50, 70, 100]
# tamaños_S = [10, 50, 100, 150, 200]

# tamaños_I = [1500] #Aquí batalla pero sí lo hace aún
# tamaños_L = [16, 30, 50, 70, 100]
# tamaños_S = [150, 200]

tamaños_I = [168, 270, 500, 900, 1500] 
tamaños_L = [16]
tamaños_S = [10, 50, 100, 150, 200]

# tamaños_I = [168] 
# tamaños_L = [16]
# tamaños_S = [10]

K = [1,2]

timelim = 1800 #15 horas 
rates = [0.4]
verif = 0.4

ambulance = [[10, 6], [20,11], [35,20]]
#eta = [10, 6]
t = 10
tmax = 30
wi = [0.65, 0.2, 0.1, 0.05]

countcsv = 1
       
book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('Tesis_Obj_Zs_060224', cell_overwrite_ok=True)

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
                
                # Create variables #
                x_vars = {}
                cantVarX = 0
                for l in L:
                    for k in K:
                        x_vars[l,k] = model.addVar(vtype=GRB.INTEGER, 
                                         name="located "+str(l)+str(' ')+str(k))
                        cantVarX += 1
                        
                        
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
                    
                    # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                    for k in K:
                        model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                    
                    # Restricción 4: No enviar más ambulancias de las localizadas para k = 1
                    amb1 = gp.LinExpr()
                    for l in L: 
                        for i in I:
                            if S[s][i-1][0] != 0:                            
                                amb1 += y_vars[s+1,l,1,i]
                        model.addConstr(amb1 <= x_vars[l,1], "c4")
                    
                    # Restricción 4_1: No enviar más ambulancias de las localizadas para k = 2
                    amb2 = gp.LinExpr()
                    for l in L:
                        for i in I:
                            if S[s][i-1][0] != 0:
                                amb2 += y_vars[s+1,l,2,i] 
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                amb2 += y_vars[s+1,l,2,i] 
                        model.addConstr(amb2 <= x_vars[l,2], "c4_1")
                        
                    
                    # Restricción 5: Desactivar alpha (cobertura total)
                    suma_alpha2 = gp.LinExpr()
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_alpha2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_alpha2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma_alpha2, "c5")
                    
                    
                    # Restricción 6: Desactivar alpha (cobertura total)
                    suma_alpha2 = gp.LinExpr()
                    for i in I:
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
                    suma_beta2 = gp.LinExpr()
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_beta2 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_beta2 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma_beta2, "c7")
                            
                            
                            
                    # Restricción 8: Desactivar beta (cobertura parcial 1)
                    suma_beta = gp.LinExpr()
                    suma_beta_aux = gp.LinExpr()
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_beta += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                                suma_beta_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_beta += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                                suma_beta_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(beta_vars[s+1,i] <= 100000000*(suma_beta - suma_beta_aux), "c8" )
           
                    
           
                    # Restricción 9: Desactivar delta (cobertura parcial 2)
                    suma_delta2 = gp.LinExpr()
                    for i in I:
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
                    suma_delta3 = gp.LinExpr()
                    suma_delta3_aux = gp.LinExpr()
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_delta3 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                                suma_delta3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0  and S[s][i-1][0] == 0:
                                suma_delta3 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                                suma_delta3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(suma_delta3*delta_vars[s+1,i] <= suma_delta3_aux, "c_10")
                            
                    
                    # Restricción 11: Desactivar phi (cobertura parcial 3)
                    suma_phi2 = gp.LinExpr()
                    for i in I:
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
                    suma_phi3 = gp.LinExpr()
                    suma_phi3_aux = gp.LinExpr()
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_phi3 += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                                suma_phi3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,1,i] + cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_phi3 += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                                suma_phi3_aux += gp.quicksum(cli[l-1][i-1]*y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(phi_vars[s+1,i] <= 1000000000000*(suma_phi3 - suma_phi3_aux), "c_12")    
                    
                    # Restricción 16: Activar gamma (cobertura nula)
                    suma_gamma = gp.LinExpr()
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            if S[s][i-1][0] != 0:
                                suma_gamma += gp.quicksum(y_vars[s+1,l,1,i] + y_vars[s+1,l,2,i] for l in L)
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                suma_gamma += gp.quicksum(y_vars[s+1,l,2,i] for l in L)
                            model.addConstr(suma_gamma + gamma_vars[s+1,i] >= 1, "c_16")
                            
                    #Restricción 17: Solo se puede activar un tipo de cobertura     
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] > 0:
                            model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_18")
                    
                    
                # objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
                # objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
                # gap = abs((objbst - objbnd) / objbst)     
    
                # Optimize model
                model.optimize(callback=data_cb)
                
                end_time = time.time()
                
                elapsed_time = end_time - model._start 
                
                #imprimir variables 
                
                with open('data_Obj_Zs_060224_'+str(len(I))+str('_')
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
                
                
                # with open('tesis.csv', 'a') as f:
                #     writer = csv.writer(f)
                #     name = str('Instance')+str(len(I))+str('_')+str(len(L))+str('_')+str(len(S))
                #     f.write(str(name))
                #     f.write('\n')
                #     for row in range(len(model._data[len(model._data)-1])):
                #         f.write(countcsv, row, str(model._data[len(model._data)-1][row]))
                #     countcsv = countcsv + 1 
                
                #Nombre: Resultados_I_L_M_N_S
                
                f = open ('Resultados_Prueba_ObjZs_Scenarios_060224_'
                              +str(len(I))+str('_')
                              +str(len(L))+str('_')
                              #+str(len(K))+str('_')
                              #+str(len(N))+str('_')
                              +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
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
                
                if model.objVal != float("-inf"):
                    for v in model.getVars():
                        f.write('%s %g' % (v.varName, v.x))
                        f.write('\n')
                
                #imprimir el valor objetivo
                print('Obj: %g' % model.objVal)
                print("Finished")
                print(" ")
                print(" ")
                
                f.close()
                
                
                # coberturas = open ('Coberturas_Obj_Zs_060224_'
                #               +str(len(I))+str('_')
                #               +str(len(L))+str('_')
                #               +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')                      
                
                # lectura = open ('Resultados_Prueba_Obj_Zs_060224_'
                #               +str(len(I))+str('_')
                #               +str(len(L))+str('_')
                #               +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','r')
                # line = lectura.readline()
                # #print("line", line)
                # line = lectura.readline()
                # #print("line", line)
                
                # for salto0 in range(cantVarX):
                #     line = lectura.readline()
                # #print("lineX", line)
                
                # for salto in range(cantVarY):
                #     line = lectura.readline()
                # #print("lineY", line)
                 
                # coberturaTotal = 0
                # for salto1 in range(cantVarAlpha):
                #     line = lectura.readline()
                #     if int(line[len(line)-2]) == 1:
                #         coberturaTotal += 1
                # coberturas.write(str(coberturaTotal/TotalAccidentes))
                # coberturas.write('\n')
                
                # #print("line1", line)
                
                # coberturaParcial1 = 0
                # for salto2 in range(cantVarBeta):
                #     line = lectura.readline()
                #     if int(line[len(line)-2]) == 1:
                #         coberturaParcial1 += 1
                # coberturas.write(str(coberturaParcial1/TotalAccidentes))
                # coberturas.write('\n')
                
                # #print("line2", line)
                
                # coberturaParcial2 = 0
                # for salto3 in range(cantVarDelta):
                #     line = lectura.readline()
                #     if int(line[len(line)-2]) == 1:
                #         coberturaParcial2 += 1
                # coberturas.write(str(coberturaParcial2/TotalAccidentes))
                # coberturas.write('\n')
                
                # #print("line3", line)
                
                # coberturaParcial3 = 0
                # for salto4 in range(cantVarPhi):
                #     line = lectura.readline()
                #     if int(line[len(line)-2]) == 1:
                #         coberturaParcial3 += 1
                # coberturas.write(str(coberturaParcial3/TotalAccidentes))
                # coberturas.write('\n')
    
                # #print("line4", line)
    
                # coberturaNula = 0
                # for salto5 in range(cantVarGamma):
                #     line = lectura.readline()
                #     if int(line[len(line)-2]) == 1:
                #         coberturaNula += 1
                # coberturas.write(str(coberturaNula/TotalAccidentes))
                # coberturas.write('\n')
                
                # #print("line5", line)
                
                # coberturas.write(str(-1))
                # coberturas.write('\n')
                
                # lectura.close()
                
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
                
                
                
                # model.write('model_250923_'+str(len(I))+str('_')
                #               +str(len(L))+str('_')
                #               #+str(len(K))+str('_')
                #               #+str(len(N))+str('_')
                #               +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.lp')
                # model.write('model_250923_'+str(len(I))+str('_')
                #               +str(len(L))+str('_')
                #               +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.mps')
                
                
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
                # for i in range(len(alpha_vars)):
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
                
                # archivo.close()
                # coberturas.close()
                
                end_time = time.time()
                total_time = end_time - initial_time 
                
                sheet.write(countcsv, 9, total_time)
                
                countcsv = countcsv + 1
                
                
                book.save('Tesis_Obj_Zs_060224_'+str(eta[0])+'_'+str(eta[1])+'.xls') 
