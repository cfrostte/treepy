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
y2 = [math.sin(3*t[i]) for i in range(len(x))]
dx = 1

plt.plot(x,y1,'b--')
plt.plot(x,y2,'r--')

t2 = np.arange(0,5*math.pi,1)
for i in range(len(t2)):
    plt.plot(t2[i],math.sin(t2[i]),'bo',t2[i],math.sin(3*t2[i]),'ro')
    # ------------------------------------
    norm1 = np.sqrt((1**2) + (math.cos(t2[i])**2))
    norm2 = np.sqrt((1**2) + ((3*math.cos(3*t2[i])**2)))

    plt.quiver(t2[i],math.sin(t2[i]), 1/norm1 ,math.cos(t2[i])/norm1 ,color=['b'], units = 'xy', scale = 2)
    plt.quiver(t2[i],math.sin(t2[i]),-math.cos(t2[i])/norm2, 1/norm1,color=['b'], units = 'xy', scale = 2)
    # ------------------------------------
    plt.quiver(t2[i],math.sin(3*t2[i]),1/norm2,3*math.cos(3*t2[i])/norm2,color=['r'], units = 'xy', scale = 2)
    plt.quiver(t2[i],math.sin(3*t2[i]),-3*math.cos(3*t2[i])/norm2,1/norm2,color=['r'], units = 'xy', scale = 2)
    # plt.quiver(t2[i],math.sin(3*t2[i]),(1/np.sqrt((1**2) + (3*math.cos(3*t2[i])**2) )),3*math.cos(3*t2[i]),color=['r'], units = 'xy', scale = 2)
    # plt.quiver(t2[i],math.sin(3*t2[i]),-3*math.cos(3*t2[i]),(1/np.sqrt((1**2) + (3*math.cos(3*t2[i])**2))),color=['r'], units = 'xy', scale = 2)



plt.show()
