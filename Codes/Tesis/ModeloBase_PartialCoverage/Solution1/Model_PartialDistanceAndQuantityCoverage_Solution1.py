# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 20:58:44 2022

@author: beatr
"""
######################################################################
######################  INSTANCES ####################################
######################################################################

import gurobipy as gp
from gurobipy import GRB

#Sets

I = [1, 2 ,3]
L = [1, 2, 3, 4, 5]
#Li = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
K = [1, 2]
N = [[1, 2, 3], [1, 2, 3]]   

S = [[[2, 0], [0, 0], [0, 1]],  #accidentes originales
      [[1, 1], [2, 0], [0, 0]],
      [[0, 1], [1, 0], [2, 1]]]
 
# S = [[[2, 0], [0, 0], [2, 0]],  #Puros accidentes tipo 1
#      [[1, 0], [3, 0], [0, 0]],
#      [[1, 0], [1, 0], [2, 0]]]

# S = [[[0, 2], [0, 0], [0, 2]], #Puros accidentes tipo 2
      # [[0, 2], [0, 3], [0, 0]],
      # [[0, 1], [0, 1], [0, 2]]]


# a = []
# for s in range(len(S)):
#     a.append([])
#     for i in I:
#         a[s].append([])
#         for num in range(2):
#             if S[s][i-1][num] == 0:
#                 a[s][i-1].append(0)
#             else:
#                 a[s][i-1].append(S[s][i-1][num])

# a_aux = []
# for s in range(len(S)):
#     a_aux.append([])
#     for i in I:
#         a_aux[s].append([])
#         for n in (2,3):
#             if S[s][i-1][0] == 0 or S[s][i-1][n] == 0: #Todos los aik
#             #if S[s][i-1][0] == 0: #solo cuando i = 0
#                 a_aux[s][i-1].append(1000)
#             else:
#                 a_aux[s][i-1].append(S[s][i-1][n])

#Parameters

p = 0.3
eta = [2,1]
#n1 = 2
#n2 = 1
t = 10
tmax = 25
ril = [[18, 25, 20, 26, 26],
       [26, 10, 19, 18, 26],
       [26, 26, 13, 22, 16]]

cil = [[0.47, 0.06, 0.3, 0, 0],
       [0, 1, 0.36, 0.42, 0],
       [0, 0, 0.82, 0.18, 0.54]]
                
######################################################################
######################    MODEL   ####################################
######################################################################

model = gp.Model("PartialRateCoverage")

# Create variables #
x_vars = {}
for l in L:
    for k in K:
        x_vars[l,k] = model.addVar(vtype=GRB.INTEGER, 
                         name="located "+str(l)+str(' ')+str(k))

y_vars = {}
for s in range(len(S)):
    for l in L:
        for i in I:
            for k in K:
                y_vars[s+1,l,k,i] = model.addVar(vtype=GRB.BINARY, 
                                     name="dispatched "+str(s+1)+str(' ')+str(l)+str(' ')+str(k)+str(' ')+str(i))
           
# znull_vars = {}
# for s in range(len(S)):
#     for i in I:
#         znull_vars[s+1,i] = model.addVar(vtype=GRB.BINARY, 
#                                      name="null "+str(s+1)+str(' ')+str(i))

# Set objective

# model.setObjective(gp.quicksum(gp.quicksum(cil[i-1][l-1]*y_vars[s+1,i,l,k] 
#                                            for l in L)/(a[s][i-1][k-1])   
#                                for s in range(len(S)) for i in I for k in K)/len(S), GRB.MAXIMIZE)

obj = gp.LinExpr()
for s in range(len(S)):
    for i in I:
        if S[s][i-1][0]!=0:
            obj += gp.quicksum(cil[i-1][l-1]*y_vars[s+1,l,k,i] for l in L for k in K)/(len(S)*(S[s][i-1][0]))
        
        if S[s][i-1][1]!=0:
            obj += gp.quicksum(cil[i-1][l-1]*y_vars[s+1,l,2,i] for l in L)/(len(S)*(S[s][i-1][1]))

model.setObjective(obj, GRB.MAXIMIZE)  


# Add constraints

for s in range(len(S)):
    
    for k in K:
        model.addConstr(gp.quicksum(x_vars[l,k] for l in L) <= eta[k-1], "c2")
    
    for l in L:
        for k in K:
            model.addConstr(gp.quicksum(y_vars[s+1,l,k,i] for i in I) <= x_vars[l,k], "c3")
            
    # for i in I:
    #     for k in K:
    #         model.addConstr(gp.quicksum(y_vars[s+1,i,l,k] for l in L) <= a[s][i-1][k-1], "c4")
    
    # for i in I:
    #     if S[s][i-1][0] != 0:
    #         model.addConstr(gp.quicksum(y_vars[s+1,i,l,k] for k in K for l in L) + znull_vars[s+1,i] >= 1, "c5")

            
# Optimize model
model.optimize()

#imprimir variables 

#Nombre: Resultados_Prueba_I_L_M_N_S

f = open ('Resultados_Prueba_'
              +str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')
              +str('Solution1_aik=0_todos')+'_.txt','w')

f.write('Obj: %g' % model.objVal)
f.write('\n')

for v in model.getVars():
    f.write('%s %g' % (v.varName, v.x))
    f.write('\n')
    
#imprimir el valor objetivo
print('Obj: %g' % model.objVal)
print("Finished")
print(" ")

f.close()

model.write('model_'+str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.lp')
model.write('model_'+str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.mps')


resultados = open ('Resultados_Prueba_'
              +str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','r')

line = resultados.readline()

# Funcion Objetivo

fobj = open ('FObj_'
              +str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','w')

fobj.write(str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str(' ')
              +line)

fobj.close()

#Located
  
located = open ('Located_'
              +str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','w')


count = 0
for i in range(len(x_vars)):
    aux = []
    line = resultados.readline().strip().split()
    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
        count = count + 1
        for i in range(len(line)):
            if i == 0:
                aux.append(line[i])
            else:
                aux.append(int(line[i]))
    
        # located.write(str(len(I))+str('_')
        #       +str(len(L))+str('_')
        #       +str(len(K))+str('_')
        #       +str(len(N))+str('_')
        #       +str(len(S))+str('_'))
        for j in range(len(aux)):
            located.write(str(aux[j])+str(" "))
        located.write("\n")
if count == 0:
    for j in range(8):
        located.write("NA"+str(' '))
    
located.close()

# Dispatched

dispatched = open ('Dispatched_'
              +str(len(I))+str('_')
              +str(len(L))+str('_')
              +str(len(K))+str('_')
              +str(len(N))+str('_')
              +str(len(S))+str('_')+str('Solution1_aik=0_todos')+'_.txt','w')

count = 0
for i in range(len(y_vars)):
    aux = []
    line = resultados.readline().strip().split()
    if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
        count = count + 1
        for i in range(len(line)):
            if i == 0:
                aux.append(line[i])
            else:
                aux.append(int(line[i]))
        # dispatched.write(str(len(I))+str('_')
        #       +str(len(L))+str('_')
        #       +str(len(K))+str('_')
        #       +str(len(N))+str('_')
        #       +str(len(S))+str('_'))
        for j in range(len(aux)):
            dispatched.write(str(aux[j])+str(" "))
        dispatched.write("\n")
if count == 0:
    for j in range(11):
        dispatched.write("NA"+str(' '))

dispatched.close()

# Null

# null = open ('Null_'
#               +str(len(I))+str('_')
#               +str(len(L))+str('_')
#               +str(len(K))+str('_')
#               +str(len(N))+str('_')
#               +str(len(S))+str('_')+'_.txt','w')


# count = 0
# for i in range(len(zfull_vars)):
#     aux = []
#     line = resultados.readline().strip().split()
#     if int(line[len(line)-1]) != 0 or int(line[len(line)-1]) != -0:
#         count = count + 1
#         for i in range(len(line)):
#             if i == 0:
#                 aux.append(line[i])
#             else:
#                 aux.append(int(line[i]))
#         null.write(str(len_I)+str(' ')
#                       +str(len_L)+str(' ')
#                       +str(len_S)+str(' ')
#                       +str(rep+1)+str(' '))
#         for j in range(len(aux)):
#             null.write(str(aux[j])+str(" "))
#         null.write("\n")
# if count == 0:
#     for j in range(9):
#         null.write("NA"+str(' '))

# null.close()

resultados.close()