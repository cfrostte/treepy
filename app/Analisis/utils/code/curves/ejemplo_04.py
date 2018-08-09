'''
	Generate curve
	a partir de puntos (ginput)

'''

import random
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import pylab

def derivada(x,a,b):
	return (2*a*x + b)

plt.axis([0, 100,0, 100])
pts = plt.ginput(-1)

x = [pts[i][0] for i in range(len(pts))]
y = [pts[i][1] for i in range(len(pts))]

z = np.polyfit(x, y, 2)
p = np.poly1d(z)

xp = np.linspace(x[0], x[len(x)-1], 100)

error = np.sum((np.polyval(np.polyfit(x, y, 2), x) - y)**2)
print('E_abs:',error,'E_re:',error/len(x))
tx = []
ty = []
for i in range(len(xp)):
	norm = math.sqrt((1**2) + ((2*z[0]*xp[i] + z[1])**2))
	tx.append(1/norm)
	ty.append((2*z[0]*xp[i] + z[1])/norm)

plt.plot(x, y, '-o', xp, p(xp),'-')
for i in range(10):
	plt.quiver(xp[i*4],p(xp[i*4]),tx[i*4],ty[i*4],color=['r'], units = 'xy', scale = 0.1)
	plt.quiver(xp[i*4],p(xp[i*4]),-ty[i*4],tx[i*4],color=['r'], units = 'xy', scale = 0.1)

plt.show()
