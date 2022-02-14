# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 19:14:27 2021

@author: beatr
"""
import random

tamaños_I = [10, 50, 100]
tamaños_L = [5, 20, 40]
tamaños_S = [10, 50, 100]


for i in range(3):
    
    f = open ('Instancias_'
              +str(tamaños_I[i])+str('_')
              +str(tamaños_L[i])+str('_')
              +'3'+str('_')
              +str(tamaños_S[i])
              +'.txt','w')
    
    ################################
    ############# SETS #############
    ################################
    
    len_I = tamaños_I[i]
    f.write(str(len_I))
    f.write("\n")
    
    len_L = tamaños_L[i]
    f.write(str(len_L))
    f.write("\n")
    
    len_N = 3
    f.write(str(len_N))
    f.write("\n")
    
    len_S = tamaños_S[i]
    f.write(str(len_S))
    f.write("\n")
    
    #Set of demand points
    I = []
    for i in range(len_I):
        I.append(i+1)
    
    for i in range(len(I)):
        f.write(str(I[i])+str(" "))
    f.write("\n")
    
    #Set of potential sites    
    L = []
    for l in range(len_L):
        L.append(l+1)
        
    for l in range(len(L)):
        f.write(str(L[l])+str(" "))
    f.write("\n")
    
    #Set of accident types
    N = []
    for n in range(len_N + 1):
        N.append(n)
    
    for n in range(len(N)):
        f.write(str(N[n])+str(" "))
    f.write("\n")
        
    
    ################################
    ########## SCENARIOS ###########
    ################################
    
    S = []
    probabilidades_S = [0.6, 0.1, 0.1, 0.6]
    opciones_S = []
    for e, p in zip(N, probabilidades_S):
        opciones_S += [e]*int(p*10000)
    
    for i in range(len_S):
        S.append([])
        for j in range(len(I)):
            a = int(random.choice(opciones_S))
            S[i].append(a)
    
    
    #Writing .txt
    for s in range(len_S):
        for i in range(len(I)):
            f.write(str(S[s][i])+str(" "))
        f.write("\n")
    
    
    ################################
    ######## RESPONSE TIME #########
    ################################
    
    r_li = []
    for l in range(len(L)):
        r_li.append([])
        for i in range(len(I)):
            b = random.randint(9, 32)
            r_li[l].append(b)
            
    
    #Writing .txt
    for l in range(len(L)):
        for i in range(len(I)):
            f.write(str(r_li[l][i])+str(" "))
        f.write("\n")
        
        
    f.close()