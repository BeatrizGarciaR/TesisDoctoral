# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 19:14:27 2021

@author: beatr
"""
import random

# tamaños_I = [100, 500, 1000]
# tamaños_L = [30, 45, 70]
# tamaños_S = [50, 100, 500]

# tamaños_I = [20, 50, 100]
# tamaños_L = [8, 20, 40]
# tamaños_S = [5, 20, 50]
#repeticiones = 5

# tamaños_I = [5, 10, 20]
# tamaños_L = [10, 25, 40]
# tamaños_S = [3, 7, 12]

# tamaños_I = [50, 200, 350]
# tamaños_L = [20, 40, 55]
# tamaños_S = [15, 50, 75]

tamaños_I = [1000]
tamaños_L = [500]
tamaños_S = [50]


# tamaños_I = [100, 300, 500, 1000, 5000, 10000]
# tamaños_L = [70, 100, 200, 500, 1000]
# tamaños_S = [50, 100, 500, 1000, 3000, 10000]

# tamaños_I = [5000, 10000]
# tamaños_L = [70, 100, 200, 500, 1000]
# tamaños_S = [50, 100, 500, 1000, 3000, 10000]


porcentaje_L1 = 0.55
porcentaje_L2 = 0.85

t = 10
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
        
        pickL2 = int(tamaños_L[jconj]*porcentaje_L2)
        L2 = random.sample(L, pickL2)
        
        ################################
        ######## RESPONSE TIME #########
        ################################
        
        # CRUM response times 
        r_li1 = []
        for l in range(len(L)):
            r_li1.append([])
            for i in range(len(I)):
                if (l+1) in L1:
                    b = random.randint(9, 45)
                    r_li1[l].append(b)
                else:
                    r_li1[l].append(1000)
        
    
        #Red Cross response times
        r_li2 = []
        for l in range(len(L)):
            r_li2.append([])
            for i in range(len(I)):
                if (l+1) in L2:
                    b = random.randint(15, 35)
                    r_li2[l].append(b)
                else:
                    r_li2[l].append(1000)
        

                    
        for sconj in range(len(tamaños_S)):
            
            #for rep in range(repeticiones):
    
            #Nombre: Instancias_Prueba_I_L_M_N_S_Rep
            
            f = open ('Instancias_Prueba_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')
                      +'2'+str('_')
                      +'3'+str('_')
                      +str(tamaños_S[sconj])+str('_')
                      #+str(rep+1)
                      +'_.txt','w')
            
            ################################
            ############# SETS #############
            ################################
            
            f.write(str(len_I))
            f.write("\n")
            
            
            f.write(str(len_L))
            f.write("\n")
        
            len_M = 2
            f.write(str(len_M))
            f.write("\n")
            
            len_N = 3
            f.write(str(len_N))
            f.write("\n")
            
            len_S = tamaños_S[sconj]
            f.write(str(len_S))
            f.write("\n")


           # f.write(str(rep+1))
            #f.write("\n")
            
            #Set of demand points
            
            
            for i in range(len(I)):
                f.write(str(I[i])+str(" "))
            f.write("\n")
            
            #Set of potential sites L 
            
                
            for l in range(len(L)):
                f.write(str(L[l])+str(" "))
            f.write("\n")
            
            #Set of potential sites L1
              
            # f.write(str(pickL1))
            # f.write("\n")
            
            # for l in range(len(L1)):
            #     f.write(str(L1[l])+str(" "))
            # f.write("\n")
            
            # #Set of potential sites L2
            
            # f.write(str(pickL2))
            # f.write("\n")
                
            # for l in range(len(L2)):
            #     f.write(str(L2[l])+str(" "))
            # f.write("\n")
        
            # #Set of ambulance types
            # M = []
            # for m in range(len_M):
            #     M.append(m)
            
            # for m in range(len(M)):
            #     f.write(str(M[m]+1)+str(" "))
            # f.write("\n")
            
            # #Set of accident types
            # N = []
            # for n in range(len_N):
            #     N.append(n)
            
            # for n in range(len(N)):
            #     f.write(str(N[n]+1)+str(" "))
            # f.write("\n")
                
            
            ################################
            ########## SCENARIOS ###########
            ################################
            
            S = []
            probabilidades_S = [0.95, 0.2, 0.08, 0.02]
            opciones_S = []
            N_aux = [0, 1, 2, 3]
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

            #Writing .txt
            for l in range(len(L)):
                for i in range(len(I)):
                    f.write(str(r_li2[l][i])+str(" "))
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
                    
                    
        
            # ################################
            # ######## AVAILABLE AMB #########
            # ################################
            # bs_l2 = []
            # probabilidades_bs = [0.3, 0.7]
            # opciones_bs = []
            # for e, p in zip(N, probabilidades_bs):
            #     opciones_bs += [e]*int(p*10000)
            
            # for i in range(len_S):
            #     bs_l2.append([])
            #     for j in range(len(L)):
            #         b = int(random.choice(opciones_bs))
            #         bs_l2[i].append(b)
        
            # #Writing .txt
            # for s in range(len_S):
            #     for l in range(len(L)):
            #         f.write(str(bs_l2[s][l])+str(" "))
            #     f.write("\n")
                
                
            f.close()
            
            