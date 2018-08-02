"""

********************************************************************************
                            Controlador de Datos
********************************************************************************

Se encarga de de crear las tablas necesarias para los objetos de tipo Base;
crea y lista objetos de tipo Base, vuelca datos de prueba y respalda la BD.

"""

import sqlite3
import random

from Datos.Arbol import Arbol
from Datos.ArbolFaltante import ArbolFaltante
from Datos.Bloque import Bloque
from Datos.Clon import Clon
from Datos.Ensayo import Ensayo
from Datos.Imagen import Imagen
from Datos.Parcela import Parcela
from Datos.Repeticion import Repeticion
from Datos.SurcoDetectado import SurcoDetectado
from Datos.SurcoDetectadoParcela import SurcoDetectadoParcela

from Utilidades import Logger as log

class ControladorDatos(object):

    db = 'Datos/store/treepy.db' # Donde se guarda la BD
    sql = 'Datos/store/treepy.sql' # Donde se exporta la BD

    # Tipos de objeto manejados:
    controlados = {
        'Arbol' : Arbol,
        'ArbolFaltante' : ArbolFaltante,
        'Bloque' : Bloque,
        'Clon' : Clon,
        'Ensayo' : Ensayo,
        'Imagen' : Imagen,
        'Parcela' : Parcela,
        'Repeticion' : Repeticion,
        'SurcoDetectado' : SurcoDetectado,
        'SurcoDetectadoParcela' : SurcoDetectadoParcela,
    }

    ############################################################################

    @classmethod
    def crear_objeto(cls, tipo):
        """..."""
        return cls.controlados[tipo].__new__(cls.controlados[tipo])

    @classmethod
    def buscar_objetos(cls, tipo, filtro=None, orden=None, asc=True, limite=None):
        """..."""
        return cls.controlados[tipo].buscar(cls.db, filtro, orden, asc, limite)

    @classmethod
    def obtener_relaciones_de(cls, uno, muchos, guardar=True, filtro=None, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, guardar, None, filtro, fk)

    @classmethod
    def relacionar_uno_muchos(cls, uno, muchos, guardar=True, lista=None, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, guardar, lista, None, fk)

    @classmethod
    def relacionar_muchos_muchos(cls, muchos_x, muchos_y):
        """..."""
        n1 = muchos_x[0].__class__.__name__
        n2 = muchos_y[0].__class__.__name__
        pivot = cls.controlados[n1 + n2]
        for x in muchos_x:
            for y in muchos_y:
                p = pivot()
                setattr(p, x.foranea(), x.clave)
                setattr(p, y.foranea(), y.clave)
                p.guardar(cls.db, False)

    ############################################################################

    @classmethod
    def crear_estructura(cls):
        """..."""
        log.debug('Creando estructura')
        for nombre, clase in cls.controlados.items():
            print(nombre)
            clase.crear_tabla(cls.db)

    ############################################################################

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        log.debug('Volcando datos de prueba')
        def f(padres, hijos, guardar):
            r = random.choice(padres)
            n = hijos[0].__class__.__name__
            cls.relacionar_uno_muchos(r, n, guardar, hijos)
        def g():
            return random.randint(1, 256)
        arboles = cls.crear_objetos_prueba(Arbol, g(), False)
        arboles_faltantes = cls.crear_objetos_prueba(ArbolFaltante, g(), False)
        bloques = cls.crear_objetos_prueba(Bloque, g(), False)
        clones = cls.crear_objetos_prueba(Clon, g())
        ensayos = cls.crear_objetos_prueba(Ensayo, g())
        imagenes = cls.crear_objetos_prueba(Imagen, g(), False)
        parcelas = cls.crear_objetos_prueba(Parcela, g(), False)
        repeticiones = cls.crear_objetos_prueba(Repeticion, g(), False)
        surcos_detectados = cls.crear_objetos_prueba(SurcoDetectado, g(), False)
        f(ensayos, repeticiones, True)
        f(repeticiones, bloques, True)
        f(repeticiones, imagenes, True)
        f(clones, parcelas, False)
        f(bloques, parcelas, True)
        f(parcelas, arboles, True)
        f(arboles, arboles_faltantes, False)
        f(imagenes, arboles_faltantes, True)
        f(imagenes, surcos_detectados, True)
        cls.relacionar_muchos_muchos(surcos_detectados, parcelas)

    @classmethod
    def crear_objetos_prueba(cls, estatico, n, guardar=True):
        """..."""
        objetos_creados = []
        for r in range(0, n):
            if guardar:
                o = estatico.aleatorio().guardar(cls.db)
            else:
                o = estatico.aleatorio()
            objetos_creados.append(o)
            print('{} : {}'.format(r, o))
        return objetos_creados

    ############################################################################

    @classmethod
    def respaldar_datos(cls):
        """..."""
        log.debug('Respaldando datos')
        conexion = sqlite3.connect(cls.db)
        with open(cls.sql, 'w') as a:
            for linea in conexion.iterdump():
                print(linea)
                a.write('%s\n' % linea)

################################################################################

log.init(ControladorDatos) # Inicializa el Logger para que guarde correctamente
