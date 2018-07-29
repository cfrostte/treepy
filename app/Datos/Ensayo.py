"""..."""

import random
from .core.Base import Base
from .Repeticion import Repeticion

class Ensayo(Base):

    _relacionados = {
        'Repeticion' : Repeticion,
    }

    _tabla = 'ensayos'

    nro = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        e = Ensayo()
        e.nro = random.randint(123, 987)
        return e

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL)"""
        return s.format(cls._tabla)
