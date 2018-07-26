"""..."""

import sqlite3
from Datos.Ensayo import Ensayo

class ControladorDatos(object):

    db = 'Datos/store/treepy.db'
    sql = 'Datos/store/treepy.sql'

    @classmethod
    def crear_tablas(cls):
        """..."""
        Ensayo.crear_tabla(cls.db)

    @classmethod
    def crear_objetos(cls, estatico, a, b):
        """..."""
        print('\n---------------------------------')
        print('\tCreando {}'.format(estatico.tabla))
        print('---------------------------------\n')
        for r in range(a, b):
            o = estatico.aleatorio().guardar(cls.db)
            print('{} : {}'.format(r, o))

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        cls.crear_objetos(Ensayo, 1, 23)
        cls.crear_objetos(Ensayo, 4, 56)
        cls.crear_objetos(Ensayo, 7, 89)

    @classmethod
    def respaldar_datos(cls):
        """..."""
        conexion = sqlite3.connect(cls.db)
        with open(cls.sql, 'w') as a:
            for linea in conexion.iterdump():
                a.write('%s\n' % linea)
