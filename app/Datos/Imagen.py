"""..."""

import random
from .core.Base import Base
from .ArbolFaltante import ArbolFaltante
from .SurcoDetectado import SurcoDetectado

class Imagen(Base):

    _relacionados = {
        'ArbolFaltante' : ArbolFaltante,
        'SurcoDetectado' : SurcoDetectado,
    }

    _tabla = 'imagenes'

    etapa = None
    fecha = None
    url = None
    largo = None
    ancho = None
    latitud = None
    longitud = None
    altitud = None
    latitudCono1 = None
    longitudCono1 = None
    latitudCono2 = None
    longitudCono2 = None
    id_repeticiones = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Imagen()
        a.etapa = random.randint(123, 987)
        a.fecha = random.randint(123, 987)
        a.url = random.randint(123, 987)
        a.largo = random.randint(123, 987)
        a.ancho = random.randint(123, 987)
        a.latitud = random.randint(123, 987)
        a.longitud = random.randint(123, 987)
        a.altitud = random.randint(123, 987)
        a.latitudCono1 = random.randint(123, 987)
        a.longitudCono1 = random.randint(123, 987)
        a.latitudCono2 = random.randint(123, 987)
        a.longitudCono2 = random.randint(123, 987)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        etapa TEXT NOT NULL,
        fecha TEXT NOT NULL,
        url TEXT NOT NULL,
        largo TEXT NOT NULL,
        ancho TEXT NOT NULL,
        latitud TEXT NOT NULL,
        longitud TEXT NOT NULL,
        altitud TEXT NOT NULL,
        latitudCono1 TEXT NOT NULL,
        longitudCono1 TEXT NOT NULL,
        latitudCono2 TEXT NOT NULL,
        longitudCono2 TEXT NOT NULL,
        id_repeticiones INTEGER NOT NULL,
        FOREIGN KEY(id_repeticiones) REFERENCES repeticiones(clave))"""
        return s.format(cls._tabla)
