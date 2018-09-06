"""..."""

import datetime
import random
import string

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
    grafo = None
    id_repeticiones = None

    def __init__(self, clave=None):
        Base.__init__(self, clave)

    @staticmethod
    def aleatorio():
        a = Imagen()
        a.etapa = random.randint(123, 987)
        a.fecha = datetime.datetime(random.randint(2008, 2018), random.randint(1, 12), random.randint(1, 28))
        a.url = ''.join([random.choice(string.ascii_letters + string.digits) for r in range(128)])
        a.largo = random.random() * random.randint(123, 987)
        a.ancho = random.random() * random.randint(123, 987)
        a.latitud = random.uniform(-180, 180)
        a.longitud = random.uniform(-90, 90)
        a.altitud = random.random() * random.randint(123, 987)
        a.latitudCono1 = random.uniform(-180, 180)
        a.longitudCono1 = random.uniform(-90, 90)
        a.latitudCono2 = random.uniform(-180, 180)
        a.longitudCono2 = random.uniform(-90, 90)
        return a

    @classmethod
    def sentencia(cls):
        s = """CREATE TABLE IF NOT EXISTS {} (
        clave INTEGER PRIMARY KEY NOT NULL,
        etapa INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        url TEXT NOT NULL,
        largo REAL NOT NULL,
        ancho REAL NOT NULL,
        latitud REAL NOT NULL,
        longitud REAL NOT NULL,
        altitud REAL NOT NULL,
        latitudCono1 REAL NOT NULL,
        longitudCono1 REAL NOT NULL,
        latitudCono2 REAL NOT NULL,
        longitudCono2 REAL NOT NULL,
        grafo BLOB,        
        id_repeticiones INTEGER NOT NULL,
        FOREIGN KEY(id_repeticiones) REFERENCES repeticiones(clave))"""
        return s.format(cls._tabla)
