# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 16:17:42 2021

@author: beatr
"""

import random

# Sets #
I = [1, 2, 3, 4, 5, 6, 7, 8]
L = [1, 2, 3, 4, 5]

# Response time from potential site to demand point #
r_li = []
for l in range(len(L)):
    r_li.append([])
    for i in range(len(I)):
        b = random.randint(9, 32)
        r_li[l].append(b)
print (r_li)

#Writing .txt

f = open ('Response_times.txt','w')
for l in range(len(L)):
    for i in range(len(I)):
        f.write(str(r_li[l][i])+str(" "))
    f.write("\n")
f.close()