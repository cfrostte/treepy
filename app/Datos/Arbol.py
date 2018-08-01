"""..."""

import random
from .core.Base import Base
from .ArbolFaltante import ArbolFaltante

class Arbol(Base):

    _relacionados = {
        'ArbolFaltante' : ArbolFaltante,
    }

    _tabla = 'arboles'

    latitud = None
    longitud = None
    arbolIzq = None
    arbolDer = None
    areaCopa = None
    primero = None
    id_parcelas = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Arbol()
        a.latitud = random.randint(123, 987)
        a.longitud = random.randint(123, 987)
        a.arbolIzq = random.randint(123, 987)
        a.arbolDer = random.randint(123, 987)
        a.areaCopa = random.randint(123, 987)
        a.primero = random.randint(123, 987)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        latitud TEXT NOT NULL,
        longitud TEXT NOT NULL,
        arbolIzq TEXT NOT NULL,
        arbolDer TEXT NOT NULL,
        areaCopa TEXT NOT NULL,
        primero TEXT NOT NULL,
        id_parcelas INTEGER NOT NULL,
        FOREIGN KEY(id_parcelas) REFERENCES parcelas(clave))"""
        return s.format(cls._tabla)
