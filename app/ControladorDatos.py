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

    @staticmethod
    def log_tarea(accion, clase=None, extra=None):
        """..."""
        _tabla = clase._tabla if clase else ''
        extra = extra if extra else ''
        print('\n-------------------------------------------------------------')
        print('\t\t\t{} {} {}'.format(accion, _tabla, extra))
        print('-------------------------------------------------------------\n')

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
    def ver_relacionados_de(cls, uno, muchos, filtro=None, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, None, filtro, fk)

    @classmethod
    def relacionar_uno_muchos(cls, uno, muchos, lista, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, lista, None, fk)

    ############################################################################

    @classmethod
    def crear_estructura(cls):
        """..."""
        cls.log_tarea('Creando estructura')
        for nombre, clase in cls.controlados.items():
            print('\t--\tCreando {} para {}'.format(clase._tabla, nombre))
            clase.crear_tabla(cls.db)

    @classmethod
    def respaldar_datos(cls):
        """..."""
        cls.log_tarea('Respaldando datos')
        conexion = sqlite3.connect(cls.db)
        with open(cls.sql, 'w') as a:
            for linea in conexion.iterdump():
                print(linea)
                a.write('%s\n' % linea)

    ############################################################################

    @classmethod
    def crear_objetos_prueba(cls, estatico, a, b, guardar=True):
        """..."""
        cls.log_tarea('Creando', estatico, 'de prueba')
        objetos_creados = []
        for r in range(a, b):
            if guardar:
                o = estatico.aleatorio().guardar(cls.db)
            else:
                o = estatico.aleatorio()
            objetos_creados.append(o)
            print('{} : {}'.format(r, o))
        return objetos_creados

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        cls.log_tarea('Volcando datos de prueba')
        def f(lista_padre, hijo, a, b):
            lista_hijos = None
            for l in lista_padre:
                print(l)
                lista_hijos = cls.crear_objetos_prueba(hijo, a, b, False)
                cls.relacionar_uno_muchos(l, hijo.__name__, lista_hijos)
            return lista_hijos
        ensayos = cls.crear_objetos_prueba(Ensayo, 0, 1)
        repeticiones = f(ensayos, Repeticion, 0, 3)
        bloques = f(repeticiones, Bloque, 0, 3)
