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
    areaCopa = None
    primero = None
    arbolIzq = None # FK
    arbolDer = None # FK
    id_parcelas = None
    id_repeticiones = None
    id_surcos_detectados = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Arbol()
        a.latitud = random.uniform(-180, 180)
        a.longitud = random.uniform(-90, 90)
        a.areaCopa = random.random() * random.randint(123, 987)
        a.primero = random.randint(0, 1)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        latitud REAL NOT NULL,
        longitud REAL NOT NULL,
        areaCopa REAL NOT NULL,
        primero INTEGER NOT NULL,
        arbolIzq INTEGER,
        arbolDer INTEGER,
        id_parcelas INTEGER,
        id_repeticiones INTEGER NOT NULL,
        id_surcos_detectados INTEGER,
        FOREIGN KEY(arbolIzq) REFERENCES arboles(clave),
        FOREIGN KEY(arbolDer) REFERENCES arboles(clave),
        FOREIGN KEY(id_parcelas) REFERENCES parcelas(clave),
        FOREIGN KEY(id_repeticiones) REFERENCES repeticiones(clave),
        FOREIGN KEY(id_surcos_detectados) REFERENCES surcos_detectados(clave))"""
        return s.format(cls._tabla)
