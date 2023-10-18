# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 16:54:56 2023

@author: beatr
"""

import xlrd
from xlrd import open_workbook
from xlutils.copy import copy

tamaños_I = [168, 270, 500, 900, 1500] #Hasta aquí puede bien el modelo
tamaños_L = [16, 30, 50, 70, 100]
tamaños_S = [10, 50, 100, 150, 200]

# tamaños_I = [1500] #Hasta aquí puede bien el modelo
# tamaños_L = [16, 30, 50, 70, 100]
# tamaños_S = [10, 50, 100]

eta = [35, 20]

rb = xlrd.open_workbook('Tesis_Obj_Zs_250923_'+str(eta[0])+'_'+str(eta[1])+'.xls')
wb = copy(rb)
ws = wb.get_sheet(0)

countcsv = 1


for iconj in range(len(tamaños_I)):
    for jconj in range(len(tamaños_L)):
        for sconj in range(len(tamaños_S)):
            
            archivo = open('Resultados_Prueba_Obj_Zs_210923_'
                      +str(tamaños_I[iconj])+str('_')
                      +str(tamaños_L[jconj])+str('_')
                      +str(tamaños_S[sconj])+'_'
                      +str(eta[0])+'_'+str(eta[1])
                      +'.txt', "r")
            
            archivo.readline()
            l = archivo.readline()
            num = float(l[5:len(l)-1])
            
            #print(num)
       
            ws.write(countcsv, 5, num)
            
            countcsv = countcsv + 1

wb.save('Tesis_Obj_Zs_270923_'+str(eta[0])+'_'+str(eta[1])+'.xls')
            
            