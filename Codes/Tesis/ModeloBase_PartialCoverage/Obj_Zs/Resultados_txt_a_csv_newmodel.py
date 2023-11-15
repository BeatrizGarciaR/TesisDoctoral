# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:57:32 2023

@author: beatr
"""

tamaños_I = [168, 270, 500, 900, 1500] 
tamaños_L = [16, 70]
tamaños_S = [10, 50, 100]

eta = [10, 6]
rates = [0.4]

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            for verif in rates:
                
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
                    
                    
                u = open ('Accidents_NewModel_111123_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'.txt','w')
                        
                
                accidentes = []
                for cant in range(tamaños_S[sconj]):
                    line_1 = h.readline().strip().split()
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