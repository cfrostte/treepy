import numpy as np
import math
import matplotlib.pyplot as plt
import time


def VectorParalelo(N,U):
    c1 = float(N[1]/N[0])
    for i in range(len(U)):
        if U[i][0] != 0:
            c2 = float(U[i][1]/U[i][0])
            if c2 == c1:
                return i
        else:
            c2 = 0
            if c1 == 0:
                print(i)
                return i
# calculate distance
def calculateDistance(coords1, coords2):
    x_side = np.abs(coords2[0]-coords1[0])
    y_side = np.abs(coords2[1]-coords1[1])
    dist = (math.sqrt((x_side)**2+(y_side)**2))
    return dist

def distMin(N,U):
    dist = []
    for i in range(len(U)):
        dist.append(calculateDistance(N,U[i]))
    dist_min = np.min(dist)
    return dist.index(dist_min)

pi = math.pi
t1 = np.arange(0,2*pi,0.2)
x = []
y = []
nx = []
ny = []
dx = []
dy = []
x2 = []
y2 = []
nx2 = []
ny2 = []
dx2 = []
dy2 = []

for i in range(len(t1)):
    x.append(2*math.cos(t1[i]))
    y.append(2*math.sin(t1[i]))

t2 = np.arange(0,2*pi,0.2)

for i in range(len(t2)):
    x2.append(4*math.cos(t2[i]))
    y2.append(4*math.sin(t2[i]))
    dx.append(-2*math.sin(t2[i]))
    dy.append(2*math.cos(t2[i]))
    nx.append(2*math.cos(t2[i]))
    ny.append(2*math.sin(t2[i]))
    dx2.append(-4*math.sin(t2[i]))
    dy2.append(4*math.cos(t2[i]))
    nx2.append(4*math.cos(t2[i]))
    ny2.append(4*math.sin(t2[i]))

soa = []
for i in range(len(x)):
    soa.append([x[i],y[i],x2[i],y2[i]])

X, Y, U, V = zip(*soa)
plt.figure()
ax = plt.gca()
ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=2)
plt.plot(X,Y,U,V,'r-')
ax.set_xlim([-1, 10])
ax.set_ylim([-1, 10])
plt.draw()

plt.plot(x,y)
plt.plot(x2,y2)
plt.xlim(-5,5)
plt.ylim(-5,5)
plt.quiver(x,y,dx,dy,color=['r'], units = 'xy', scale = 10)
plt.quiver(x,y,nx,ny,color=['r'], units = 'xy', scale = 10)
plt.quiver(x2,y2,dx2,dy2,color=['b'], units = 'xy', scale = 10)
plt.quiver(x2,y2,nx2,ny2,color=['b'], units = 'xy', scale = 10)

p = 2
plt.plot(x[p],y[p],'mo')

U = []
for i in range(len(x2)):
    U.append((nx2[i],ny2[i]))

timei = time.time()
t1 = VectorParalelo((nx[p],ny[p]),U)
timef = time.time()
print('t1:',timei)
print('t2:',timef)
print('ejec:',np.abs(timei-timef))
print(t1)

plt.plot(x2[t1],y2[t1],'ro')
s = "Normal: " + str(np.abs(timei-timef))
plt.text(x2[t1]+0.3,y2[t1], s, bbox=dict(facecolor='green', alpha=0.5))


p1 = 3
p2 = (x[p1],y[p1])
plt.plot(p2[0],p2[1],'yo')
V = []
for i in range(len(x2)):
    V.append((x2[i],y2[i]))
print('t1:',timei)

timei2 = time.time()

t2 = distMin(p2,V)
timef2 = time.time()
plt.plot(x2[t2],y2[t2],'ro')
print('ti2:',timei2)
print('tf2:',timef2)
print('ejec2:',np.abs(timei2-timef2))
s1 = "Dist: " + str(np.abs(timei2-timef2))
plt.text(x2[t2]+0.3,y2[t2], s1, bbox=dict(facecolor='green', alpha=0.5))


print(t2)
plt.show()
