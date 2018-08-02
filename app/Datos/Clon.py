"""..."""

import random
from .core.Base import Base
from .Parcela import Parcela

class Clon(Base):

    _relacionados = {
        'Parcela' : Parcela,
    }

    _tabla = 'clones'

    nro = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Clon()
        a.nro = random.randint(123, 987)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro INTEGER NOT NULL)"""
        return s.format(cls._tabla)
