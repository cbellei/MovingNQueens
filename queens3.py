# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 10:29:15 2015

@author: admin-bellei
"""
import matplotlib.pyplot as plt
import math
import numpy as np
from functions import nCk
from functions import threatening_matrix, allowed_to_move
from functions import frame_matrix, queens_matrix

N = 100

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
               
##add buffer on the side to make sure we have a space of 2 * (8*N) + SZ 
T = np.ones([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
Q = np.ones([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
#T = np.ones([2 * (1*N) + SZ,2 * (1*N) + SZ],dtype=int)
##update position of queens
p[:,0] += 8 * N #+ math.floor(0.5*SZ) 
p[:,1] += 8 * N #+ math.floor(0.5*SZ) 


##move first 10 by 20 on the right
#p[0:40,0] += 30
#p[0:40,1] += 20
#
##move first 10 by 20 on the right
#p[40:80,0] -= 30
#p[40:80,1] -= 20


p0[:,0] = p[:,0]
p0[:,1] = p[:,1]


#
choose = 0; #choose the reference queen
print "position of chosen queen is ", p[choose]
T = threatening_matrix(p[choose],T) #contains threatening paths of increasing number of queens
Q = queens_matrix(p,Q) #matrix containing position of all queens


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

nmoves = 0
for queen in choose: #choose all queens (except for reference one)
    if not allowed_to_move(p[queen],p):
        continue
    safe = False #assume that initially, the queen is not in a safe position
    c = 0
    while not safe:
        sp =  frame_matrix(T,Q,p[queen],c)
        if sp!=[]:
            nmoves += c
            p[queen] = sp #update position of queen
            T = threatening_matrix(sp,T)
            Q = queens_matrix(p,Q)
            safe = True
        else:
            c +=1
    

G = np.zeros([2 * (8*N) + SZ,2 * (8*N) + SZ],dtype=int)
for i,par in enumerate(p0):
    G[p[i,0],p[i,1]] = 1
    print par, p[i] 
 
ax1 = plt.subplot(1,2,1)   
plt.imshow(P0,cmap='Greys',interpolation='nearest') 
plt.xlim([8*N - 3*SZ,8*N + 4*SZ])
plt.ylim([8*N - 3*SZ,8*N + 4*SZ])
ax1.set_title("Old Positions")

ax2 = plt.subplot(1,2,2)   
plt.imshow(G,cmap='Greys',interpolation='nearest') 
ax2.set_title("New Positions")
#ax2.set_xticks(np.arange(1,1000), minor=True)
#ax2.set_yticks(np.arange(1,1000), minor=True)
plt.xlim([8*N - 3*SZ,8*N + 4*SZ])
plt.ylim([8*N - 3*SZ,8*N + 4*SZ])
#plt.grid()

#plt.grid()
#ax2.set_xticks(np.arange(1,100))
#ax2.set_xticks()
#ax2.xlim([8*N - 5*SZ,8*N + 5*SZ])

plt.show()

print "nmoves = ", nmoves, "; Max Allowed Moves = ", 8 * N
print "--Does it satisfy nmoves < 8 * N??,  ", nmoves < 8 * N 