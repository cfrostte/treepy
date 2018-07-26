"""..."""

import sqlite3
from Datos.Ensayo import Ensayo

class ControladorDatos(object):

    """...""" # DEBERIA SER UN SINGLETON?

    db = 'Datos/store/treepy.db'
    sql = 'Datos/store/treepy.sql'

    @classmethod
    def crear_tablas(cls):
        """..."""
        Ensayo.crear_tabla(cls.db)

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        cls.crear_objetos(Ensayo, 1, 23)

    @classmethod
    def respaldar_datos(cls):
        """..."""
        conexion = sqlite3.connect(cls.db)
        with open(cls.sql, 'w') as a:
            for linea in conexion.iterdump():
                a.write('%s\n' % linea)

    @classmethod
    def crear_objetos(cls, muestra, a, b):
        """..."""
        print('\n------------------------------')
        print('\tCreando {}'.format(muestra.tabla))
        print('------------------------------\n')
        for r in range(a, b):
            o = muestra.aleatorio().guardar(cls.db)
            print('{} : {}'.format(r, o))
