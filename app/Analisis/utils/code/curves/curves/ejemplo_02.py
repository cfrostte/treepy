import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import barycentric_interpolate

def f(x): # sample function
 return np.sin(x)

# Se evalua la funcion en el rango de -2 a 4 con 150 intervalos
x = np.linspace(-2,20,200)
#Se le pasa a la funcion los valores definidos en x.
y = f(x)

#Se le pasa el punto a calcular la tangente de la curva.
a = [2.5, 5.5, 15.5, 30.5]

#Se le pasa el diferencial con un valor de 0.1
h = 0.1
#Se calcula la derivada.
for i in range(len(a)):
    x2 = np.linspace(a[i],a[i]+0.5,2)
    fprime = (f(a[i]+h)-f(a[i]))/h # derivative
    tan = f(a[i])+fprime*(x2-a[i])
    plt.plot(x2,tan,'-r')
    plt.quiver(x2,a[i],x2,tan,color=['b'], units = 'xy', scale = 5)

#Se calcula la tangente
  # tangent

# Se grafica la funcion y la tangente.
plt.plot(x,y,'b',a,f(a),'om')
#Se muestra la grafica.
plt.show()
