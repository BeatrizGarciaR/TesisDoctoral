# -*- coding: utf-8 -*-
"""
Created on Nov 03 2022

@author: beatr
"""

import gurobipy as gp
from gurobipy import GRB
from statistics import mean
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

# tamaños_I = [1000]
# tamaños_L = [85]
# tamaños_S = [100]

tamaños_I = [50]
tamaños_L = [50]
tamaños_S = [25]

K = [1, 2]

porcentaje_L1 = 0.85
porcentaje_L2 = 0.75

eta = [20, 11]
t = 10
tmax = 25
wi = [1, 0.85, 0.6, 0.3]
V = [1,2,3]

countcsv = 1

book=xlwt.Workbook(encoding="utf-8",style_compression=0)
sheet = book.add_sheet('Tesis', cell_overwrite_ok=True)

def data_cb(m, where):
    if where == gp.GRB.Callback.MIP:
        cur_obj = m.cbGet(gp.GRB.Callback.MIP_OBJBST)
        cur_bd = m.cbGet(gp.GRB.Callback.MIP_OBJBND)
        gap = abs((cur_obj - cur_bd) / cur_obj)*100  
        status = gp.GRB.OPTIMAL
        m._data.append(["time", "best", "best bound", "gap %", "status"])
        m._data.append([time.time() - model._start, cur_obj, cur_bd, gap, status])
        
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
            
            initialSolution = []
            
            pickL1 = int(len(L)*porcentaje_L1)
            L1 = random.sample(L, pickL1)
        
            pickL2 = int(len(L)*porcentaje_L2)
            L2 = random.sample(L, pickL2)


            Cobertura1 = []
            puntosCubiertos1 = []
            for l in range(len(L)):
                coberturaDemanda = 0
                puntosCubiertos1.append([])
                for i in range(len(I)):
                    if r_li[l][i] < 15:
                        coberturaDemanda += 1
                        puntosCubiertos1[l].append(i)
                Cobertura1.append(coberturaDemanda)
                
            # print("puntos cubiertos 1") # demand points 
            # print(puntosCubiertos1)
            # print(" ")
            
            # print("Cantidad Cobertura") # how many demand points 
            # print(Cobertura1)
            # print( " ")
            
            Cobertura2 = []
            puntosCubiertos2 = []
            for l in range(len(L)):
                coberturaDemanda = 0
                puntosCubiertos2.append([])
                for i in range(len(I)):
                    if r_li[l][i] < 15:
                        coberturaDemanda += 1
                        puntosCubiertos2[l].append(i)
                Cobertura2.append(coberturaDemanda)
                
            # print("puntos cubiertos 2") #demand points
            # print(puntosCubiertos2)
            # print(" ")
            
            # print("Cantidad Cobertura 2") # how many demand points 
            # print(Cobertura2)
            # print( " ")
            
            
            initialSolution1 = []
            initialSolution2 = []
            
            
            for i in range(math.ceil(len(L)*(0.5))): 
                
                cantidadCobertura1 = []
                for l in range(len(L)):
                    cantidadCobertura1.append(len(puntosCubiertos1[l]))
                    
                # print("Cantidad Cobertura 1")
                # print(cantidadCobertura1)
                # print( " ")
                    
                cantidadCobertura2 = []
                for l in range(len(L)):
                    cantidadCobertura2.append(len(puntosCubiertos2[l]))
                    
                # print("Cantidad Cobertura 2")
                # print(cantidadCobertura2)
                # print( " ")
                
                
                if any(cantidadCobertura1): #Se llena el arreglo de initsol
                                            #hsta que ya se cubren todos los puntos
                
                    maxtipo1 = max(cantidadCobertura1)
                    indicemaxTipo1 = cantidadCobertura1.index(maxtipo1)
                    Cobertura1[indicemaxTipo1] = -1
                    #print(indicemaxTipo1)
                    #print(puntosCubiertos1[indicemaxTipo1])
                    
                    maxtipo2 = max(cantidadCobertura2)
                    indicemaxTipo2 = cantidadCobertura2.index(maxtipo2)
                    Cobertura2[indicemaxTipo2] = -1
                    #print(indicemaxTipo2)
                    #print(puntosCubiertos2[indicemaxTipo2])
                    
                    initialSolution1.append(indicemaxTipo1)
                    initialSolution2.append(indicemaxTipo2)
                    
                    # print("la solucion inicial es ") 
                    # print(initialSolution1)
                    # print(initialSolution2)
                    # print(" ")
                    
                    puntosCubiertosAux1 = puntosCubiertos1[indicemaxTipo1]
                    for puntoAeliminar1 in range(len(puntosCubiertosAux1)):
                        #print("for 1 ", puntoAeliminar1)
                        #print("punto a eliminar 1 ", puntosCubiertosAux1[0])
                        #print(" ")
                        for puntosCubiertos in range(len(puntosCubiertos1)):
                            # print("entra otro for ", puntosCubiertos)
                            # print(" ")
                            if puntosCubiertosAux1[0] in puntosCubiertos1[puntosCubiertos] and puntosCubiertos != indicemaxTipo1:
                                puntosCubiertos1[puntosCubiertos].remove(puntosCubiertosAux1[0])
                        puntosCubiertos1[indicemaxTipo1].remove(puntosCubiertosAux1[0])
     
                    
                    # print("Nuevos puntos cubiertos 1")
                    # print(puntosCubiertos1)
                    # print(" ")
                    
                    puntosCubiertosAux2 = puntosCubiertos2[indicemaxTipo2]
                    for puntoAeliminar2 in range(len(puntosCubiertosAux2)):
                        #print("for 2 ", puntoAeliminar2)
                        #print("punto a eliminar 2 ", puntosCubiertosAux2[0])
                        #print(" ")
                        for puntosCubiertos in range(len(puntosCubiertos2)):
                            # print("entra otro for ", puntosCubiertos)
                            # print(" ")
                            if puntosCubiertosAux2[0] in puntosCubiertos2[puntosCubiertos] and puntosCubiertos != indicemaxTipo2:
                                puntosCubiertos2[puntosCubiertos].remove(puntosCubiertosAux2[0])
                        puntosCubiertos2[indicemaxTipo2].remove(puntosCubiertosAux2[0])
                    
                    # print("Nuevos puntos cubiertos 2")
                    # print(puntosCubiertos2)
                    # print(" ")               

                
                else: # se llenan al azar los puntos que faltan de acuerdo a la cantidad 
                    
                    # print("Cobertura 1 inicial ", Cobertura1)
                    # print(" ")
                    # print("Cobertura 2 inicial ", Cobertura2)
                    # print(" ")
                    
                    randoms1 = []
                    for p in range(len(Cobertura1)):
                        if Cobertura1[p] > 0:
                            randoms1.append(p)
                    #print("posiciones random 1 ", randoms1)
                    
                    random_positions1 = random.sample(randoms1, eta[0] - len(initialSolution1))
                    for y in range(len(random_positions1)):
                        initialSolution1.append(random_positions1[y])

                    randoms2 = []
                    for p in range(len(Cobertura2)):
                        if Cobertura2[p] > 0:
                            randoms2.append(p)
                    #print("posiciones random 2 ", randoms2)
                    
                    random_positions2 = random.sample(randoms2, eta[1] - len(initialSolution2))
                    for y in range(len(random_positions2)):
                        initialSolution2.append(random_positions2[y])
                    
                    print( " Soluciones iniciales ")
                    print(initialSolution1, initialSolution2)
                    print(" ")
                    
                    break
            
            # Vamos a ver de esos puntos cuáles tienen más demanda 
            
            demandtype1 = []
            demandtype2 = []
            for i in range(len(I)):
                for k in range(len(K)):
                    demandcount = 0
                    if k == 1:
                        for s in range(len(S)):
                            demandcount += S[s][i][k]
                        demandtype1.append(demandcount)
                    else:
                        for s in range(len(S)):
                            demandcount += S[s][i][k]
                        demandtype2.append(demandcount)
                        
            # print("Demand count type 1") # me dice cuántos accidentes hubo
            # print(demandtype1)
            # print(" ")  
            
            # print("Demand count type 2") # me dice cuántos accidentes hubo
            # print(demandtype2)
            # print(" ") 
            
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
                        
            accidentesesperados1 = []
            for potentialsites1 in initialSolution1:
                accidentesConteo1 = 0
                for puntos1 in puntosCubiertos1[potentialsites1]:
                    accidentesConteo1 += demandtype1[puntos1]
                accidentesesperados1.append(accidentesConteo1/len(puntosCubiertos1[potentialsites1]))
                
            #print(accidentesesperados1)
            
            accidentesesperados2 = []
            for potentialsites2 in initialSolution2:
                accidentesConteo2 = 0
                for puntos2 in puntosCubiertos2[potentialsites2]:
                    accidentesConteo2 += demandtype2[puntos2]
                accidentesesperados2.append(accidentesConteo2/len(puntosCubiertos2[potentialsites2]))
                
            #print(accidentesesperados2)
            
            # ASIGNEMOS AMBULANCIAS 
            
            middle1 = min(accidentesesperados1) + (max(accidentesesperados1) - min(accidentesesperados1))/2
            oneambulance1 = []
            twoambulances1 = []
            countAmb1 = 0
            for i in range(len(accidentesesperados1)):
                if accidentesesperados1[i] >= middle1 and countAmb1+2 <= eta[0]:
                    twoambulances1.append(initialSolution1[i])
                    countAmb1 += 2
                else:
                    if countAmb1+1 <= eta[0]:
                        oneambulance1.append(initialSolution1[i])
                        countAmb1 += 1
            print(oneambulance1)
            print(twoambulances1)
        
            middle2 = min(accidentesesperados2) + (max(accidentesesperados2) - min(accidentesesperados2))/2
            oneambulance2 = []
            twoambulances2 = []
            countAmb2 = 0
            for i in range(len(accidentesesperados2)):
                if accidentesesperados2[i] >= middle2 and countAmb2+2 <= eta[1]:
                    twoambulances2.append(initialSolution2[i])
                    countAmb2 += 2
                else:
                    if countAmb2+1 <= eta[1]:
                        oneambulance2.append(initialSolution2[i])
                        countAmb2 += 1
            print(oneambulance2)          
            print(twoambulances2)
                 
            for lenL in range(len(L)):
                
                initialSolution.append([])
                
                if lenL in oneambulance1:
                    initialSolution[lenL].append(1)
                elif lenL in twoambulances1:
                    initialSolution[lenL].append(2)
                else:
                    initialSolution[lenL].append(0)
                    
                if lenL in oneambulance2:
                    initialSolution[lenL].append(1)
                elif  lenL in twoambulances2:
                    initialSolution[lenL].append(2)
                else:
                    initialSolution[lenL].append(0) 

            # Solamente se asignan 1 y 2... hay que modificar eso
            print("La solucion inicial final es ")
            print(initialSolution)
            print(" ")
            print( " ")
            #break 
            
            
        
            ######################################################################
            ######################    MODEL   ####################################
            ######################################################################
            
            model = gp.Model("TabuSearchWithSAA")            
            model.setParam('TimeLimit', 5*60)
            model._obj = None
            model._bd = None
            model._data = []
            model._start = time.time()
            
            sumaelapsed = 0
            
            # Create variables #
            y_vars = {}
            for s in range(len(S)):
                
                for l in L:
                    if initialSolution[l-1][0] > 0:
                        for i in I:
                            if S[s][i-1][0] != 0:
                                y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                              
                    if initialSolution[l-1][1] > 0:
                        for i in I:
                            for k in K:
                                if S[s][i-1][1] != 0:
                                    y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                     name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                if S[s][i-1][0] != 0:
                                    y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                                                     name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(k)+str(' ')+str(i))
                        
                
                # for l in L:
                #     if initialSolution[l-1][0] == 1:
                #         for i in I:
                #             for v in V:
                #                 if v == 2:
                #                     if S[s][i-1][1] != 0:
                #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                #                 else:
                #                     if S[s][i-1][0] != 0:
                #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                              
                #     if initialSolution[l-1][1] == 1:
                #         for i in I:
                #             for v in V:
                #                 if v == 2:
                #                     if S[s][i-1][1] != 0:
                #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                #                 else:
                #                     if S[s][i-1][0] != 0:
                #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                
            
            alpha_vars = {}  ## z full
            for s in range(len(S)):
                for i in I:
                    if S[s][i-1][0] != 0:
                        alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Full "+str(s+1)+str(' ')+str(i))
                    if S[s][i-1][1] != 0:
                        alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Full "+str(s+1)+str(' ')+str(i))
            
            beta_vars = {}  ## z partial 1
            for s in range(len(S)):
                for i in I:
                    if S[s][i-1][0] != 0:
                        beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial1 "+str(s+1)+str(' ')+str(i))
                    if S[s][i-1][1] != 0:
                        beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial1 "+str(s+1)+str(' ')+str(i))
            
            delta_vars = {}  ## z partial 2
            for s in range(len(S)):
                for i in I:
                    if S[s][i-1][0] != 0:
                        delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial2 "+str(s+1)+str(' ')+str(i))
                    if S[s][i-1][1] != 0:
                        delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial2 "+str(s+1)+str(' ')+str(i))
            
            phi_vars = {}   ## z partial 3
            for s in range(len(S)):
                for i in I:
                    if S[s][i-1][0] != 0:
                        phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial3 "+str(s+1)+str(' ')+str(i))
                    if S[s][i-1][1] != 0:
                        phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                  name="Partial3 "+str(s+1)+str(' ')+str(i))
            
            gamma_vars = {} ## z null
            for s in range(len(S)):
                for i in I:
                    if S[s][i-1][0] != 0:
                        gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                 name="Null "+str(s+1)+str(' ')+str(i))
                    if S[s][i-1][1] != 0:
                        gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                 name="Null "+str(s+1)+str(' ')+str(i))
        
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
                            
                # for l in L:
                #     for k in K:
                #         if initialSolution[l-1][k-1] != 0:
                #             suma = 0
                #             for i in I:
                #                 if S[s][i-1][0] != 0:
                #                     suma += y_vars[s+1,l,1,i]
                #                     model.addConstr(suma <= initialSolution[l-1][k-1], "c3")
                        
                #         if initialSolution[l-1][k-1] != 0:
                #             suma = 0
                #             for i in I:
                #                 if S[s][i-1][0] != 0:
                #                     suma += y_vars[s+1,l,3,i]
                #                 if S[s][i-1][1] != 0:
                #                     suma += y_vars[s+1,l,2,i] 
                #             model.addConstr(suma <= initialSolution[l-1][k-1], "c4")
            
                # for i in I:
                #     if S[s][i-1][0] != 0:
                #         suma = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 suma += y_vars[s+1,l,1,i] + y_vars[s+1,l,3,i]
                #         model.addConstr(suma <= S[s][i-1][0], "c5")
                    
                # for i in I:
                #     if S[s][i-1][1] != 0:
                #         suma = 0
                #         for l in L:
                #             if initialSolution[l-1][1] != 0:
                #                 suma += y_vars[s+1,l,2,i]
                #                 model.addConstr(suma <= S[s][i-1][1], "c6")

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
                        
                # for i in I:
                #     if S[s][i-1][0] + S[s][i-1][1] != 0:
                #         suma = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #         model.addConstr(suma - (S[s][i-1][0]+S[s][i-1][1]) <= alpha_vars[s+1,i] - 1, "c7")
                
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
                
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #         model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma, "c8")
             
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
                        
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma = 0
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(2*suma1 - suma - (S[s][i-1][0]+S[s][i-1][1]) <= (S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i], "c9" )

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
                        
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma1, "c_10")

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
                  
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(suma1 - 1 <= (S[s][i-1][0]+S[s][i-1][1])*delta_vars[s+1,i], "c_11")
                
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
                    
                
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(delta_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_12")

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
                    
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma = 0
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(suma1*delta_vars[s+1,i] <= suma, "c_13")

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
                    
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma = 0
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(suma1 - suma <= (S[s][i-1][0]+S[s][i-1][1])*phi_vars[s+1,i], "c_14")

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
                    
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(phi_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_15")

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
                    
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma = 0
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(np.amin(cli)*phi_vars[s+1,i] <= suma1 - suma, "c_16")

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
                    
                # for i in I:
                #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                #         suma1 = 0
                #         for l in L:
                #             if initialSolution[l-1][0] != 0:
                #                 for v in V:
                #                     if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                     else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #             if initialSolution[l-1][1] != 0:
                #                 for v in V:
                #                      if v == 2:
                #                         if S[s][i-1][1] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #                      else: 
                #                         if S[s][i-1][0] != 0:
                #                             suma1 += y_vars[s+1,l,v,i] 
                #         model.addConstr(suma1 + gamma_vars[s+1,i] >= 1, "c_17")
                   
                for i in I:
                    if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_18")
        
            # Optimize model
            
            model.optimize(callback=data_cb)
            
            end_time = time.time()
            
            elapsed_time = end_time - model._start
            
            sumaelapsed = sumaelapsed + elapsed_time
            
            #imprimir variables 

            colnames = ["name", "I size", "L size", "S size", "time", "best obj", "best bound", "gap %"]
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
        
            with open('data'+str(len(I))+str('_')
                              +str(len(L))+str('_')
                              +str(len(S))+'.csv', 'w') as fi:
                    writer = csv.writer(fi)
                    writer.writerows(model._data)
            
            #Nombre: Resultados_Prueba_I_L_M_N_S
            
            f = open ('Resultados_Prueba_'
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
            
            model.write('model_'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(S))+'.lp')
            model.write('model_'+str(len(I))+str('_')
                          +str(len(L))+str('_')
                          +str(len(S))+'.mps')
                    
            #break 
            
            valorObjetivo = model.objVal
        
            ####################################
            ####### LOCAL SEARCH ###############
            ####################################
            
            localsearch = 0
            entraSale1 = []
            entraSale2 = []

            while(1): # MODIFICAR PARA QUE SEAN DISTINTAS VECINDADES Y VER CON 
                        # CUAL FUNCIONA MEJOR Y HACER CORRIDAS GRANDES 
                                
                localsearch += 1
    
                #Vecindad
                posiblesVecinos1 = []
                for i in range(len(cantidadCobertura1)):
                    if cantidadCobertura1[i] != -1:
                        posiblesVecinos1.append(i)
    
                print("posibles vecinos")
                print(posiblesVecinos1)
                print(" ")
                
                cantidadVecinos1 = math.ceil(len(posiblesVecinos1)*(0.1))
                vecindad1 = random.sample(posiblesVecinos1, cantidadVecinos1)
                print(posiblesVecinos1)
                print(vecindad1)
                print(" ")
                
                vecino1 = random.sample(vecindad1, 1)
                indiceaux1 = []
                for i in range(len(initialSolution)):
                    if initialSolution[i][0] != 0:
                        indiceaux1.append(i)
                puntoQueSale1 = random.sample(indiceaux1, 1)
                
                print("initial solution")
                print(initialSolution)
                print(" ")
                
                print("Sale1: ", puntoQueSale1[0])
                print("vecino1: ", vecino1[0]-1)
                print(" ")
                
                initialSolution[puntoQueSale1[0]][0] = 0
                initialSolution[vecino1[0]-1][0] = 1
                
                posiblesVecinos2 = []
                for i in range(len(cantidadCobertura2)):
                    if cantidadCobertura2[i] != -1:
                        posiblesVecinos2.append(i)
                        
                print("posibles vecinos")
                print(posiblesVecinos2)
                print(" ")
                
     
                cantidadVecinos2 = math.ceil(len(posiblesVecinos2)*(0.1))
                vecindad2 = random.sample(posiblesVecinos2, cantidadVecinos2)
                print(posiblesVecinos2)
                print(vecindad2)
                print(" ")
                
                vecino2 = random.sample(vecindad2, 1)
                indiceaux2 = []
                for i in range(len(initialSolution)):
                    if initialSolution[i][0] != 0:
                        indiceaux2.append(i)
                puntoQueSale2 = random.sample(indiceaux2, 1)
                
                
                print("Sale2: ", puntoQueSale2[0])
                print("vecino2: ", vecino2[0]-1)
                print(" ")
                
                initialSolution[puntoQueSale2[0]][1] = 0
                initialSolution[vecino2[0]-1][1] = 1


                print("initial solution nueva")
                print(initialSolution)
                print(" ")
                

                ######################################################################
                ######################    MODEL   ####################################
                ######################################################################
                
                if (puntoQueSale1[0],vecino1[0]-1) not in entraSale1 and (puntoQueSale2[0],vecino2[0]-1) not in entraSale2:
                
                    entraSale1.append((puntoQueSale1[0],vecino1[0]-1))    
                    entraSale2.append((puntoQueSale2[0],vecino2[0]-1))
                
                    model = gp.Model("TabuSearchWithSAA")            
                    model.setParam('TimeLimit', 5*60)
                    model._obj = None
                    model._bd = None
                    model._data = []
                    model._start = time.time()
                    
                    # Create variables #
                    y_vars = {}
                    for s in range(len(S)):
                        
                        for l in L:
                            if initialSolution[l-1][0] > 0:
                                for i in I:
                                    if S[s][i-1][0] != 0:
                                        y_vars[s+1,l,1,i] = model.addVar(vtype=GRB.BINARY, 
                                                        name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(1)+str(' ')+str(i))
                                      
                            if initialSolution[l-1][1] > 0:
                                for i in I:
                                    for k in K:
                                        if S[s][i-1][1] != 0:
                                            y_vars[s+1,l,2,i] = model.addVar(vtype=GRB.BINARY, 
                                                             name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(2)+str(' ')+str(i))
                                        if S[s][i-1][0] != 0:
                                            y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                                                             name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(k)+str(' ')+str(i))
                                
                        
                        # for l in L:
                        #     if initialSolution[l-1][0] == 1:
                        #         for i in I:
                        #             for v in V:
                        #                 if v == 2:
                        #                     if S[s][i-1][1] != 0:
                        #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                        #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                        #                 else:
                        #                     if S[s][i-1][0] != 0:
                        #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                        #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                                      
                        #     if initialSolution[l-1][1] == 1:
                        #         for i in I:
                        #             for v in V:
                        #                 if v == 2:
                        #                     if S[s][i-1][1] != 0:
                        #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                        #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                        #                 else:
                        #                     if S[s][i-1][0] != 0:
                        #                         y_vars[s+1,l,v,i] = model.addVar(vtype=GRB.BINARY, 
                        #                                      name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(v)+str(' ')+str(i))
                        
                    
                    alpha_vars = {}  ## z full
                    for s in range(len(S)):
                        for i in I:
                            if S[s][i-1][0] != 0:
                                alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Full "+str(s+1)+str(' ')+str(i))
                            if S[s][i-1][1] != 0:
                                alpha_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Full "+str(s+1)+str(' ')+str(i))
                    
                    beta_vars = {}  ## z partial 1
                    for s in range(len(S)):
                        for i in I:
                            if S[s][i-1][0] != 0:
                                beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Partial1 "+str(s+1)+str(' ')+str(i))
                            if S[s][i-1][1] != 0:
                                beta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Partial1 "+str(s+1)+str(' ')+str(i))
                    
                    delta_vars = {}  ## z partial 2
                    for s in range(len(S)):
                        for i in I:
                            if S[s][i-1][0] != 0:
                                delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Partial2 "+str(s+1)+str(' ')+str(i))
                            if S[s][i-1][1] != 0:
                                delta_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Partial2 "+str(s+1)+str(' ')+str(i))
                    
                    phi_vars = {}   ## z partial 3
                    for s in range(len(S)):
                        for i in I:
                            if S[s][i-1][0] != 0:
                                phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Partial3 "+str(s+1)+str(' ')+str(i))
                            if S[s][i-1][1] != 0:
                                phi_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                          name="Partial3 "+str(s+1)+str(' ')+str(i))
                    
                    gamma_vars = {} ## z null
                    for s in range(len(S)):
                        for i in I:
                            if S[s][i-1][0] != 0:
                                gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                         name="Null "+str(s+1)+str(' ')+str(i))
                            if S[s][i-1][1] != 0:
                                gamma_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
                                                         name="Null "+str(s+1)+str(' ')+str(i))
                
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
                                    
                        # for l in L:
                        #     for k in K:
                        #         if initialSolution[l-1][k-1] != 0:
                        #             suma = 0
                        #             for i in I:
                        #                 if S[s][i-1][0] != 0:
                        #                     suma += y_vars[s+1,l,1,i]
                        #                     model.addConstr(suma <= initialSolution[l-1][k-1], "c3")
                                
                        #         if initialSolution[l-1][k-1] != 0:
                        #             suma = 0
                        #             for i in I:
                        #                 if S[s][i-1][0] != 0:
                        #                     suma += y_vars[s+1,l,3,i]
                        #                 if S[s][i-1][1] != 0:
                        #                     suma += y_vars[s+1,l,2,i] 
                        #             model.addConstr(suma <= initialSolution[l-1][k-1], "c4")
                    
                        # for i in I:
                        #     if S[s][i-1][0] != 0:
                        #         suma = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 suma += y_vars[s+1,l,1,i] + y_vars[s+1,l,3,i]
                        #         model.addConstr(suma <= S[s][i-1][0], "c5")
                            
                        # for i in I:
                        #     if S[s][i-1][1] != 0:
                        #         suma = 0
                        #         for l in L:
                        #             if initialSolution[l-1][1] != 0:
                        #                 suma += y_vars[s+1,l,2,i]
                        #                 model.addConstr(suma <= S[s][i-1][1], "c6")
        
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
                                
                        # for i in I:
                        #     if S[s][i-1][0] + S[s][i-1][1] != 0:
                        #         suma = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #         model.addConstr(suma - (S[s][i-1][0]+S[s][i-1][1]) <= alpha_vars[s+1,i] - 1, "c7")
                        
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
                        
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #         model.addConstr((S[s][i-1][0]+S[s][i-1][1])*alpha_vars[s+1,i] <= suma, "c8")
                     
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
                                
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma = 0
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(2*suma1 - suma - (S[s][i-1][0]+S[s][i-1][1]) <= (S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i], "c9" )
        
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
                                
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr((S[s][i-1][0]+S[s][i-1][1])*beta_vars[s+1,i] <= suma1, "c_10")
        
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
                          
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(suma1 - 1 <= (S[s][i-1][0]+S[s][i-1][1])*delta_vars[s+1,i], "c_11")
                        
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
                            
                        
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(delta_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_12")
        
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
                            
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma = 0
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(suma1*delta_vars[s+1,i] <= suma, "c_13")
        
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
                            
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma = 0
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(suma1 - suma <= (S[s][i-1][0]+S[s][i-1][1])*phi_vars[s+1,i], "c_14")
        
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
                            
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(phi_vars[s+1,i] <= (S[s][i-1][0]+S[s][i-1][1]) - suma1, "c_15")
        
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
                            
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma = 0
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma += cli[l-1][i-1]*y_vars[s+1,l,v,i] 
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(np.amin(cli)*phi_vars[s+1,i] <= suma1 - suma, "c_16")
        
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
                            
                        # for i in I:
                        #     if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                        #         suma1 = 0
                        #         for l in L:
                        #             if initialSolution[l-1][0] != 0:
                        #                 for v in V:
                        #                     if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                     else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #             if initialSolution[l-1][1] != 0:
                        #                 for v in V:
                        #                      if v == 2:
                        #                         if S[s][i-1][1] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #                      else: 
                        #                         if S[s][i-1][0] != 0:
                        #                             suma1 += y_vars[s+1,l,v,i] 
                        #         model.addConstr(suma1 + gamma_vars[s+1,i] >= 1, "c_17")
                           
                        for i in I:
                            if (S[s][i-1][0] + S[s][i-1][1]) != 0:
                                model.addConstr(alpha_vars[s+1,i] + beta_vars[s+1,i] + delta_vars[s+1,i] + phi_vars[s+1,i] + gamma_vars[s+1,i] == 1, "c_18")
                    
                    # Optimize model
                    
                    model.optimize(callback=data_cb)
                    
                    end_time = time.time()
                    
                    elapsed_time = end_time - model._start
                    
                    sumaelapsed = sumaelapsed + elapsed_time
                    
                    
                    #imprimir variables 
             
                    colnames = ["name", "I size", "L size", "S size", "time", "best obj", "best bound", "gap %"]
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
                
                    #writer.writerows(name)
                    with open('data'+str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.csv', 'a') as f: #Cambiar de w a a
                        writer = csv.writer(f)
                        writer.writerows("new")
                        writer.writerows(model._data)
                    
                    #Nombre: Resultados_Prueba_I_L_M_N_S
                    
                    f = open ('Resultados_Prueba_'
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
                    
                    model.write('model_'+str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.lp')
                    model.write('model_'+str(len(I))+str('_')
                                  +str(len(L))+str('_')
                                  +str(len(S))+'.mps')
                    
                if model.objVal > valorObjetivo:
                    print("   ")
                    print("   ")
                    print("entra ultimo if", localsearch)
                    print("   ")
                    print("   ")
                    break
                
                else:
                    if sumaelapsed > 300:
                        print("   ")
                        print("   ")
                        print("entra ultimo else", localsearch)
                        print("   ")
                        print("   ")
                        break

            
print("Elapsed time total ")
print(sumaelapsed)
print(" ")

sheet.write(countcsv+1, 0, "Total Elapsed Time")
sheet.write(countcsv+1, 1, sumaelapsed)
            
            ########### HACER EL CICLO PARA MEJORAR LA SOLUCION INICIAL
            
            # listaTabu = []      
            # for meth in range(10):
                
            #     ######################################################################
            #     ###################    TABU SEARCH   #################################
            #     ######################################################################
                
            #     #Vecindad
            #     posiblesVecinos1 = []
            #     for i in range(len(cantidadCobertura1)):
            #         if cantidadCobertura1[i] != -1:
            #             posiblesVecinos1.append(i)
                        
            #     print("posibles vecinos")
            #     print(posiblesVecinos1)
            #     print(" ")
                
            #     cantidadVecinos1 = math.ceil(len(posiblesVecinos1)*(0.1))
            #     vecindad1 = random.sample(posiblesVecinos1, cantidadVecinos1)
            #     print(posiblesVecinos1)
            #     print(vecindad1)
            #     print(" ")
                
            #     vecino1 = random.sample(vecindad1, 1)
            #     indiceaux1 = []
            #     for i in range(len(initialSolution)):
            #         if initialSolution[i][0] != 0:
            #             indiceaux1.append(i)
            #     puntoQueSale1 = random.sample(indiceaux1, 1)
                
            #     print("initial solution")
            #     print(initialSolution)
            #     print(" ")
                
            #     print("Sale1: ", puntoQueSale1[0])
            #     print("vecino1: ", vecino1[0]-1)
            #     print(" ")
                
            #     initialSolution[puntoQueSale1[0]][0] = 0
            #     initialSolution[vecino1[0]-1][0] = 1
                
            #     posiblesVecinos2 = []
            #     for i in range(len(cantidadCobertura2)):
            #         if cantidadCobertura2[i] != -1:
            #             posiblesVecinos2.append(i)
                        
            #     print("posibles vecinos")
            #     print(posiblesVecinos2)
            #     print(" ")
                
 
            #     cantidadVecinos2 = math.ceil(len(posiblesVecinos2)*(0.1))
            #     vecindad2 = random.sample(posiblesVecinos2, cantidadVecinos2)
            #     print(posiblesVecinos2)
            #     print(vecindad2)
            #     print(" ")
                
            #     vecino2 = random.sample(vecindad2, 1)
            #     indiceaux2 = []
            #     for i in range(len(initialSolution)):
            #         if initialSolution[i][0] != 0:
            #             indiceaux2.append(i)
            #     puntoQueSale2 = random.sample(indiceaux2, 1)
                
                
            #     print("Sale2: ", puntoQueSale2[0])
            #     print("vecino2: ", vecino2[0]-1)
            #     print(" ")
                
            #     initialSolution[puntoQueSale2[0]][1] = 0
            #     initialSolution[vecino2[0]-1][1] = 1
                
            #     print("initial solution nueva")
            #     print(initialSolution)
            #     print(" ")
            
            #     #Lista Tabu 
                
            #     listaTabu.append(puntoQueSale1[0])
            #     listaTabu.append(puntoQueSale2[0])
                
            #     print("Lista Tabu")
            #     print(listaTabu)
            #     print(" ")
                
            #     model(countcsv)

fi.close()
book.save('TesisTS.xls') 
            