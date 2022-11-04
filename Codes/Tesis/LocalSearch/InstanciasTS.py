# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 12:30:17 2022

@author: beatr
"""

import random
import numpy as np
 

tamaños_I = [20, 50, 80]
tamaños_L = [40, 50, 70]
tamaños_S = [12, 25, 30]
porcentaje_L1 = 0.65
t = 9
tmax = 25
K = [1,2]

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        
        len_I = tamaños_I[iconj]
        len_L = tamaños_L[jconj]
        
        I = []
        for i in range(len_I):
            I.append(i+1)
        
        L = []
        for l in range(len_L):
            L.append(l+1)
        
        pickL1 = int(tamaños_L[jconj]*porcentaje_L1)
        L1 = random.sample(L, pickL1)
        
        ################################
        ######## RESPONSE TIME #########
        ################################
        
        r_li1 = []
        for l in range(len(L)):
            r_li1.append([])
            for i in range(len(I)):
                if (l+1) in L1:
                    mu, sigma = 15.2, 4.3 # media y desvio estandar
                    b = np.random.normal(mu, sigma, 1)
                    #b = random.randint(9, 45) ## Cambiar 
                    if round(b[0]) < 0:
                        r_li1[l].append(0)
                    else:
                        r_li1[l].append(round(b[0]))
                else:
                    r_li1[l].append(1000)
                    
        for sconj in range(len(tamaños_S)):
    
            #Nombre: Instancias_Prueba_I_L_S
            
            f = open ('Instancias_Prueba_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')
                      +str(tamaños_S[sconj])+str('_')
                      +'.txt','w')
            
            ################################
            ############# SETS #############
            ################################
            
            f.write(str(len_I))
            f.write("\n")
            
            
            f.write(str(len_L))
            f.write("\n")
        
        
            len_S = tamaños_S[sconj]
            f.write(str(len_S))
            f.write("\n")
            
            
            #Set of demand points
        
            # for i in range(len(I)):
            #     f.write(str(I[i])+str(" "))
            # f.write("\n")
            
            # #Set of potential sites L 
            
                
            # for l in range(len(L)):
            #     f.write(str(L[l])+str(" "))
            # f.write("\n")

            
            ################################
            ########## SCENARIOS ###########
            ################################
            
            S = []
            probabilidades_S = [0.75, 0.25]
            opciones_S = []
            N_aux = [0, 1]
            for e, p in zip(N_aux, probabilidades_S):
                opciones_S += [e]*int(p*1000000)
            for i in range(len_S):
                S.append([])
                for j in range(len(I)):
                    S[i].append([])
                    for k in range(len(K)):
                        a = int(random.choice(opciones_S))
                        S[i][j].append(a)
            
            #print(S)
            
            #Writing .txt
            for s in range(len_S):
                for i in range(len(I)):
                    for k in range(len(K)):
                        f.write(str(S[s][i][k])+str(" "))
                f.write("\n")
        
            # RESPONSE TIMES 
            
            #Writing .txt
            for l in range(len(L)):
                for i in range(len(I)):
                    f.write(str(r_li1[l][i])+str(" "))
                f.write("\n")
                
            ################################
            ########## Cil ###########
            ################################          
            cli = []
            for l in range(len(L)):
                cli.append([])
                for i in range(len(I)):
                    if r_li1[l][i] != 1000:
                        #print(r_li1[l][i])
                        if r_li1[l][i] < t:
                            cli[l].append(1)
                            #print("entra a 1")
                        elif r_li1[l][i] > tmax:
                            cli[l].append(0)
                            #print("entra a 0")
                        else:
                            d_rli = 1 - ((r_li1[l][i]-t)/(tmax-t))
                            cli[l].append(d_rli)
                            #print("entra a d_rli", d_rli)
                    else:
                        cli[l].append(0)
                        
                    
            #Writing .txt
            for l in range(len(L)):
                for i in range(len(I)):
                    f.write(str(cli[l][i])+str(" "))
                f.write("\n")
                
                
            f.close()
            
import numpy as np
import scipy.special
import matplotlib.pyplot as plt
import math
from scipy import stats

# Graficando Poisson
mu =  14.2 # parametro de forma 
poisson = stats.poisson(mu) # Distribución
x = np.arange(poisson.ppf(0.01),
              poisson.ppf(0.99))
fmp = poisson.pmf(x)*500
print("poisson")
print(x)
print(fmp)
print (" ")

#x = np.linspace(1, 7, 25)
# mu, sigma = 15.2, 4.3 # media y desvio estandar
# x = np.random.normal(mu, sigma, 25)
# print("x")
# print(x)
# print(" ")
# y = scipy.special.gamma(x)
# print("y")
# print(y)
# print (" ")

# for i in range(25):
#     print(int(1/y[i]))

# for i in range(25):
#     print("math gamma")
#     print(int(math.gamma(x[i])))

# plt.figure(num=1)
# plt.plot(x,y,'b-')
# plt.xlim((-5,5))
# plt.ylim((-6,6))
# plt.grid('on')
# plt.show()



# from sympy.stats import Gamma, density 
# from sympy import Symbol, pprint 

# z = Symbol("z") 
  
# X = Gamma("x", 1 / 3, 45) 
# pprint(X)

# gamVar = density((X)(z)) 
# pprint(gamVar)
  
# k = Symbol("k", positive = True) 
# theta = Symbol("theta", positive = True) 
# z = Symbol("z") 
  
# X = Gamma("x", k, theta) 
# pprint(X)
# gamVar = density((X)(z)) 
  
# pprint(gamVar)
