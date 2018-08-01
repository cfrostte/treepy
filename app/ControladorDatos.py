"""

********************************************************************************
                            Controlador de Datos
********************************************************************************

Se encarga de de crear las tablas necesarias para los objetos de tipo Base;
crea y lista objetos de tipo Base, vuelca datos de prueba y respalda la BD.

"""

import sqlite3

from Datos.Arbol import Arbol
from Datos.ArbolFaltante import ArbolFaltante
from Datos.Bloque import Bloque
from Datos.Clon import Clon
from Datos.Ensayo import Ensayo
from Datos.Imagen import Imagen
from Datos.Parcela import Parcela
from Datos.Repeticion import Repeticion
from Datos.SurcoDetectado import SurcoDetectado
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
        ensayos = cls.crear_objetos_prueba(Ensayo, 0, 1)
        repeticiones = cls.crear_objetos_prueba(Repeticion, 0, 2, False)
        bloques = cls.crear_objetos_prueba(Bloque, 0, 3, False)
        clones = cls.crear_objetos_prueba(Clon, 0, 4)
        parcelas = cls.crear_objetos_prueba(Parcela, 0, 5, False)
        arboles = cls.crear_objetos_prueba(Arbol, 0, 6, False)
        imagenes = cls.crear_objetos_prueba(Imagen, 0, 7, False)
        arboles_faltantes = cls.crear_objetos_prueba(ArbolFaltante, 0, 8, False)
        surcos_detectados = cls.crear_objetos_prueba(SurcoDetectado, 0, 9, False)
        def f(padres, hijos, guardar):
            for p in padres:
                print(p)
                for h in hijos:
                    print(h)
                    setattr(h, p.foranea(), p.clave)
                    if guardar:
                        h.guardar(cls.db)
        f(ensayos, repeticiones, True)
        f(repeticiones, bloques, True)
        f(repeticiones, imagenes, True)
        f(clones, parcelas, False)
        f(bloques, parcelas, True)
        f(parcelas, arboles, True)
        f(arboles, arboles_faltantes, False)
        f(imagenes, arboles_faltantes, True)
        f(imagenes, surcos_detectados, True)

    @classmethod
    def crear_objetos_prueba(cls, estatico, a, b, guardar=True):
        """..."""
        objetos_creados = []
        for r in range(a, b):
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

############################################################################

log.init(ControladorDatos) # Inicializa el Logger para que guarde correctamente
