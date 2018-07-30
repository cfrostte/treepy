"""..."""

import random
from .core.Base import Base

class SurcoDetectado(Base):

    _tabla = 'surcos_detectados'

    distanciaMedia = None
    anguloMedio = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = SurcoDetectado()
        a.distanciaMedia = random.randint(123, 987)
        a.anguloMedio = random.randint(123, 987)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        distanciaMedia TEXT NOT NULL,
        anguloMedio TEXT NOT NULL)"""
        return s.format(cls._tabla)
