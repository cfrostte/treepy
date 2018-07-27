"""..."""

import random
from .core.Base import Base

class Repeticion(Base):

    _tabla = 'repeticiones'

    _consulta = """CREATE TABLE IF NOT EXISTS {} (
    clave INTEGER PRIMARY KEY NOT NULL,
    nro TEXT NOT NULL,
    id_ensayos INTEGER, 
    FOREIGN KEY(id_ensayos) REFERENCES ensayos(clave))"""

    # Colecciones en memoria:
    _bloques = None

    # Columnas de la tabla:
    nro = None

    def __init__(self, nro, clave=None):
        Base.__init__(self, clave)
        self.nro = nro
        self._bloques = []

    @staticmethod
    def desde_fila(f):
        return Repeticion(f['nro'], f['clave'])

    @staticmethod
    def aleatorio():
        nro = random.randint(123, 987)
        return Repeticion(nro)

    @classmethod
    def id_disponible(cls, donde, _tabla=None):
        return Base.id_disponible(donde, cls._tabla)

    def obtener(self, donde):
        fila = super().obtener(donde)
        if fila:
            return Repeticion(fila['nro'], fila['clave'])
        return None

    def guardar(self, donde, valores=None):
        return super().guardar(donde, (self.nro, ))
