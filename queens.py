# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 14:01:57 2015

@author: admin-bellei
"""

import math
import numpy as np
from combinations import nCk


def threaten(p1,p2):
    #check if queens are on same row/column/diagonal
    if p1[0]==p2[0] or p1[1]==p2[1] or abs(p1[0]-p2[0])==abs(p1[1]-p2[1]): 
        return True;
    else:
        return False;

N = 10

p = np.zeros([N,2],dtype=int) #will store position of queens 
r = []; #record of positions

#determine position of queens at random inside square of size sqrt(N)<=SZ<=2*sqrt(N)
SZ1 = math.ceil(np.sqrt(N))
SZ2 = math.floor(2*np.sqrt(N))
SZ = np.random.randint(SZ1,SZ2+1)  

print "SZ = ", SZ
nq = 0
#
while nq < N:
    i = np.random.randint(1,SZ+1)       
    j = np.random.randint(1,SZ+1) 
    if [i,j] not in r:  #then this position is not already occupied
        r.append([i,j])
        p[nq,0] = i
        p[nq,1] = j        
        nq += 1
        
qp = np.zeros([nCk(N,2),2],dtype=int)
#choose (N,2) pair of queens among the N queens
c = 0
for q1 in range(N):
    for q2 in range(q1,N):
        if (q1!=q2):
            p1 = p[q1,:]
            p2 = p[q2,:]
            if ( not threaten(p1,p2) ):
                qp[c] = [q1,q2] 
                c += 1

qp = qp[0:c]

qpp = np.zeros([N*qp.shape[0],3],dtype=int)

c = 0
for n in range(N):
    for pair in qp: #check third particle
        if n not in pair:
            p1 = p[n,:]
            p2 = p[pair[0],:]
            p3 = p[pair[1],:]
            if ( not threaten(p1,p2) ) and ( not threaten(p1,p3) ):
                qpp[c] = [n,pair[0],pair[1]]
                c +=1
  
qpp = qpp[0:c,:]      

qppp = np.zeros([N*qpp.shape[0],4],dtype=int)
c = 0
for n in range(N):
    for triple in qpp: #check third particle
        if n not in triple:
            p1 = p[n,:]
            p2 = p[triple[0],:]
            p3 = p[triple[1],:]
            p4 = p[triple[2],:]
            if ( not threaten(p1,p2) ) and ( not threaten(p1,p3) ) and ( not threaten(p1,p4) ):
                qppp[c] = [n,triple[0],triple[1],triple[2]]
                c +=1

qppp = qppp[0:c,:] 

print qp.shape
print qpp.shape            
print qppp.shape            

    