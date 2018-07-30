"""..."""

import random
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
        a.establecimiento = random.randint(123, 987)
        a.nroCuadro = random.randint(123, 987)
        a.suelo = random.randint(123, 987)
        a.espaciamientoX = random.randint(123, 987)
        a.espaciamientoY = random.randint(123, 987)
        a.plantasHa = random.randint(123, 987)
        a.fechaPlantacion = random.randint(123, 987)
        a.nroTratamientos = random.randint(123, 987)
        a.totalPlantas = random.randint(123, 987)
        a.totalHas = random.randint(123, 987)
        a.plantasParcela = random.randint(123, 987)
        a.tipoClonal = random.randint(123, 987)
        a.nroRepeticiones = random.randint(123, 987)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        nro TEXT NOT NULL,
        establecimiento TEXT NOT NULL,
        nroCuadro TEXT NOT NULL,
        suelo TEXT NOT NULL,
        espaciamientoX TEXT NOT NULL,
        espaciamientoY TEXT NOT NULL,
        plantasHa TEXT NOT NULL,
        fechaPlantacion TEXT NOT NULL,
        nroTratamientos TEXT NOT NULL,
        totalPlantas TEXT NOT NULL,
        totalHas TEXT NOT NULL,
        plantasParcela TEXT NOT NULL,
        tipoClonal TEXT NOT NULL,
        nroRepeticiones TEXT NOT NULL)"""
        return s.format(cls._tabla)
