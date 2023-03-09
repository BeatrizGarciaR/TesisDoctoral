# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:49:46 2023

@author: beatr
"""

import gurobipy as gp
from gurobipy import GRB
#from statistics import mean
import random 
import numpy as np
import csv
import time
import xlwt
import math

### Info de instancias ###

# tamaños_I = [20, 50, 80]
# tamaños_L = [40, 50, 70]
# tamaños_S = [12, 25, 30]

# tamaños_I = [20]
# tamaños_L = [40]
# tamaños_S = [12]

# tamaños_I = [80]
# tamaños_L = [70]
# tamaños_S = [30]

tamaños_I = [95]
tamaños_L = [100]
tamaños_S = [40]

# tamaños_I = [10]
# tamaños_L = [10]
# tamaños_S = [5]

K = [1, 2]

porcentaje_L1 = 0.85
porcentaje_L2 = 0.75

eta = [20, 11]
t = 10
tmax = 25
wi = [1, 0.85, 0.6, 0.3]
V = [1,2,3]

elapsedtimeStop = 1200
modelStopTime = 60

sumaelapsed = 0

countcsv = 1

alpha_def = 0.30

soluciones = []

book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('TesisTS_GRASP_', cell_overwrite_ok=True)

def data_cb(m, where):
    if where == gp.GRB.Callback.MIP:
        cur_obj = m.cbGet(gp.GRB.Callback.MIP_OBJBST)
        cur_bd = m.cbGet(gp.GRB.Callback.MIP_OBJBND)
        gap = abs((cur_obj - cur_bd) / cur_obj)*100  
        status = gp.GRB.OPTIMAL
        m._data.append(["time", "elapsed time", "best", "best bound", "gap %", "status"])
        m._data.append([time.time() - model._start, model._sumaelapsed, cur_obj, cur_bd, gap, status])
        
        
###########################################################################
################ REPETICIONES DE INSTANCIAS ###############################
###########################################################################

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            
            valorObjetivo = 0
    
            #Nombre: Instancias_Prueba_I_L_S
                
            archivo = open('Instancias_Prueba_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')
                      +str(tamaños_S[sconj])
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
            pi = np.amax(cli)/len(S) + 0.005

            ########################
            ### Solución inicial ###
            ########################  
            
            #initialSolution = []
            
            pickL1 = int(len(L)*porcentaje_L1)
            L1 = random.sample(L, pickL1)
        
            pickL2 = int(len(L)*porcentaje_L2)
            L2 = random.sample(L, pickL2)
            
            # Vamos a ver de esos puntos cuáles tienen más demanda 
            
            demandtype1 = []
            demandtype2 = []
            for i in range(len(I)):
                for k in range(len(K)):
                    demandcount = 0
                    if k == 0:
                        for s in range(len(S)):
                            demandcount += S[s][i][k]
                        demandtype1.append(demandcount)
                    else:
                        for s in range(len(S)):
                            demandcount += S[s][i][k]
                        demandtype2.append(demandcount)
                        
            print("Demand count type 1") # me dice cuántos accidentes hubo
            print(demandtype1)
            print(" ")  
            
            print("Demand count type 2") # me dice cuántos accidentes hubo
            print(demandtype2)
            print(" ") 
            
            puntosCubiertos1 = []
            for l in range(len(L)):
                puntosCubiertos1.append([])
                for i in range(len(I)):
                    if r_li[l][i] < 15:
                        puntosCubiertos1[l].append(i)
            
            puntosCubiertos2 = []
            for l in range(len(L)):
                puntosCubiertos2.append([])
                for i in range(len(I)):
                    if r_li[l][i] < 15:
                        puntosCubiertos2[l].append(i)
                        
            accidentesesperados1 = []      #### ACCIDENTES ESPERADOS DE TODOS LOS SITIOS POTENCIALES
            for potentialsites1 in range(len(L)):
                accidentesConteo1 = 0
                for puntos1 in puntosCubiertos1[potentialsites1]:
                    accidentesConteo1 += demandtype1[puntos1]
                accidentesesperados1.append(accidentesConteo1/len(puntosCubiertos1[potentialsites1]))
            
            accidentesesperados2 = []
            for potentialsites2 in range(len(L)):
                accidentesConteo2 = 0
                for puntos2 in puntosCubiertos2[potentialsites2]:
                    accidentesConteo2 += demandtype2[puntos2]
                accidentesesperados2.append(accidentesConteo2/len(puntosCubiertos2[potentialsites2]))
    
                
            #print(initialSolution)
            
            
            #########################################
            #######3 CONSTRUCT GRASP #############
            ########################################
            
            while sumaelapsed < elapsedtimeStop:
                
                initialSolution = []
                for g in range(len(L)):
                    initialSolution.append([0,0])
                
                LCR1 = []
                restodepuntos1 = []
                if len(L) <= eta[0]:
                    for i in range(len(L)):
                        LCR1.append(i)
                else:
                    funcion_maximo = max(accidentesesperados1)
                    funcion_minimo = min(accidentesesperados1)
                    funcion_diferencia = funcion_maximo - funcion_minimo
                    alpha_mejor = funcion_diferencia * alpha_def
                    #lenLCR1 = max(eta[0], int(len(L)*0.5))
                    for i in range(len(L)):
                        if accidentesesperados1[i] >= (funcion_maximo - alpha_mejor):
                            LCR1.append(i)
                    for l in range(len(L)):
                        if l not in LCR1:
                            restodepuntos1.append(l)  

                LCR2 = []
                restodepuntos2 = []
                if len(L) <= eta[1]:
                    for i in range(len(L)):
                        LCR2.append(i)
                else:
                    funcion_maximo = max(accidentesesperados2)
                    funcion_minimo = min(accidentesesperados2)
                    funcion_diferencia = funcion_maximo - funcion_minimo
                    alpha_mejor = funcion_diferencia * alpha_def
                    #lenLCR1 = max(eta[0], int(len(L)*0.5))
                    for i in range(len(L)):
                        if accidentesesperados2[i] >= (funcion_maximo - alpha_mejor):
                            LCR2.append(i)
                    for l in range(len(L)):
                        if l not in LCR2:
                            restodepuntos2.append(l)
                        
                # LCR2 = []
                # if len(L) <= eta[1]:
                #     for i in range(len(L)):
                #         LCR2.append(i)
                # else:
                #     lenLCR2 = max(eta[1], int(len(L)*0.5))
                #     for i in range(lenLCR2):
                #         indice_LCR2 = accidentesesperados2.index(max(accidentesesperados2))
                #         LCR2.append(indice_LCR2)
                #         accidentesesperados2[indice_LCR2] = -1
                
                #print(LCR1)
                #print(LCR2)
                
                #break
                
                ###### FALTA LLENAR BIEN LA LCR PARA QUE SEA UNA CANTIDAD BUENA DE AMBULANCIAS
                
                contamb1 = 0
                while contamb1 < eta[0]:
                    a = random.uniform(0,1)
                    if eta[0] - contamb1 == 1:
                        if LCR1 != []:
                            b = random.choice(LCR1)
                            LCR1.remove(b)
                        else:
                            b = random.choice(restodepuntos1)
                            restodepuntos1.remove(b)
                        initialSolution[b][0] = 1
                        contamb1 += 1                  
                    else:
                        if a < 0.85: 
                            if LCR1 != []:
                                b = random.choice(LCR1)
                                LCR1.remove(b)
                            else:
                                b = random.choice(restodepuntos1)
                                restodepuntos1.remove(b)
                            initialSolution[b][0] = 1
                            contamb1 += 1
                        else:
                            if LCR1 != []:
                                b = random.choice(LCR1)
                                LCR1.remove(b)
                            else:
                                b = random.choice(restodepuntos1)
                                restodepuntos1.remove(b)
                            initialSolution[b][0] = 2
                            contamb1 += 2
                            
                contamb2 = 0
                while contamb2 < eta[1]:
                    a = random.uniform(0,1)
                    if eta[1] - contamb2 == 1:
                        if LCR2 != []:
                            b = random.choice(LCR2)
                            LCR2.remove(b)
                        else:
                            b = random.choice(restodepuntos2)
                            restodepuntos2.remove(b)
                        initialSolution[b][1] = 1
                        contamb2 += 1                  
                    else:
                        if a < 0.85: 
                            if LCR2 != []:
                                b = random.choice(LCR2)
                                LCR2.remove(b)
                            else:
                                b = random.choice(restodepuntos2)
                                restodepuntos2.remove(b)
                            initialSolution[b][1] = 1
                            contamb2 += 1
                        else:
                            if LCR2 != []:
                                b = random.choice(LCR2)
                                LCR2.remove(b)
                            else:
                                b = random.choice(restodepuntos2)
                                restodepuntos2.remove(b)
                            initialSolution[b][1] = 2
                            contamb2 += 2
                
    
                # Solamente se asignan 1 y 2... hay que modificar eso
                print("La solucion inicial final es ")
                print(initialSolution)
                print(" ")
                print( " ")
                
                #break
                
                soluciones.append(initialSolution)
    
                with open('SolutionX_GRASP_'+str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.csv', 'w') as solutionX:            
                    solutionX.write(str(initialSolution))
                    solutionX.write('\n')
                
                potentialSiteActivos = []
                for i in range(len(initialSolution)):
                    if any(initialSolution[i]):
                        potentialSiteActivos.append(i)
                print(potentialSiteActivos)
                
                #break 
                
                ######################################################################
                ######################    MODEL   ####################################
                ######################################################################
                
                model = gp.Model("TabuSearchWithSAA")            
                model.setParam('TimeLimit', modelStopTime)
                model._obj = None
                model._bd = None
                model._data = []
                model._start = time.time()
                #model._sumaelapsed = None
                
                #sumaelapsed = 0
                
                # Create variables #
                y_vars = {}    
                cantVarY = 0
                for s in range(len(S)):        
                    for l in L:
                        if initialSolution[l-1][0] > 0:
                            for i in I:
                                if S[s][i-1][0] != 0:
                                    y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                    name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                    cantVarY += 1
                                  
                        if initialSolution[l-1][1] > 0:
                            for i in I:
                                for k in K:
                                    if S[s][i-1][1] != 0:
                                        y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                         name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                        cantVarY += 1
                                    if S[s][i-1][0] != 0:
                                        y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                                                         name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(k)+str(' ')+str(i))
                                        cantVarY += 1
 
                alpha_vars = {}  ## z full
                cantVarAlpha = 0
                for s in range(len(S)):
                    for i in I:
                        if S[s][i-1][0] != 0:
                            alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Full "+str(s+1)+str(' ')+str(i))
                            cantVarAlpha += 1
                        if S[s][i-1][1] != 0:
                            alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Full "+str(s+1)+str(' ')+str(i))
                            cantVarAlpha += 1
                
                beta_vars = {}  ## z partial 1
                cantVarBeta = 0
                for s in range(len(S)):
                    for i in I:
                        if S[s][i-1][0] != 0:
                            beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial1 "+str(s+1)+str(' ')+str(i))
                            cantVarBeta += 1
                        if S[s][i-1][1] != 0:
                            beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial1 "+str(s+1)+str(' ')+str(i))
                            cantVarBeta += 1
                
                delta_vars = {}  ## z partial 2
                cantVarDelta = 0
                for s in range(len(S)):
                    for i in I:
                        if S[s][i-1][0] != 0:
                            delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial2 "+str(s+1)+str(' ')+str(i))
                            cantVarDelta += 1
                        if S[s][i-1][1] != 0:
                            delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial2 "+str(s+1)+str(' ')+str(i))
                            cantVarDelta += 1
                
                phi_vars = {}   ## z partial 3
                cantVarPhi = 0
                for s in range(len(S)):
                    for i in I:
                        if S[s][i-1][0] != 0:
                            phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial3 "+str(s+1)+str(' ')+str(i))
                            cantVarPhi += 1
                        if S[s][i-1][1] != 0:
                            phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                      name="Partial3 "+str(s+1)+str(' ')+str(i))
                            cantVarPhi += 1
                
                gamma_vars = {} ## z null
                cantVarGamma = 0
                for s in range(len(S)):
                    for i in I:
                        if S[s][i-1][0] != 0:
                            gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                     name="Null "+str(s+1)+str(' ')+str(i))
                            cantVarGamma += 1
                        if S[s][i-1][1] != 0:
                            gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                     name="Null "+str(s+1)+str(' ')+str(i))
                            cantVarGamma += 1
            
                obj = gp.LinExpr()
                for s in range(len(S)):
                    for i in I:
                        if S[s][i-1][0]:
                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                        if S[s][i-1][1]:
                            obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                model.setObjective(obj, GRB.MAXIMIZE)  
            
            
                ## Add constraints 
                
                for s in range(len(S)):
                    
                    for l in L:
                        for k in K:
                            if k == 1 and initialSolution[l-1][k-1] != 0:
                                suma = 0
                                for i in I:
                                    if S[s][i-1][0] != 0:
                                        suma += y_vars[s+1,l,1,i]
                                model.addConstr(suma <= initialSolution[l-1][k-1], "c3")
                            
                            if k == 2 and initialSolution[l-1][k-1] != 0:
                                suma = 0
                                for i in I:
                                    if S[s][i-1][0] != 0:
                                        suma += y_vars[s+1,l,1,i]
                                    if S[s][i-1][1] != 0:
                                        suma += y_vars[s+1,l,k,i] 
                                model.addConstr(suma <= initialSolution[l-1][k-1], "c4")
                                  
                    for i in I:
                        if S[s][i-1][0] + S[s][i-1][1] != 0:
                            suma = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                            model.addConstr(suma - (S[s][i-1][0]+S[s][i-1][1]) <= alpha_vars[s+1,i] - 1, "c7")
                  
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                            model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma, "c8")             

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma = 0
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr(2*suma1 - suma - (S[s][i-1][0]+S[s][i-1][1]) <= (S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i], "c9" )

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma1, "c_10")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr(suma1 - 1 <= (S[s][i-1][0]+S[s][i-1][1])*delta_vars[s+1,i], "c_11")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr(delta_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_12")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma = 0
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr(suma1*delta_vars[s+1,i] <= suma, "c_13")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma = 0
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                             suma1 += y_vars[s+1,l,k,i]  
                            model.addConstr(suma1 - suma <= (S[s][i-1][0]+S[s][i-1][1])*phi_vars[s+1,i], "c_14")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr(phi_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_15")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma = 0
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                             suma1 += y_vars[s+1,l,k,i]  
                            model.addConstr(np.amin(cli)*phi_vars[s+1,i] <= suma1 - suma, "c_16")

                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            suma1 = 0
                            for l in L:
                                if initialSolution[l-1][0] != 0:
                                    if S[s][i-1][0] != 0:
                                        suma1 += y_vars[s+1,l,1,i] 
                                if initialSolution[l-1][1] != 0:
                                    for k in K:
                                         if S[s][i-1][1] != 0:
                                             suma1 += y_vars[s+1,l,2,i] 
                                         if S[s][i-1][0] != 0:
                                             suma1 += y_vars[s+1,l,k,i] 
                            model.addConstr(suma1 + gamma_vars[s+1,i] >= 1, "c_17")
 
                    for i in I:
                        if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                            model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_18")
            
                # Optimize model
                
                end_time = time.time()
                
                elapsed_time = end_time - model._start
                
                sumaelapsed = sumaelapsed + elapsed_time
                
                model._sumaelapsed = sumaelapsed
                
                model.optimize(callback=data_cb)
                
                #imprimir variables 
    
                colnames = ["name", "I size", "L size", "S size", "time", "elapsed time", "best obj", "best bound", "gap %"]
                for column in range(len(colnames)):
                    sheet.write(0, column, colnames[column])
                name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')+str(len(S))
                sheet.write(countcsv, 0, name)
                sheet.write(countcsv, 1, len(I))
                sheet.write(countcsv, 2, len(L))
                sheet.write(countcsv, 3, len(S))
                if len(model._data) != 0:
                    print(" Entra datos for ")
                    datos = model._data[len(model._data)-1]
                    for row in range(len(datos)):
                        sheet.write(countcsv, row+4, datos[row])
                countcsv = countcsv + 1
            
                with open('data_GRASP_'+str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.csv', 'w') as fi:
                        writer = csv.writer(fi)
                        writer.writerows(model._data)
                
                #Nombre: Resultados_Prueba_I_L_M_N_S
                
                f = open ('Resultados_Prueba_GRASP_'
                              +str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.txt','w')
                
                f.write("Elapsed time: ")
                f.write(str(elapsed_time))
                f.write('\n')
            
                        
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
                
                break
                
                ### LEER AQUI ARCHIVO DE RESULTADO Y CONTAR LAS COBERTURAS
                
                coberturas = open ('Coberturas_GRASP_'
                              +str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.txt','w')                      
                
                lectura = open ('Resultados_Prueba_GRASP_'
                              +str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.txt','r')
                lectura.readline()
                lectura.readline()
                
                for salto in range(cantVarY):
                    lectura.readline()
                 
                coberturaTotal = 0
                for salto1 in range(cantVarAlpha):
                    line = lectura.readline()
                    if int(line[len(line)-2]) == 1:
                        coberturaTotal += 1
                coberturas.write(str(coberturaTotal/TotalAccidentes))
                coberturas.write('\n')
    
                coberturaParcial1 = 0
                for salto2 in range(cantVarBeta):
                    line = lectura.readline()
                    if int(line[len(line)-2]) == 1:
                        coberturaParcial1 += 1
                coberturas.write(str(coberturaParcial1/TotalAccidentes))
                coberturas.write('\n')
                
                coberturaParcial2 = 0
                for salto3 in range(cantVarDelta):
                    line = lectura.readline()
                    if int(line[len(line)-2]) == 1:
                        coberturaParcial2 += 1
                coberturas.write(str(coberturaParcial2/TotalAccidentes))
                coberturas.write('\n')
                
                coberturaParcial3 = 0
                for salto4 in range(cantVarPhi):
                    line = lectura.readline()
                    if int(line[len(line)-2]) == 1:
                        coberturaParcial3 += 1
                coberturas.write(str(coberturaParcial3/TotalAccidentes))
                coberturas.write('\n')
    
                coberturaNula = 0
                for salto5 in range(cantVarGamma):
                    line = lectura.readline()
                    if int(line[len(line)-2]) == 1:
                        coberturaNula += 1
                coberturas.write(str(coberturaNula/TotalAccidentes))
                coberturas.write('\n')
                
                coberturas.write(str(-1))
                coberturas.write('\n')
                
                lectura.close()
                
                archivo.close()
                
                model.write('model_GRASP_'+str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.lp')
                model.write('model_GRASP_'+str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.mps')
                        
                #break 
                
                #valorObjetivo = model.objVal
                
                
                if model.objVal > valorObjetivo:
                    print("   ")
                    print("   ")
                    print("entra if better solution del GRASP")
                    print("   ")
                    #print(initialSolution)
                    
                    soluciones.append(initialSolution)
                    
                    with open('SolutionX_GRASP_'+str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.csv', 'a') as solutionX:            
                        solutionX.write(str(initialSolution))
                        solutionX.write('\n')
                    
                    potentialSiteActivos = []
                    for i in range(len(initialSolution)):
                        if any(initialSolution[i]):
                            potentialSiteActivos.append(i)
                    print(potentialSiteActivos)
                    
                    valorObjetivo = model.objVal
                    print("   ")
                    print("   ")
                    
                    mejoras = open ("mejoras_GRASP_"
                              +str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.txt','a')
                    
                    mejoras.write('mejoró %g' % model.objVal + '  GRASP' )
                    mejoras.write('\n')
                    
                    
                    colnames = ["name", "I size", "L size", "S size", "time", "elapsed time", "best obj", "best bound", "gap %"]
                    for column in range(len(colnames)):
                        sheet.write(0, column, colnames[column])
                    name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')+str(len(S))
                    sheet.write(countcsv, 0, name)
                    sheet.write(countcsv, 1, len(I))
                    sheet.write(countcsv, 2, len(L))
                    sheet.write(countcsv, 3, len(S))
                    if len(model._data) != 0:
                        print("Entra datos for 2")
                        datos = model._data[len(model._data)-1]
                        for row in range(len(datos)):
                            sheet.write(countcsv, row+4, datos[row])
                    countcsv = countcsv + 1
                    
                
                    coberturas = open ('Coberturas_GRASP_'
                                  +str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.txt','a')                      
                    
                    lectura = open ('Resultados_Prueba_GRASP_'
                                  +str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.txt','r')
                    lectura.readline()
                    lectura.readline()
                    
                    for salto in range(cantVarY):
                        lectura.readline()
                     
                    coberturaTotal = 0
                    for salto1 in range(cantVarAlpha):
                        line = lectura.readline()
                        if int(line[len(line)-2]) == 1:
                            coberturaTotal += 1
                    coberturas.write(str(coberturaTotal/TotalAccidentes))
                    coberturas.write('\n')
        
                    coberturaParcial1 = 0
                    for salto2 in range(cantVarBeta):
                        line = lectura.readline()
                        if int(line[len(line)-2]) == 1:
                            coberturaParcial1 += 1
                    coberturas.write(str(coberturaParcial1/TotalAccidentes))
                    coberturas.write('\n')
                    
                    coberturaParcial2 = 0
                    for salto3 in range(cantVarDelta):
                        line = lectura.readline()
                        if int(line[len(line)-2]) == 1:
                            coberturaParcial2 += 1
                    coberturas.write(str(coberturaParcial2/TotalAccidentes))
                    coberturas.write('\n')
                    
                    coberturaParcial3 = 0
                    for salto4 in range(cantVarPhi):
                        line = lectura.readline()
                        if int(line[len(line)-2]) == 1:
                            coberturaParcial3 += 1
                    coberturas.write(str(coberturaParcial3/TotalAccidentes))
                    coberturas.write('\n')
        
                    coberturaNula = 0
                    for salto5 in range(cantVarGamma):
                        line = lectura.readline()
                        if int(line[len(line)-2]) == 1:
                            coberturaNula += 1
                    coberturas.write(str(coberturaNula/TotalAccidentes))
                    coberturas.write('\n')
                    
                    coberturas.write(str(-1))
                    coberturas.write('\n')
                    
                    lectura.close()
                                        
   
                ####################################
                ####### LOCAL SEARCH ###############
                ####################################
                
                localsearch = 0
                
                mejoras = open ("mejoras_GRASP_"
                                +str(len(I))+str('_')
                                +str(len(L))+str('_')
                                +str(len(S))+'.txt','a')
                
                initialL_lista = []
                while(1):
                    localsearch += 1
                    vecindad = []
                    
                    (" Entra al while de nuevo ")
                    print(" ")
                    
                    for initialL in range(len(L)): 
                        if initialL in potentialSiteActivos and initialL not in initialL_lista:
                            initialL_lista.append(initialL)
                            aux = initialSolution[initialL][0]
                            aux1 = initialSolution[initialL][1]
                            for j in range(len(L)):
                                #if j != initialL:
                                #if j not in potentialSiteActivos:  #LS1
                                #if j in potentialSiteActivos and j != initialL: #LS2
                            
                                    # breakaux = 0
                                    
                                    # initialSolution[j][0] += initialSolution[initialL][0]
                                    # initialSolution[j][1] += initialSolution[initialL][1]
                                    # initialSolution[initialL][0] = 0
                                    # initialSolution[initialL][1] = 0
                                
                                    
                                if j in potentialSiteActivos and j != initialL: #LS3
                                
                                    breakaux = 0
                                    
                                    if aux + aux1 > 1:
                                        if aux > 1:
                                            initialSolution[j][0] += math.floor(aux/2)
                                            initialSolution[initialL][0] -= math.floor(aux/2)
                                        if aux1 > 1:
                                            initialSolution[j][1] += math.floor(aux1/2)
                                            initialSolution[initialL][1] -= math.floor(aux1/2)
                                  
                                    
                                  
                                    print ("initial solution de potentialSiteActivos")
                                    print(" ")
                                    print(initialSolution)                                
           
                                    model = gp.Model("TabuSearchWithSAA")            
                                    model.setParam('TimeLimit', modelStopTime)
                                    model._obj = None
                                    model._bd = None
                                    model._data = []
                                    model._start = time.time()
                                    
                                    # Create variables #
                                    y_vars = {}    
                                    cantVarY = 0
                                    for s in range(len(S)):        
                                        for l in L:
                                            if initialSolution[l-1][0] > 0:
                                                for i in I:
                                                    if S[s][i-1][0] != 0:
                                                        y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                        name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                                        cantVarY += 1
                                                      
                                            if initialSolution[l-1][1] > 0:
                                                for i in I:
                                                    for k in K:
                                                        if S[s][i-1][1] != 0:
                                                            y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                                              name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                                            cantVarY += 1
                                                        if S[s][i-1][0] != 0:
                                                            y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                                                                              name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(k)+str(' ')+str(i))
                                  
                                    alpha_vars = {}  ## z full
                                    cantVarAlpha = 0
                                    for s in range(len(S)):
                                        for i in I:
                                            if S[s][i-1][0] != 0:
                                                alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Full "+str(s+1)+str(' ')+str(i))
                                                cantVarAlpha += 1
                                            if S[s][i-1][1] != 0:
                                                alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Full "+str(s+1)+str(' ')+str(i))
                                                cantVarAlpha += 1
                                    
                                    beta_vars = {}  ## z partial 1
                                    cantVarBeta = 0
                                    for s in range(len(S)):
                                        for i in I:
                                            if S[s][i-1][0] != 0:
                                                beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Partial1 "+str(s+1)+str(' ')+str(i))
                                                cantVarBeta += 1
                                            if S[s][i-1][1] != 0:
                                                beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Partial1 "+str(s+1)+str(' ')+str(i))
                                                cantVarBeta += 1
                                    
                                    delta_vars = {}  ## z partial 2
                                    cantVarDelta = 0
                                    for s in range(len(S)):
                                        for i in I:
                                            if S[s][i-1][0] != 0:
                                                delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Partial2 "+str(s+1)+str(' ')+str(i))
                                                cantVarDelta += 1
                                            if S[s][i-1][1] != 0:
                                                delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Partial2 "+str(s+1)+str(' ')+str(i))
                                                cantVarDelta += 1
                                    
                                    phi_vars = {}   ## z partial 3
                                    cantVarPhi = 0
                                    for s in range(len(S)):
                                        for i in I:
                                            if S[s][i-1][0] != 0:
                                                phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Partial3 "+str(s+1)+str(' ')+str(i))
                                                cantVarPhi += 1
                                            if S[s][i-1][1] != 0:
                                                phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Partial3 "+str(s+1)+str(' ')+str(i))
                                                cantVarPhi += 1
                                    
                                    gamma_vars = {} ## z null
                                    cantVarGamma = 0
                                    for s in range(len(S)):
                                        for i in I:
                                            if S[s][i-1][0] != 0:
                                                gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Null "+str(s+1)+str(' ')+str(i))
                                                cantVarGamma += 1
                                            if S[s][i-1][1] != 0:
                                                gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                                          name="Null "+str(s+1)+str(' ')+str(i))
                                                cantVarGamma += 1   
                                                
                                    obj = gp.LinExpr()
                                    for s in range(len(S)):
                                        for i in I:
                                            if S[s][i-1][0]:
                                                obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                            if S[s][i-1][1]:
                                                obj += (wi[0]*alpha_vars[s+1,i] + wi[1]*beta_vars[s+1,i] + wi[2]*delta_vars[s+1,i] + wi[3]*phi_vars[s+1,i] - pi*gamma_vars[s+1,i]) * (1/len(S))
                                    model.setObjective(obj, GRB.MAXIMIZE)  
                                
                                
                                    ## Add constraints 
                                    
                                    for s in range(len(S)):
                                        
                                        for l in L:
                                            for k in K:
                                                if k == 1 and initialSolution[l-1][k-1] != 0:
                                                    suma = 0
                                                    for i in I:
                                                        if S[s][i-1][0] != 0:
                                                            suma += y_vars[s+1,l,1,i]
                                                    model.addConstr(suma <= initialSolution[l-1][k-1], "c3")
                                                
                                                if k == 2 and initialSolution[l-1][k-1] != 0:
                                                    suma = 0
                                                    for i in I:
                                                        if S[s][i-1][0] != 0:
                                                            suma += y_vars[s+1,l,1,i]
                                                        if S[s][i-1][1] != 0:
                                                            suma += y_vars[s+1,l,k,i] 
                                                    model.addConstr(suma <= initialSolution[l-1][k-1], "c4")
    
                                        for i in I:
                                            if S[s][i-1][0] + S[s][i-1][1] != 0:
                                                suma = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                                model.addConstr(suma - (S[s][i-1][0]+S[s][i-1][1]) <= alpha_vars[s+1,i] - 1, "c7")
                                                                                   
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                                model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma, "c8")             
                                                                         
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma = 0
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr(2*suma1 - suma - (S[s][i-1][0]+S[s][i-1][1]) <= (S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i], "c9" )
                                                                   
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma1, "c_10")
                                                
                      
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr(suma1 - 1 <= (S[s][i-1][0]+S[s][i-1][1])*delta_vars[s+1,i], "c_11")
                                                                             
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr(delta_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_12")
                                            
                                                
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma = 0
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr(suma1*delta_vars[s+1,i] <= suma, "c_13")
                                            
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma = 0
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                                                  suma1 += y_vars[s+1,l,k,i]  
                                                model.addConstr(suma1 - suma <= (S[s][i-1][0]+S[s][i-1][1])*phi_vars[s+1,i], "c_14")
                                            
                       
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr(phi_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_15")
                                            
                       
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma = 0
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma += cli[l-1][i-1]*y_vars[s+1,l,1,i] 
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,2,i] 
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma += cli[l-1][i-1]*y_vars[s+1,l,k,i] 
                                                                  suma1 += y_vars[s+1,l,k,i]  
                                                model.addConstr(np.amin(cli)*phi_vars[s+1,i] <= suma1 - suma, "c_16")
                                            
                  
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                suma1 = 0
                                                for l in L:
                                                    if initialSolution[l-1][0] != 0:
                                                        if S[s][i-1][0] != 0:
                                                            suma1 += y_vars[s+1,l,1,i] 
                                                    if initialSolution[l-1][1] != 0:
                                                        for k in K:
                                                              if S[s][i-1][1] != 0:
                                                                  suma1 += y_vars[s+1,l,2,i] 
                                                              if S[s][i-1][0] != 0:
                                                                  suma1 += y_vars[s+1,l,k,i] 
                                                model.addConstr(suma1 + gamma_vars[s+1,i] >= 1, "c_17")
                                            
          
                                        for i in I:
                                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                                model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_18")
                                    
                                    # Optimize model
                                    
                                    end_time = time.time()
                                    
                                    elapsed_time = end_time - model._start
                                    
                                    sumaelapsed = sumaelapsed + elapsed_time
                                    
                                    model._sumaelapsed = sumaelapsed
                                    
                                    model.optimize(callback=data_cb)
                                    
                                    print(" ")
                                    print(" ")
                                    print("suma elapsed = " , sumaelapsed)
                                    print(" ")
                                    print(" ")
                                    
                                    #imprimir variables 
                                
                                    #writer.writerows(name)
                                    with open('data_GRASP_'+str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  +str(len(S))+'.csv', 'a') as f: #Cambiar de w a a
                                        writer = csv.writer(f)
                                        writer.writerows("new")
                                        writer.writerows(model._data)
                                    
                                    #Nombre: Resultados_Prueba_I_L_M_N_S
                                    
                                    f = open ('Resultados_Prueba_GRASP_'
                                                  +str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  +str(len(S))+'.txt','w')
                                    
                                    f.write("Elapsed time: ")
                                    f.write(str(elapsed_time))
                                    f.write('\n')
                                
                                            
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
                                                        
    
                                    
                                    archivo.close()
                                    
                                    model.write('model_GRASP_'+str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  +str(len(S))+'.lp')
                                    model.write('model_GRASP_'+str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  +str(len(S))+'.mps')
                                    
                                    mejoras = open ("mejoras_GRASP_"
                                                  +str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  +str(len(S))+'.txt','a')
                                        
                                    
                                    if model.objVal > valorObjetivo:
                                        print("   ")
                                        print("   ")
                                        print("entra if better solution", localsearch)
                                        print("   ")
                                        #print(initialSolution)
                                        
                                        soluciones.append(initialSolution)
                                        
                                        with open('SolutionX_GRASP_'+str(len(I))+str('_')
                                                      +str(len(L))+str('_')
                                                      +str(len(S))+'.csv', 'a') as solutionX:            
                                            solutionX.write(str(initialSolution))
                                            solutionX.write('\n')
                                        
                                        potentialSiteActivos = []
                                        for i in range(len(initialSolution)):
                                            if any(initialSolution[i]):
                                                potentialSiteActivos.append(i)
                                        print(potentialSiteActivos)
                                        
                                        valorObjetivo = model.objVal
                                        print("   ")
                                        print("   ")
                                        
                                        mejoras = open ("mejoras_GRASP_"
                                                  +str(len(I))+str('_')
                                                  +str(len(L))+str('_')
                                                  +str(len(S))+'.txt','a')
                                        
                                        mejoras.write('mejoró %g' % model.objVal + ' en initial L '+ str(initialL) + ' con j = ' + str(j) + ' localsearch ' + str(localsearch))
                                        mejoras.write('\n')
                                        
                                        
                                        colnames = ["name", "I size", "L size", "S size", "time", "elapsed time", "best obj", "best bound", "gap %"]
                                        for column in range(len(colnames)):
                                            sheet.write(0, column, colnames[column])
                                        name = str('Instance')+str('_')+str(len(I))+str('_')+str(len(L))+str('_')+str(len(S))
                                        sheet.write(countcsv, 0, name)
                                        sheet.write(countcsv, 1, len(I))
                                        sheet.write(countcsv, 2, len(L))
                                        sheet.write(countcsv, 3, len(S))
                                        if len(model._data) != 0:
                                            print("Entra datos for 2")
                                            datos = model._data[len(model._data)-1]
                                            for row in range(len(datos)):
                                                sheet.write(countcsv, row+4, datos[row])
                                        countcsv = countcsv + 1
                                        
                                    
                                        coberturas = open ('Coberturas_GRASP_'
                                                      +str(len(I))+str('_')
                                                      +str(len(L))+str('_')
                                                      +str(len(S))+'.txt','a')                      
                                        
                                        lectura = open ('Resultados_Prueba_GRASP_'
                                                      +str(len(I))+str('_')
                                                      +str(len(L))+str('_')
                                                      +str(len(S))+'.txt','r')
                                        lectura.readline()
                                        lectura.readline()
                                        
                                        for salto in range(cantVarY):
                                            lectura.readline()
                                         
                                        coberturaTotal = 0
                                        for salto1 in range(cantVarAlpha):
                                            line = lectura.readline()
                                            if int(line[len(line)-2]) == 1:
                                                coberturaTotal += 1
                                        coberturas.write(str(coberturaTotal/TotalAccidentes))
                                        coberturas.write('\n')
                            
                                        coberturaParcial1 = 0
                                        for salto2 in range(cantVarBeta):
                                            line = lectura.readline()
                                            if int(line[len(line)-2]) == 1:
                                                coberturaParcial1 += 1
                                        coberturas.write(str(coberturaParcial1/TotalAccidentes))
                                        coberturas.write('\n')
                                        
                                        coberturaParcial2 = 0
                                        for salto3 in range(cantVarDelta):
                                            line = lectura.readline()
                                            if int(line[len(line)-2]) == 1:
                                                coberturaParcial2 += 1
                                        coberturas.write(str(coberturaParcial2/TotalAccidentes))
                                        coberturas.write('\n')
                                        
                                        coberturaParcial3 = 0
                                        for salto4 in range(cantVarPhi):
                                            line = lectura.readline()
                                            if int(line[len(line)-2]) == 1:
                                                coberturaParcial3 += 1
                                        coberturas.write(str(coberturaParcial3/TotalAccidentes))
                                        coberturas.write('\n')
                            
                                        coberturaNula = 0
                                        for salto5 in range(cantVarGamma):
                                            line = lectura.readline()
                                            if int(line[len(line)-2]) == 1:
                                                coberturaNula += 1
                                        coberturas.write(str(coberturaNula/TotalAccidentes))
                                        coberturas.write('\n')
                                        
                                        coberturas.write(str(-1))
                                        coberturas.write('\n')
                                        
                                        lectura.close()
                                        
                                        breakaux = 1
                                        
                                        break
                                    
                                    # else:
                                        
                                    #     mejoras.write('no mejoró %g' % model.objVal + ' en initial L '+ str(initialL) + ' con j = ' + str(j) + ' localsearch ' + str(localsearch))
                                    #     mejoras.write('\n')
                                    #     print("entra else que repite solution")
                                    #     print(" ")
                                    #     print(" ")
                                    #     initialSolution[initialL][0] = aux
                                    #     initialSolution[initialL][1] = aux1
                                    #     initialSolution[j][0] = 0
                                    #     initialSolution[j][1] = 0
                                    #     # print(initialSolution)
                                    #     # print(" ")
                                    #     # print(" ")
                                    
                                    else:
                                        
                                        mejoras.write('no mejoró %g' % model.objVal + ' en initial L '+ str(initialL) + ' con j = ' + str(j) + ' localsearch ' + str(localsearch))
                                        mejoras.write('\n')
                                        print("entra else que repite solution")
                                        print(" ")
                                        print(" ")
                                        initialSolution[initialL][0] = aux
                                        initialSolution[initialL][1] = aux1
                                        initialSolution[j][0] -= math.floor(aux/2)
                                        initialSolution[j][1] -= math.floor(aux1/2)
                                        # print(initialSolution)
                                        # print(" ")
                                        # print(" ")
                                        
                                    if sumaelapsed > elapsedtimeStop:
                                            print("   ")
                                            print("   ")
                                            print("entra if de elapsed", localsearch)
                                            print("   ")
                                            print("   ")
                                            break
                                        
                            if breakaux == 1:    
                                print ("break de breakaux") 
                                print(" ")
                                print(" ")
                                break 
                            # print ("break de potentialSiteActivos") 
                            # print(" ")
                            # print(" ")
                            # break 
                        
                            if sumaelapsed > elapsedtimeStop :
                                print("   ")
                                print("   ")
                                print("entra if de elapsed", localsearch)
                                print("   ")
                                print("   ")
                                break    
       
                    #break 
                    
                    if initialL == len(L)-1:
                        print ("break de initialL") 
                        print(" ")
                        print(" ")
                        break
                        
                    if sumaelapsed > elapsedtimeStop :
                        print("   ")
                        print("   ")
                        print("entra if de elapsed", localsearch)
                        print("   ")
                        print("   ")
                        break   
                    
                # if initialL == len(L)-1:
                #         print ("break de initialL") 
                #         print(" ")
                #         print(" ")
                #         break
            
        countcsv += 3
        sheet.write(countcsv, 1,"newinstance")
        countcsv += 3
  

initial1 = 0
initial2 = 0
for sol in range(len(initialSolution)):
    for solK in range(len(K)):
        if solK == 0:
            initial1 += initialSolution[sol][solK]
        else:
            initial2 += initialSolution[sol][solK]
         
print("amb tipo 1 = ", initial1, "  eta 1 = ", eta[0])
print("amb tipo 2 = ", initial2, "  eta 2 = ", eta[1])
            
    
print("Elapsed time total ")
print(sumaelapsed)
print(" ")

sheet.write(countcsv+1, 0, "Total Elapsed Time")
sheet.write(countcsv+1, 1, sumaelapsed)
fi.close()
book.save('TesisTS_GRASP_.xls') 
solutionX.close()
coberturas.close()
mejoras.close()
            
  