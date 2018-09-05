"""..."""

import datetime
import random
import string

from .core.Base import Base
from .Repeticion import Repeticion

class Ensayo(Base):

    _relacionados = {
        'Repeticion' : Repeticion,
    }

    _tabla = 'ensayos'

    nro = None
    establecimiento = None
    nroCuadro = None
    suelo = None
    espaciamientoX = None
    espaciamientoY = None
    plantasHa = None
    fechaPlantacion = None
    nroTratamientos = None
    totalPlantas = None
    totalHas = None
    plantasParcela = None
    tipoClonal = None
    nroRepeticiones = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Ensayo()
        a.nro = random.randint(123, 987)
        a.establecimiento = ''.join([random.choice(string.ascii_letters + string.digits) for r in range(16)])
        a.nroCuadro = random.randint(123, 987)
        a.suelo = random.randint(123, 987)
        a.espaciamientoX = random.randint(123, 987)
        a.espaciamientoY = random.randint(123, 987)
        a.plantasHa = random.randint(123, 987)
        a.fechaPlantacion = datetime.datetime(random.randint(2008, 2018), random.randint(1, 12), random.randint(1, 28))
        a.nroTratamientos = random.randint(123, 987)
        a.totalPlantas = random.randint(123, 987)
        a.totalHas = random.randint(123, 987)
        a.plantasParcela = random.randint(123, 987)
        a.tipoClonal = ''.join([random.choice(string.ascii_letters + string.digits) for r in range(4)])
        a.nroRepeticiones = random.randint(1, 3)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro INTEGER NOT NULL,
        establecimiento TEXT NOT NULL,
        nroCuadro INTEGER NOT NULL,
        suelo TEXT NOT NULL,
        espaciamientoX TEXT NOT NULL,
        espaciamientoY TEXT NOT NULL,
        plantasHa INTEGER NOT NULL,
        fechaPlantacion TEXT NOT NULL,
        nroTratamientos INTEGER NOT NULL,
        totalPlantas INTEGER NOT NULL,
        totalHas INTEGER NOT NULL,
        plantasParcela INTEGER NOT NULL,
        tipoClonal TEXT NOT NULL,
        nroRepeticiones INTEGER NOT NULL)"""
        return s.format(cls._tabla)
