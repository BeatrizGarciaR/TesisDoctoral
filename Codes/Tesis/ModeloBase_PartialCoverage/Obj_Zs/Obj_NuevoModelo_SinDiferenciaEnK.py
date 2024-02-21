# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 17:40:38 2024

@author: beatr


MODELO MODIFICADO SIN RESTRICCIONES DE K=1 Y K=2

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

# tamaños_I = [168] #Aquí batalla pero sí lo hace aún
# tamaños_L = [16]
# tamaños_S = [10]

tamaños_I = [168, 270, 500, 900, 1500] 
tamaños_L = [30]
tamaños_S = [10, 50, 100, 150, 200]

K = [1,2]

timelim = 10800 #3 horas 
rates = [0.4]
verif = 0.4

ambulance = [[10, 6], [20,11], [35,20]]
#ambulance = [[10,6]]
t = 10
tmax = 30
w_vars = [0.7, 0.3]
countcsv = 1
       
book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('Tesis_NewModel_NewModel_070224', cell_overwrite_ok=True)

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
    # else:
    #     cur_obj = m.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
    #     cur_bd = m.cbGet(gp.GRB.Callback.MIPSOL_OBJBND)
    #     #sepa = model.cbGet(GRB.callback.MIP_NODCNT)
    #     #sepa2 = model.cbGet(GRB.callback.MIP_ITRCNT)
    #     gap = abs((cur_obj - cur_bd) / cur_obj)*100  
    #     status = gp.GRB.OPTIMAL
    #     #gap = cur_obj - cur_bd
    #     # Did objective value or best bound change?
    #     # if m._obj != cur_obj or m._bd != cur_bd:
    #     #     m._obj = cur_obj
    #     #     m._bd = cur_bd
    #     #     m._data.append([time.time() - model._start, cur_obj, cur_bd])
    #     m._data.append(["time", "best", "best bound", "gap %", "status"])
    #     m._data.append([time.time() - model._start, cur_obj, cur_bd, gap, status])



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
                #pi = 0.1
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
                                         name="located_"+str(l)+str(' ')+str(k))
                        cantVarX += 1
                        
                
                y_vars = {}    
                cantVarY = 0
                for s in range(len(S)):        
                    for l in L:
                        for i in I:
                            if S[s][i-1][0] != 0:
                                y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="OnTime_"+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                cantVarY += 1
                                
                                
                            if S[s][i-1][1] != 0:
                                y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="OnTime_"+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                cantVarY += 1
                        
                        
                # y_vars = {}    
                # cantVarY = 0
                # for s in range(len(S)):        
                #     for l in L:
                #         for i in I:
                #             for k in K:
                #                 y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                #                                 name="OnTime_"+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                #                 cantVarY += 1
                
                
                v_vars = {}    
                cantVarV = 0
                for s in range(len(S)):        
                    for l in L:
                        for i in I:
                            if S[s][i-1][0] != 0:
                                v_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="Delayed_"+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                cantVarV += 1
                                
                            if S[s][i-1][1] != 0:
                                v_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="Delayed_"+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                cantVarV += 1

                
                # v_vars = {}    
                # cantVarV = 0
                # for s in range(len(S)):        
                #     for l in L:
                #         for i in I:
                #             for k in K:
                #                 v_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                #                                 name="delayed_"+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                #                 cantVarV += 1
                
                
                gamma_vars = {}    
                cantVarGamma = 0
                for s in range(len(S)):
                    for l in L:
                        for i in I:
                            if S[s][i-1][0] != 0:
                                gamma_vars[s+1,1,i] = model.addVar(vtype=GRB.INTEGER, 
                                                name="NotAssigned_"+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                cantVarGamma += 1
                                
                                
                            if S[s][i-1][1] != 0:
                                gamma_vars[s+1,2,i] = model.addVar(vtype=GRB.INTEGER, 
                                                name="NotAssigned_"+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                cantVarGamma += 1
                                
                
                # gamma_vars = {} ## z null
                # cantVarGamma = 0
                # for s in range(len(S)):
                #     for i in I:
                #         for k in K:
                #             gamma_vars[s+1,i,k] = model.addVar(vtype=GRB.BINARY,
                #                                                name="notAssigned"+str(s+1)+str(' ')+str(i)+str(k))
                #             cantVarGamma += 1
                           
                            
                obj = gp.LinExpr()
                for s in range(len(S)):
                    for l in L:    
                        for i in I:
                            if S[s][i-1][0] != 0:
                                obj += (w_vars[0]*y_vars[s+1,l,1,i] + w_vars[1]*v_vars[s+1,l,1,i] - pi*gamma_vars[s+1,1,i]) * (1/len(S))
                               
                            if S[s][i-1][1] != 0 and S[s][i-1][0] == 0:
                                obj += (w_vars[0]*y_vars[s+1,l,2,i] + w_vars[1]*v_vars[s+1,l,2,i] - pi*gamma_vars[s+1,2,i]) * (1/len(S))
                               
                model.setObjective(obj, GRB.MAXIMIZE)  
    
                 
                # Add constraints
                
                for s in range(len(S)):
                    
                    # Restricción 3: No localizar más ambulancias de las disponibles en el sistema
                    for k in K:
                        model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c3")
                    
                    # Restricción 4: No enviar más ambulancias de las localizadas para k = 1
                    for l in L: 
                        amb1 = gp.LinExpr()
                        for i in I:
                            if S[s][i-1][0] != 0:                            
                                amb1 += y_vars[s+1,l,1,i] + v_vars[s+1,l,1,i]
                        model.addConstr(amb1 <= x_vars[l,1], "c4")                       
                        
                    # Restricción 5: No enviar más ambulancias de las localizadas para k = 2
                    for l in L:
                        amb2 = gp.LinExpr()
                        for i in I:
                            if S[s][i-1][1] != 0:
                                amb2 += y_vars[s+1,l,2,i] + v_vars[s+1,l,2,i]
                        model.addConstr(amb2 <= x_vars[l,2], "c5")
                                     
                    # # Restricción 6: No enviar más ambulancias de las necesarias para k = 1
                    # for i in I: 
                    #     if S[s][i-1][0] != 0: 
                    #         model.addConstr(gp.quicksum(y_vars[s+1,l,1,i] for l in L) <= S[s][i-1][0], "c6")   
                    
                    # # # Restricción 6: No enviar más ambulancias de las necesarias
                    # # amb1 = gp.LinExpr()
                    # # for i in I:  
                    # #     for k in K:
                    # #         amb1 = gp.quicksum(y_vars[s+1,l,k,i] for l in L)
                    # #         model.addConstr(amb1 <= S[s][i-1][k-1], "c6")
                            
                    # # Restricción 7: No enviar más ambulancias de las necesarias para k = 2
                    # for i in I:
                    #     if S[s][i-1][1] != 0:
                    #         model.addConstr(gp.quicksum(y_vars[s+1,l,2,i] for l in L) <= S[s][i-1][1], "c7")
                            
                    # Restricción 8: No exceder cli para k = 1
                    for l in L:
                        for i in I: 
                            if S[s][i-1][0] != 0:                       
                                model.addConstr(y_vars[s+1,l,1,i] <= cli[l-1][i-1], "c8")  
                    
                    # # # Restricción 8: No exceder cli
                    # # for l in L:
                    # #     for i in I:
                    # #         for k in K:
                    # #             model.addConstr(y_vars[s+1,l,k,i]  <= cli[l-1][i-1], "c8")
                                
                    # Restricción 9: No exceder cli para k = 2
                    for l in L:
                        for i in I:  
                            if S[s][i-1][1] != 0:
                                model.addConstr(y_vars[s+1,l,2,i] <= cli[l-1][i-1], "c9") 
                                
                    # Restricción 10: solo se prende y_vars o v_vars o ninguna para k = 1
                    for l in L:
                        for i in I: 
                            if S[s][i-1][0] != 0:                       
                                model.addConstr(y_vars[s+1,l,1,i] + v_vars[s+1,l,1,i] <= 1, "c10") 
                                    
                    # # #Restricción 10: Solo se activa una de las variables y_vars o v_vars
                    # # for l in L:
                    # #     for i in I:
                    # #         for k in K:
                    # #             model.addConstr(y_vars[s+1,l,k,i] + v_vars[s+1,l,k,i]  <= 1, "c9")
                    
                    # Restricción 11: solo se prende y_vars o v_vars o ninguna para k = 2
                    for l in L:
                        for i in I: 
                            if S[s][i-1][1] != 0:
                                model.addConstr(y_vars[s+1,l,2,i] + v_vars[s+1,l,2,i] <= 1, "c11") 
                                
                    # Restricción 12: suma de variables igual a aik para k = 1
                    for i in I: 
                        if S[s][i-1][0] != 0:                       
                            model.addConstr(gp.quicksum(y_vars[s+1,l,1,i] + v_vars[s+1,l,1,i] for l in L) + gamma_vars[s+1,1,i] == S[s][i-1][0], "c12") 
                  
                    # # # Restricción 10: la suma de las variables es lo que se necesita
                    # # for i in I:
                    # #     for k in K:
                    # #         model.addConstr(gp.quicksum(y_vars[s+1,l,k,i] + v_vars[s+1,l,k,i] for l in L) + gamma_vars[s+1,i,k] == 1)
                    
                    # Restricción 13: suma de variables igual a aik para k = 2
                    for i in I:
                        if S[s][i-1][1] != 0:
                            model.addConstr(gp.quicksum(y_vars[s+1,l,2,i] + v_vars[s+1,l,2,i] for l in L) + gamma_vars[s+1,2,i] == S[s][i-1][1], "c13") 
                    
                    # # Restricción 14: No enviar más ambulancias de las necesarias para k = 1
                    # for i in I: 
                    #     if S[s][i-1][0] != 0: 
                    #         model.addConstr(gp.quicksum(v_vars[s+1,l,1,i] for l in L) <= S[s][i-1][0], "c14") 
                  
                    # # # Restricción 11: 
                    # # for i in I:
                    # #     for k in K:
                    # #         model.addConstr(gp.quicksum(v_vars[s+1,l,k,i] for l in L) <= S[s][i-1][k-1], "c11")   
                    
                    # # Restricción 15: No enviar más ambulancias de las necesarias para k = 2
                    
                    # for i in I:
                    #     if S[s][i-1][1] != 0 :
                    #         model.addConstr(gp.quicksum(v_vars[s+1,l,2,i] for l in L)  <= S[s][i-1][1], "c15")
                     
                    # # Restricción 16: No enviar más de las necesarias y + v para k = 1
                    # for i in I: 
                    #     if S[s][i-1][0] != 0: 
                    #         model.addConstr(gp.quicksum(y_vars[s+1,l,1,i] + v_vars[s+1,l,1,i] for l in L) <= S[s][i-1][0], "c16") 
                            
                    
                    # # Restricción 17: No enviar más de las necesarias y + v para k = 2
                    
                    # for i in I:
                    #     if S[s][i-1][1] != 0:
                    #         model.addConstr(gp.quicksum(y_vars[s+1,l,2,i] + v_vars[s+1,l,2,i] for l in L)  <= S[s][i-1][1], "c17")
                     
                    
                    # # Restricción 18: 
                    # for i in I: 
                    #     if S[s][i-1][0] != 0: 
                    #         model.addConstr(gp.quicksum(y_vars[s+1,l,1,i] for l in L) <= x_vars[l,1], "c18") 
                            
                    
                    # # Restricción 19: 
                    
                    # for i in I:
                    #     if S[s][i-1][1] != 0:
                    #         model.addConstr(gp.quicksum(y_vars[s+1,l,2,i] for l in L)  <= x_vars[l,2], "c19")
                        
                    # # Restricción 20: 
                    # for i in I: 
                    #     if S[s][i-1][0] != 0: 
                    #         model.addConstr(gp.quicksum(v_vars[s+1,l,1,i] for l in L) <= x_vars[l,1], "c20") 
                            
                    
                    # # Restricción 21: 
                    
                    # for i in I:
                    #     if S[s][i-1][1] != 0:
                    #         model.addConstr(gp.quicksum(v_vars[s+1,l,2,i] for l in L)  <= x_vars[l,2], "c21")
                        
                                           
                # objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
                # objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
                # gap = abs((objbst - objbnd) / objbst)     
    
                # Optimize model
                model.optimize(callback=data_cb)
                
                end_time = time.time()
                
                elapsed_time = end_time - model._start 
                
                #imprimir variables 
                
                with open('data_NewModel_NewModel_070224_'+str(len(I))+str('_')
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
                
                
                # model.write('model_NewModel_NewModel_070224_'+str(len(I))+str('_')
                #               +str(len(L))+str('_')
                #               #+str(len(K))+str('_')
                #               #+str(len(N))+str('_')
                #               +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.lp')
                
                # model.write('model_NewModel_NewModel_070224_'+str(len(I))+str('_')
                #               +str(len(L))+str('_')
                #               +str(len(S))+'_'+str(eta[0])+'_'+str(eta[1])+'.mps')
                
                f = open ('Resultados_Prueba_NewModel_NewModel_070224_'
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
                
                archivo.close()
                
                end_time = time.time()
                total_time = end_time - initial_time 
                
                sheet.write(countcsv, 9, total_time)
                
                countcsv = countcsv + 1
                
                
                book.save('Tesis_NewModel_NewModel_070224_'+str(eta[0])+'_'+str(eta[1])+'.csv') 
