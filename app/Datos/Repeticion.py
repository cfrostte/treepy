"""..."""

import random
from .core.Base import Base

class Repeticion(Base):

    _tabla = 'repeticiones'

    # Columnas de la tabla:
    nro = None
    id_ensayos = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def desde_fila(f):
        r = Repeticion(f['clave'])
        r.nro = f['nro']
        return r

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

    @classmethod
    def id_disponible(cls, donde, _tabla=None):
        return Base.id_disponible(donde, cls._tabla)

    def obtener(self, donde):
        fila = super().obtener(donde)
        if fila:
            self = Repeticion(fila['clave'])
            self.nro = fila['nro']
            return self
        return None
