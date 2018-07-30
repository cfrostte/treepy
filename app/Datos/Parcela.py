"""..."""

import random
from .core.Base import Base
from .Arbol import Arbol

class Parcela(Base):

    _relacionados = {
        'Arbol' : Arbol,
    }

    _tabla = 'parcelas'

    fila = None
    columna = None
    id_bloques = None
    id_repeticiones = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Parcela()
        a.fila = random.randint(123, 987)
        a.columna = random.randint(123, 987)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        fila TEXT NOT NULL,
        columna TEXT NOT NULL,
        id_bloques INTEGER NOT NULL,
        id_clones INTEGER NOT NULL,
        FOREIGN KEY(id_bloques) REFERENCES bloques(clave),
        FOREIGN KEY(id_clones) REFERENCES clones(clave))"""
        return s.format(cls._tabla)
