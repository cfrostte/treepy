import random
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import pylab


def f(x):
	return x**2 + x

N=100
x = np.linspace(-100,100,N)
y = [f(x[i]) for i in range(len(x))]
n=np.random.normal(0,1,N)
yn = np.add(y,n)

z = np.polyfit(x, yn, 2)
p = np.poly1d(z)

e=np.abs(np.polyval(z, x) - y)
error = np.sum(e)
print(error)
print(error/N)

plt.plot(x,y,'g-',x,p(x),'b-')
plt.plot(x,yn,'.r')
plt.figure()
plt.plot(x,e)


plt.show()
