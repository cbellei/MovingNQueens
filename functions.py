# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 13:48:43 2015

@author: admin-bellei
"""

from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
import math
import numpy as np

def nCk(n,k): 
  return int( reduce(mul, (Fraction(n-i, i+1) for i in range(k)) ) )
  

def threatening_matrix(pq,A): #pw = position of queen to add, A = threatening matrix
    L = A.shape[0]
        
    A[pq[0],:] = 0
    A[:,pq[1]] = 0
    border1 = np.maximum(- pq[0], - pq[1])
    border2 = np.minimum(L - pq[0], L - pq[1])
    d1 = [ [pq[0] + m, pq[1] + m] for m in np.arange(border1,border2) ]
    for k in range(len(d1)):
        A[d1[k][0],d1[k][1]] = 0
    border1 = np.minimum(pq[1], L - pq[0])
    border2 = np.minimum(L - pq[1], pq[0])
    d1 = [ [pq[0] + m, pq[1] - m] for m in np.arange(1,border1) ]
    d2 = [ [pq[0] - m, pq[1] + m] for m in np.arange(1,border2) ]
    for k in range(len(d2)):
        A[d2[k][0],d2[k][1]] = 0
    d2 = [ [pq[0] + m, pq[1] - m] for m in np.arange(1,border1) ]
    for k in range(len(d2)):
        A[d2[k][0],d2[k][1]] = 0
   
    return A  


def queens_matrix(p,A): #add position of queens in threatening matrix
    for pos in p:
        A[pos[0],pos[1]] = 0     
    return A

def allowed_to_move(pq,p): #check if current queen can even move (could be surrounded by other queens)
    #these are the 8 cells surrounding the queen
    check = [ [pq[0],pq[1]-1],[pq[0],pq[1]+1], \
            [pq[0]-1,pq[1]],[pq[0]+1,pq[1]], \
            [pq[0]-1,pq[1]-1],[pq[0]+1,pq[1]+1], \
            [pq[0]-1,pq[1]+1],[pq[0]+1,pq[1]-1] ]
    
    v = np.zeros(8,dtype=int)
    p = p.tolist() #transform into list to check existence of pairs
    for i, ch in enumerate(check):
        if ch in p:
            v[i] = 1
                
    if sum(v) == 8: #then it can't move
        print "can't move!!"
        return False
    else:
        return True
        
def frame_matrix(T,Q,p,c):
    sp = [] #safe position is initially empty    
    
    v1 = [[p[0]-c,p[1]+m] for m in range(-c,c+1)]
    v2 = [[p[0]+c,p[1]+m] for m in range(-c,c+1)]
    v3 = [[p[0]+m,p[1]-c] for m in range(-c+1,c)]
    v4 = [[p[0]+m,p[1]+c] for m in range(-c+1,c)]
        
    v = v1 + v2 + v3 + v4 #this is the full frame to consider
            
    for i,p in enumerate(v):
        if T[v[i][0],v[i][1]] == 1 and Q[v[i][0],v[i][1]]: #then it's safe
#            print "safe!"
            sp = np.array([v[i][0],v[i][1]]) 
            return sp;
            
    return sp #we only get here if there is no safe place in this frame

def delete_queen(p,A): #delete position of queen after it has been moved
    print "delete queen in position", p
    A[p[0],p[1]] = 1 #this position is now safe
    return A

