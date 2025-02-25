# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 11:50:21 2023

@author: beatr
"""

# # tamaños_I = [168, 270, 500, 900, 1500] #Hasta aquí puede bien el modelo
# tamaños_L = [16, 30, 50, 70, 100]
# tamaños_S = [10, 50, 100, 150, 200]

tamaños_I = [168, 270, 500, 900, 1500] 
tamaños_L = [16, 50, 100]
tamaños_S = [10, 50, 100, 150, 200]

# tamaños_I = [168] 
# tamaños_L = [16]
# tamaños_S = [10]

rates = [0.4]
verif = 0.4

#ambulance = [[10, 6], [20,11], [35,20]]
ambulance = [[35,20]]

for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            for k in range(len(ambulance)):
            #for rep in range(repeticiones):
                
                eta = ambulance[k]

                # archivo = open('Resultados_Prueba_ObjZs_Scenarios__Modif_121024_'
                #           +str(tamaños_I[iconj])+str('_')
                #           +str(tamaños_L[jconj])+str('_')
                #           +str(tamaños_S[sconj])
                #           +'_'+str(eta[0])+'_'+str(eta[1])
                #           +'.txt', "r")

                archivo = open('Best_Matheuristic_081024_'
                          +str(tamaños_I[iconj])+str('_')
                          +str(tamaños_L[jconj])+str('_')
                          +str(tamaños_S[sconj])
                          +'_'+str(eta[0])+'_'+str(eta[1])
                          +'.txt', "r")
                
                line = archivo.readline().strip().split()
                line = archivo.readline().strip().split()
                
                f = open ('Location_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                for i in range(tamaños_L[jconj]*2):
                    line = archivo.readline()
                    f.write(line)
                    
                f.close()
                
                
                line = archivo.readline()
                g = open ('Dispatch_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while len(line) > 15:
                    g.write(line)
                    line = archivo.readline()
                        
                g.close()
                
                line = archivo.readline()
                
                #print(line)
                h = open ('Full_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Full" in line:
                    h.write(line)
                    line = archivo.readline()
                        
                h.close()
                
                line = archivo.readline()
                
                o = open ('Partial1_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Partial1" in line:
                    o.write(line)
                    line = archivo.readline()
                        
                o.close()
                
                line = archivo.readline()
                
                p = open ('Partial2_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Partial2" in line:
                    p.write(line)
                    line = archivo.readline()
                        
                p.close()
                
                line = archivo.readline()
                
                q = open ('Partial3_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Partial3" in line:
                    q.write(line)
                    line = archivo.readline()
                        
                q.close()
                    
                line = archivo.readline()
                
                r = open ('Null_Matheuristic_081024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                while "Null" in line:
                    r.write(line)
                    line = archivo.readline()
                        
                r.close()
                
                # verif=0.4
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
                
                
                un = open ('ScAccidents_ObjZs_Scenarios__Modif_121024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'.txt','w')
                
                u = open ('Accidents_ObjZs_Scenarios__Modif_121024_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'.txt','w')
                        
                
                accidentes = []
                for cant in range(tamaños_S[sconj]):
                    line_1 = h.readline().strip().split()
                    un.write(str(line_1))
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
                    
                un.close()
                
                    
                    
                # # u = open ('Accidents_ObjZs_Scenarios_'
                # #               +str(tamaños_I[iconj])+str('_')
                # #               +str(tamaños_L[jconj])+str('_')
                # #               +str(tamaños_S[sconj])+'.txt','w')
                        
                
                # # accidentes = []
                # # for cant in range(tamaños_S[sconj]):
                # #     line_1 = h.readline().strip().split()
                # #     accident = 0
                # #     total_accidents = 0
                # #     for a in range(tamaños_I[iconj]):
                # #         if int(line_1[accident])!=0 or int(line_1[accident+1])!=0:
                # #             total_accidents += 1 
                # #         accident += 2
                # #     accidentes.append(total_accidents)
                # #     u.write(str(total_accidents))
                # #     u.write(' ')
                
                # # u.close()
                
                # tim = open ('rli_ObjZs_Scenarios__Modif_121024_'
                #               +str(tamaños_I[iconj])+str('_')
                #               +str(tamaños_L[jconj])+str('_')
                #               +str(tamaños_S[sconj])+'.txt','w')
                
                # for cant in range(tamaños_L[jconj]):
                #     line_1 = h.readline()
                #     tim.write(line_1)
                    
                # v = open ('Cli_ObjZs_Scenarios__Modif_121024_'
                #               +str(tamaños_I[iconj])+str('_')
                #               +str(tamaños_L[jconj])+str('_')
                #               +str(tamaños_S[sconj])+'.txt','w')
                    
                # for cant in range(tamaños_L[jconj]):
                #     line_1 = h.readline()
                #     v.write(line_1)
                    
                # v.close()
                    
                
                        
                