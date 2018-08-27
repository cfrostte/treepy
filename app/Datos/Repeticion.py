"""..."""

import random

from .core.Base import Base
from .Arbol import Arbol
from .Bloque import Bloque
from .Imagen import Imagen

class Repeticion(Base):

    _relacionados = {
        'Arbol' : Arbol,
        'Bloque' : Bloque,
        'Imagen' : Imagen,
    }

    _tabla = 'repeticiones'

    nro = None
    nroFilas = None
    nroColumnas = None
    id_ensayos = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Repeticion()
        a.nro = random.randint(123, 987)
        a.nroFilas = 10
        a.nroColumnas = 10
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro INTEGER NOT NULL,
        nroFilas INTEGER NOT NULL,
        nroColumnas INTEGER NOT NULL,
        id_ensayos INTEGER NOT NULL, 
        FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave))"""
        return s.format(cls._tabla)

    def matriz(self, donde):
        q = """SELECT p.fila, p.columna, b.color, c.nro
        FROM repeticiones AS r JOIN bloques AS b 
        JOIN parcelas AS p JOIN clones AS c
        WHERE r.clave = b.id_repeticiones AND b.clave = p.id_bloques 
        AND c.clave = p.id_clones AND r.clave = ?"""
        resultado = super().consultar(donde, q, (self.clave, ))
        m = [[0 for i in range(self.nroFilas)] for i in range(self.nroColumnas)]
        def datos(x, y):
            if resultado:
                for r in resultado:
                    x = int(x)
                    c = int(r['columna'])
                    y = int(y)
                    f = int(r['fila'])
                    if x == c and y == f:
                        return {'color' : r['color'], 'nro' : r['nro']}
            return {'color' : '#FFFFFF', 'nro' : ''}
        for x in range(self.nroColumnas):
            for y in range(self.nroFilas):
                m[x][y] = datos(x, y)
        return m