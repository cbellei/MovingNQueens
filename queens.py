# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 14:01:57 2015

@author: admin-bellei
"""

import math

N = 9

p = np.empty([9,2])
r = []; #empty list of 
#determine position of queens at random inside square of size sqrt(N)<=SZ<=2*sqrt(N)
SZ1 = math.ceil(np.sqrt(N))
SZ2 = math.floor(2*np.sqrt(N))
SZ = np.random.randint(SZ1,SZ2)  
print "SZ = ", SZ
nq = 0
#
#for k in range(20):
while nq < 9:
    i = np.random.randint(1,SZ)       
    j = np.random.randint(1,SZ) 
    if [i,j] not in r: 
        r.append([i,j])
        p[nq,0] = i
        p[nq,1] = j        
        nq += 1
        
print p


qp = np.zeros([nCk(N,2),2])
#choose (N,2) pair of queens among the N queens
c = 0
for i in range(N):
    for j in range(i+1,N):
        qp[c] = [i,j] 
        c = c + 1
                
                        