"""..."""

import random
from .core.Base import Base

class Ensayo(Base):

    tabla = 'ensayos'

    consulta = """CREATE TABLE IF NOT EXISTS {} (
    clave INTEGER PRIMARY KEY NOT NULL,
    nro TEXT NOT NULL)"""

    nro = None

    def __init__(self, nro, clave=None):
        Base.__init__(self, clave)
        self.nro = nro

    def __str__(self):
        return "clave=%s, nro=%s" % (self.clave, self.nro)

    @classmethod
    def id_disponible(cls, donde, tabla=None):
        return Base.id_disponible(donde, cls.tabla)

    def obtener(self, donde):
        fila = super().obtener(donde)
        if fila:
            return Ensayo(fila['nro'], fila['clave'])
        return None

    def guardar(self, donde, valores=None):
        return super().guardar(donde, (self.nro, ))

    @staticmethod
    def aleatorio():
        nro = random.randint(123, 987)
        return Ensayo(nro)
