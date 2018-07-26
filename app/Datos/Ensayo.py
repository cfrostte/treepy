"""..."""

import random
from .core.Base import Base

class Ensayo(Base):

    tabla = 'ensayos'
    nro = None

    def __init__(self, nro=None, clave=None):
        Base.__init__(self, clave)
        self.nro = nro

    def __str__(self):
        return "clave=%s, nro=%s" % (self.clave, self.nro)

    @classmethod
    def crear_tabla(cls, donde):
        consulta = """CREATE TABLE IF NOT EXISTS {} (
        id INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL)""".format(cls.tabla)
        cls.consultar(donde, consulta)

    @classmethod
    def id_disponible(cls, donde, tabla=None):
        return Base.id_disponible(donde, cls.tabla)

    def obtener(self, donde):
        fila = super().obtener(donde)
        if fila:
            return Ensayo(fila['nro'], fila['id'])
        return None

    def guardar(self, donde):
        if self.obtener(donde): # Existe, entonces modificar:
            consulta = """UPDATE {} SET nro = ? WHERE id = ?""".format(self.tabla)
            self.consultar(donde, consulta, (self.nro, self.clave))
        else: # No existe, entonces crear
            consulta = """INSERT INTO {} (id, nro) VALUES (?, ?)""".format(self.tabla)
            clave = self.id_disponible(donde)
            self.consultar(donde, consulta, (clave, self.nro))
            self.clave = clave
        return self.obtener(donde)

    @staticmethod
    def aleatorio():
        nro = random.randint(123, 987)
        return Ensayo(nro)
