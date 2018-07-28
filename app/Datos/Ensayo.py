"""..."""

import random
from .core.Base import Base
from .Repeticion import Repeticion

class Ensayo(Base):

    _tabla = 'ensayos'

    # Columnas de la tabla:
    nro = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def desde_fila(f):
        e = Ensayo(f['clave'])
        e.nro = f['nro']
        return e

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

    @classmethod
    def id_disponible(cls, donde, _tabla=None):
        return Base.id_disponible(donde, cls._tabla)

    def obtener(self, donde):
        fila = super().obtener(donde)
        if fila:
            self = Ensayo(fila['clave'])
            self.nro = fila['nro']
            return self
        return None

    # Asignacion u obtencion de objetos hijos:

    def repeticiones(self, donde, lista=None):
        if lista:
            for l in lista:
                l.id_ensayos = self.clave
                l.guardar(donde)
        return Repeticion.todos(donde, None, self)
