# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:22:26 2022

@author: beatr
"""
import random 
import numpy as np

### Lectura de instancias ###

tamaños_I = [20, 50, 80]
tamaños_L = [40, 50, 70]
tamaños_S = [12, 25, 30]
K = [1, 2]

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
    
            #Nombre: Instancias_Prueba_I_L_S
                
            archivo = open('Instancias_Prueba_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')
                      +str(tamaños_S[sconj])+str('_')
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
            p = np.amax(cli)/len(S) + 0.005
            eta = [20, 11]
            t = 10
            tmax = 25
            wi = [1, 0.85, 0.6, 0.3]
            
            V = [1,2,3]

            ### Solución inicial ###
            initialSolution = []
            random_positions1 = random.sample(range(len(I)), eta[0])
            random_positions2 = random.sample(range(len(I)), eta[1])
            print(random_positions1)
            print(random_positions2)
            
            for l in range(len(L)):
                
                if l in random_positions1:
                    initialSolution.append(1)
                else:
                    initialSolution.append(0)
                    
                if l in random_positions2:
                    initialSolution.append(1)
                else:
                    initialSolution.append(0)
            
            print("la solucion inicial es ") 
            print(initialSolution)
            print(" ")
            
            ### Evaluación de la solución inicial ###
            objFunction = 0
            