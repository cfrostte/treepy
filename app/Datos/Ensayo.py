"""..."""

import random
from .core.Base import Base
from .Repeticion import Repeticion

class Ensayo(Base):

    _tabla = 'ensayos'

    _consulta = """CREATE TABLE IF NOT EXISTS {} (
    clave INTEGER PRIMARY KEY NOT NULL,
    nro TEXT NOT NULL)"""

    # Colecciones en memoria:
    _repeticiones = None

    # Columnas de la tabla:
    nro = None

    def __init__(self, nro, clave=None):
        Base.__init__(self, clave)
        self.nro = nro
        self._repeticiones = []

    @staticmethod
    def desde_fila(f):
        return Ensayo(f['nro'], f['clave'])

    @staticmethod
    def aleatorio():
        nro = random.randint(123, 987)
        return Ensayo(nro)

    @classmethod
    def id_disponible(cls, donde, _tabla=None):
        return Base.id_disponible(donde, cls._tabla)

    def obtener(self, donde):
        fila = super().obtener(donde)
        if fila:
            e = Ensayo(fila['nro'], fila['clave'])
            e._repeticiones = Repeticion.todos(donde, None, self)
            return e
        return None

    def guardar(self, donde, valores=None):
        return super().guardar(donde, (self.nro, ))
