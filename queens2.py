# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 10:29:15 2015

@author: admin-bellei
"""
import matplotlib.pyplot as plt
import math
import numpy as np
from functions import nCk

N = 100
        
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
    
def add_queens(p,A): #add position of queens in threatening matrix
    for pos in p:
        A[pos[0],pos[1]] = 0 
    
    return A
    
#def delete_queen(p,A): #delete position of queen after it has been moved
#    print "delete queen in position", p
#    A[p[0],p[1]] = 1 #this position is now safe
#    return A
    
def allowed_to_move(pq,p): #check if current queen can even move (could be surrounded by other queens)
    #these are the 8 cells surrounding the queen
    check = [ [pq[0],pq[1]-1],[pq[0],pq[1]+1], \
            [pq[0]-1,pq[1]],[pq[0]+1,pq[1]], \
            [pq[0]-1,pq[1]-1],[pq[0]+1,pq[1]+1], \
            [pq[0]-1,pq[1]+1],[pq[0]+1,pq[1]-1] ]
    
    v = np.zeros(8,dtype=int)
    for i, ch in enumerate(check):
        if ch in p:
            v[i] = 1
            
    if sum(v) == 8: #then it can't move
        return False
    else:
        print "it's surrounded"
        return True
    
def frame_matrix(T,p,c):

    sp = [] #safe position is initially empty    
    
    v1 = [[p[0]-c,p[1]+m] for m in range(-c,c+1)]
    v2 = [[p[0]+c,p[1]+m] for m in range(-c,c+1)]
    v3 = [[p[0]+m,p[1]-c] for m in range(-c+1,c)]
    v4 = [[p[0]+m,p[1]+c] for m in range(-c+1,c)]
        
    v = v1 + v2 + v3 + v4 #this is the full frame to consider
    
#    print p[0], p[1]
#    print v1
#    print v2
#    print v3
#    print v4
    
#    print T[p[0],p[1]]
        
    for i,p in enumerate(v):
        if T[v[i][0],v[i][1]] == 1: #then it's safe
#            print "safe!"
            sp = np.array([v[i][0],v[i][1]]) 
            return sp;
            
    return sp #we only get here if there is no safe place in this frame
    
p = np.zeros([N,2],dtype=int) #will store position of queens 
p0 = np.zeros([N,2],dtype=int) #will store initial position of queens 
r = []; #record of positions

#determine position of queens at random inside square of size sqrt(N)<=SZ<=2*sqrt(N)
SZ1 = math.ceil(np.sqrt(N))
SZ2 = math.floor(2*np.sqrt(N))
SZ = np.random.randint(SZ1,SZ2+1)  


#SZ=4  #USED FOR TESTING

print "SZ = ", SZ
nq = 0
M = np.ones([SZ,SZ],dtype=int)

while nq < N:
    i = np.random.randint(1,SZ+1)       
    j = np.random.randint(1,SZ+1) 
    if [i,j] not in r:  #then this position is not already occupied
        r.append([i,j])
        M[i-1,j-1] = 0
        p[nq,0] = i
        p[nq,1] = j        
        nq += 1

# USED FOR TESTING
#p = np.zeros([N,2],dtype=int) #will store position of queens  
#p[0,0] = 5
#p[0,1] = 5
#p[1,0] = 5
#p[1,1] = 8
               
##add buffer on the side to make sure we have a space of 2 * (8*N) + SZ 
T = np.ones([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
#T = np.ones([2 * (1*N) + SZ,2 * (1*N) + SZ],dtype=int)
##update position of queens
p[:,0] += 8 * N + math.floor(0.5*SZ) #8 * N + math.floor(0.5*SZ)
p[:,1] += 8 * N + math.floor(0.5*SZ) # 8 * N + math.ceil(0.5*SZ)

p0[:,0] = p[:,0]
p0[:,1] = p[:,1]

#
choose = 0; #choose the reference queen
print "position of chosen queen is ", p[choose]
T = threatening_matrix(p[choose],T)
T = add_queens(p,T) #add position of all queens in threatening matrix: they are not allowed positions!

#
#plt.imshow(T,interpolation='nearest',cmap='Greys') 
##plt.grid(color='w')
#ax = plt.gca()
#ax.set_xticks(np.arange(1,SZ+1))
#ax.set_yticks(np.arange(1,SZ+1))
#plt.show()

choose = np.arange(1,N) #choose particles (apart from reference one)
#choose = np.array([1]) #USED FOR TESTING

G = np.zeros([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
G[p[0,0],p[0,1]] = 1

P0 = np.zeros([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
for pos in p:
    P0[pos[0],pos[1]] = 1


#plt.figure(plt.figsize(10,30))
plt.subplot(131)
plt.imshow(P0,cmap='Greys',interpolation='nearest') 
plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
plt.ylim([8*N - 2*SZ,8*N + 3*SZ])  

plt.subplot(132)
plt.imshow(G,cmap='Greys',interpolation='nearest') 
plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
plt.ylim([8*N - 2*SZ,8*N + 3*SZ])  

plt.subplot(133)
G = np.zeros([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
G[:] = T[:]
plt.imshow(G,cmap='Greys',interpolation='nearest') 
plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
plt.ylim([8*N - 2*SZ,8*N + 3*SZ])  

#plt.figure(plt.figsize(10,10))

nmoves = 0
for queen in choose: #choose all queens (except for reference one)
    if not allowed_to_move(p[queen],p):
        break
    T = delete_queen(p[queen],T)  #the current queen position is not a treat for that very queen 
    safe = False #assume that initially, the queen is not in a safe position
    c = 0
    while not safe:
        sp =  frame_matrix(T,p[queen],c)
        if sp!=[]:
            nmoves += c
            p[queen] = sp #update position of queen
            T = threatening_matrix(sp,T)

#            plt.subplot(234)
#            plt.imshow(T,cmap='Greys',interpolation='nearest') 
#            plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
#            plt.ylim([8*N - 2*SZ,8*N + 3*SZ])
#            plt.show()

            G[sp[0],sp[1]] = 1
#            print "new queen is at ", sp
#            plt.figure()
#            plt.subplot(121)
#            plt.imshow(G,cmap='Greys',interpolation='nearest') 
#            plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
#            plt.ylim([8*N - 2*SZ,8*N + 3*SZ])  
#
#            plt.subplot(122)
#            plt.imshow(T,cmap='Greys',interpolation='nearest') 
#            plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
#            plt.ylim([8*N - 2*SZ,8*N + 3*SZ])  
#            plt.show()
            safe = True
        else:
            c +=1
    
#plt.figure()    
#plt.imshow(T,cmap='Greys',interpolation='nearest') 
#plt.xlim([8*N - 2*SZ,8*N + 3*SZ])
#plt.ylim([8*N - 2*SZ,8*N + 3*SZ])
#plt.grid(color='w')
#ax = plt.gca()
#ax.set_xticks(np.arange(1,SZ+1))
#ax.set_yticks(np.arange(1,SZ+1))
#plt.show()

G = np.zeros([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
for i,par in enumerate(p0):
    G[p[i,0],p[i,1]] = 1
    print par, p[i] 
 
ax1 = plt.subplot(1,2,1)   
plt.imshow(P0,cmap='Greys',interpolation='nearest') 
plt.xlim([8*N - 5*SZ,8*N + 5*SZ])
plt.ylim([8*N - 5*SZ,8*N + 5*SZ])
ax1.set_title("Old Positions")

ax2 = plt.subplot(1,2,2)   
plt.imshow(G,cmap='Greys',interpolation='nearest') 
plt.xlim([8*N - 5*SZ,8*N + 5*SZ])
plt.ylim([8*N - 5*SZ,8*N + 5*SZ])
ax2.set_title("New Positions")

plt.show()

print "nmoves = ", nmoves, "; Max Allowed Moves = ", 8 * N
print "--Does it satisfy nmoves < 8 * N??,  ", nmoves < 8 * N 