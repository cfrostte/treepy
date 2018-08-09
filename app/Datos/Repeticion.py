"""..."""

import random

from .core.Base import Base
from .Bloque import Bloque
from .Imagen import Imagen

class Repeticion(Base):

    _relacionados = {
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
        a.nroFilas = random.randint(123, 987)
        a.nroColumnas = random.randint(123, 987)
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
