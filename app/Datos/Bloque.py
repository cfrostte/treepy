"""..."""

import random
import string

from .core.Base import Base
from .Parcela import Parcela

class Bloque(Base):

    _relacionados = {
        'Parcela' : Parcela,
    }

    _tabla = 'bloques'

    color = None
    tipoSuelo = None
    id_repeticiones = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Bloque()
        a.color = ''.join([random.choice(string.ascii_letters + string.digits) for r in range(4)])
        a.tipoSuelo = ''.join([random.choice(string.ascii_letters + string.digits) for r in range(8)])
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        color TEXT NOT NULL,
        tipoSuelo TEXT NOT NULL,
        id_repeticiones INTEGER NOT NULL,
        FOREIGN KEY(id_repeticiones) REFERENCES repeticiones(clave))"""
        return s.format(cls._tabla)
