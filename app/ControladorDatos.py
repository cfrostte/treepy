"""

********************************************************************************
                            Controlador de Datos
********************************************************************************

Se encarga de de crear las tablas necesarias para los objetos de tipo Base;
crea y lista objetos de tipo Base, vuelca datos de prueba y respalda la BD.

"""

import sqlite3
from Datos.Ensayo import Ensayo
from Datos.Repeticion import Repeticion

class ControladorDatos(object):

    db = 'Datos/store/treepy.db' # Donde se guarda la BD
    sql = 'Datos/store/treepy.sql' # Donde se exporta la BD

    # Tipos de objeto manejados:
    controlados = {
        'Ensayo' : Ensayo,
        'Repeticion' : Repeticion,
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
    def ver_relacionados_entre(cls, uno, muchos, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, None, fk)

    @classmethod
    def relacionar_uno_muchos(cls, objeto, lista, fk=None):
        """..."""
        return cls.controlados[objeto].lista(cls.db, lista, None, fk)

    ############################################################################

    @classmethod
    def crear_estructura(cls):
        """..."""
        cls.log_tarea('Creando estructura')
        Ensayo.crear_tabla(cls.db)
        Repeticion.crear_tabla(cls.db)

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
    def crear_objetos_prueba(cls, estatico, a, b):
        """..."""
        cls.log_tarea('Creando', estatico, 'de prueba')
        objetos_creados = []
        for r in range(a, b):
            o = estatico.aleatorio().guardar(cls.db)
            objetos_creados.append(o)
            print('{} : {}'.format(r, o))
        return objetos_creados

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        cls.log_tarea('Volcando datos de prueba')
        ensayos = cls.crear_objetos_prueba(Ensayo, 0, 9)
        for e in ensayos:
            e.lista(cls.db, 'Repeticion', cls.crear_objetos_prueba(Repeticion, 0, 3))
