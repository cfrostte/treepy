import numpy as np
import math
import matplotlib.pyplot as plt
import time


# derivada de VectorParalelo
def Derivada(y):
    dy = []
    for i in range(len(y)-1):
        dy.append(3*(y[i+1] - y[i]))
    dy.append(dy[len(dy)-1])
    return dy
# calculate distance
def calculateDistance(coords1, coords2):
    x_side = np.abs(coords2[0]-coords1[0])
    y_side = np.abs(coords2[1]-coords1[1])
    dist = (math.sqrt((x_side)**2+(y_side)**2))
    return dist

# index of dist min
def distMin(N,U):
    dist = []
    for i in range(len(U)):
        dist.append(calculateDistance(N,U[i]))
    dist_min = np.min(dist)
    return dist.index(dist_min)

t = np.arange(0,5*math.pi,0.1)

x = t
y1 = [math.sin(t[i]) for i in range(len(x))]
y2 = [math.sin(2*t[i]) for i in range(len(x))]
dx = 1

plt.plot(x,y1,'b--')
plt.plot(x,y2,'r--')

indx = 47
U = []
for i in range(len(x)):
    U.append((x[i],y2[i]))

t2_min = distMin((x[indx],y1[indx]),U)

plt.plot(x[indx],y1[indx],'o')
plt.plot(x[t2_min],y2[t2_min],'o')
plt.annotate('tension maxima', xy=(x[indx],y1[indx]), xytext=(x[t2_min],y2[t2_min]),arrowprops=dict(facecolor='black', shrink=0.02))


plt.show()
