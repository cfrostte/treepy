"""..."""

import random
from .core.Base import Base

class Repeticion(Base):

    _tabla = 'repeticiones'

    nro = None
    id_ensayos = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        r = Repeticion()
        r.nro = random.randint(123, 987)
        return r

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        id_ensayos INTEGER, 
        FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave))"""
        return s.format(cls._tabla)
