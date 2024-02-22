# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 11:57:32 2023

@author: beatr
"""

# tamaños_I = [168, 270, 500, 900, 1500, 2100, 3000] 
# tamaños_L = [30, 50, 70, 100, 250]
# tamaños_S = [10, 50, 100, 150, 200, 500]


# tamaños_I = [168, 270] 
# tamaños_L = [16]
# tamaños_S = [10, 50]


tamaños_I = [168, 270, 500, 900, 1500] 
tamaños_L = [30]
tamaños_S = [10, 50, 100, 150, 200]

amb = [[10, 6], [20, 11], [35,20]] 
#amb = [[10,6]]
rates = [0.4]


for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            for a in range(len(amb)):
                
                verif = rates[0]
                
                eta = amb[a]
                
                
                archivo = open('Resultados_Prueba_NewModel_Supuesto_070224_'
                          +str(tamaños_I[iconj])+str('_')
                          +str(tamaños_L[jconj])+str('_')
                          +str(tamaños_S[sconj])
                          +'_'+str(eta[0])+'_'+str(eta[1])
                          +'.txt', "r")
                
                line = archivo.readline().strip().split()
                line = archivo.readline().strip().split()
                
                f = open ('Location_Obj_NewModel_Supuesto_070224_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                for i in range(tamaños_L[jconj]*2):
                    line = archivo.readline()
                    f.write(line)
                    
                f.close()
                
                
                line = archivo.readline()
                g = open ('OnTime_Obj_NewModel_Supuesto_070224_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                
                count_ontime = 0
                while "OnTime" in line:
                    if line[len(line)-2] == '1':
                        i = 7
                        line_aux = str()
                        while line[i] != " ":
                            line_aux += line[i]
                            i = i+1
                        g.write(line_aux + " " + line)
                        count_ontime = count_ontime + 1
                    line = archivo.readline()
                    
                if count_ontime == 0:
                    g.write(str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0))
                    g.write('\n')
                            
                g.close()
                
               
                h = open ('Delayed_Obj_NewModel_Supuesto_070224_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                count_delayed = 0
                while "Delayed" in line:
                    if line[len(line)-2] == '1':
                        i = 8
                        line_aux = str()
                        while line[i] != " ":
                            line_aux += line[i]
                            i = i+1
                        h.write(line_aux + " " + line)
                        count_delayed = count_delayed + 1
                    line = archivo.readline()
                        
                if count_delayed == 0:
                    h.write(str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0))
                    h.write('\n')
                    
                h.close()
                
                
                r = open ('NotAssigned_Obj_NewModel_Supuesto_070224_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'_'+str(eta[0])+'_'+str(eta[1])+'.txt','w')
                
                count_notassigned = 0
                while "NotAssigned" in line:
                    if line[len(line)-2] != '0':
                        i = 12
                        line_aux = str()
                        while line[i] != " ":
                            line_aux += line[i]
                            i = i+1
                        r.write(line_aux + " " + line)
                        count_notassigned = count_notassigned + 1
                    if line[len(line)-2] == '0' and line[len(line)-3] != ' ':
                        i = 12
                        line_aux = str()
                        while line[i] != " ":
                            line_aux += line[i]
                            i = i+1
                        r.write(line_aux + " " + line)
                        count_notassigned = count_notassigned + 1
                    line = archivo.readline()
                    
                if count_notassigned == 0:
                    r.write(str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0))
                    r.write('\n')
                        
                r.close()
                
                
                # Accidents
                
                
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
                    
                    
                u = open ('Accidents_NewModel_Supuesto_070224_'
                              +str(tamaños_I[iconj])+str('_')
                              +str(tamaños_L[jconj])+str('_')
                              +str(tamaños_S[sconj])+'.txt','w')
                
                v = open ('I_Accidents_NewModel_Supuesto_070224_'
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
                            v.write(str(int(line_1[accident])+int(line_1[accident+1])))
                            v.write(' ')
                        else:
                            v.write(str(0))
                            v.write(' ')
                        accident += 2
                    v.write('\n')
                    accidentes.append(total_accidents)
                    u.write(str(total_accidents))
                    u.write(' ')
                
                v.close()
                
                u.write('\n')
                u.close()
                
   