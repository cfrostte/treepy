"""..."""

from .core.Base import Base

class ArbolFaltante(Base):

    _tabla = 'arboles_faltantes'

    id_imagenes = None
    id_arboles = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = ArbolFaltante()
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        id_imagenes INTEGER NOT NULL,
        id_arboles INTEGER NOT NULL,
        FOREIGN KEY(id_imagenes) REFERENCES imagenes(clave),
        FOREIGN KEY(id_arboles) REFERENCES arboles(clave))"""
        return s.format(cls._tabla)
