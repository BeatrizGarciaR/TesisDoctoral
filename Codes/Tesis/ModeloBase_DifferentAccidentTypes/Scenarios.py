# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 19:01:41 2021

@author: beatr
"""

import random

I = [1, 2, 3, 4, 5, 6, 7, 8]
L = [1, 2, 3, 4, 5]
N = [0, 1, 2, 3]

# Scenarios #

S = []
len_S = 3
probabilidades_S = [0.6, 0.8, 0.4, 0.1]
opciones_S = []

for e, p in zip(N, probabilidades_S):
    opciones_S += [e]*int(p*10000)

for i in range(len_S):
    S.append([])
    for j in range(len(I)):
        a = int(random.choice(opciones_S))
        S[i].append(a)
print (S)
print()


#Writing .txt

f = open ('Scenarios.txt','w')
f.write(str(len_S))
f.write("\n")
for s in range(len_S):
    for i in range(len(I)):
        f.write(str(S[s][i])+str(" "))
    f.write("\n")
f.close()