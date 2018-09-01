"""
Clase para realizar transformaciones afines para calcular
puntos geograficos en base a coordenadas de pixeles
"""

import numpy as N

def aumentar(a):
    """Agregue una columna final de unos para ingresar datos"""
    arr = N.ones((a.shape[0], a.shape[1]+1))
    arr[:, :-1] = a
    return arr

class GeoEspacial(object):

    def __init__(self, array=None):
        self.trans_matrix = array

    @classmethod
    def from_tiepoints(cls, fromCoords, toCoords):
        """Producir transformada afín mediante la ingesta de coordenadas locales y georreferenciadas para los puntos de enlace"""
        fromCoords = aumentar(N.array(fromCoords))
        toCoords = N.array(toCoords)
        trans_matrix, residuals, rank, sv = N.linalg.lstsq(fromCoords, toCoords)
        print('residuals', residuals)
        print('rank', rank)
        print('sv', sv)
        geoespacial = cls(trans_matrix) # Configurar la transformación afín de la matriz de transformación
        solucion = N.dot(fromCoords, geoespacial.trans_matrix) # Compute la solución del modelo
        print('solucion', solucion)
        return geoespacial

    def transform(self, points):
        """Transformar los datos proyectados localmente utilizando la matriz de transformación"""
        return N.dot(aumentar(N.array(points)), self.trans_matrix)        