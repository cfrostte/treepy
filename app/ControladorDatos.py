"""..."""

import sqlite3
from Datos.Ensayo import Ensayo
from Datos.Repeticion import Repeticion

class ControladorDatos(object):

    db = 'Datos/store/treepy.db'
    sql = 'Datos/store/treepy.sql'

    @classmethod
    def crear_tablas(cls):
        """..."""
        cls.log_tarea('Creando tablas')
        Ensayo.crear_tabla(cls.db)
        Repeticion.crear_tabla(cls.db)

    @classmethod
    def crear_objetos(cls, estatico, a, b):
        """..."""
        cls.log_tarea('Creando', estatico)
        objetos_creados = []
        for r in range(a, b):
            o = estatico.aleatorio().guardar(cls.db)
            objetos_creados.append(o)
            print('{} : {}'.format(r, o))
        return objetos_creados

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        ensayos = cls.crear_objetos(Ensayo, 0, 9)
        for e in ensayos:
            e.repeticiones(cls.db, cls.crear_objetos(Repeticion, 0, 3))

    @classmethod
    def listar_objetos(cls, tipo, limite=None):
        """..."""
        tipos = {
            'Ensayo': Ensayo,
            'Repeticion': Repeticion,
        }
        cls.log_tarea('Listando', tipos[tipo])
        for objeto in tipos[tipo].todos(cls.db, limite):
            print(objeto)
        if limite:
            print('\nlimite={}'.format(limite))

    @classmethod
    def respaldar_datos(cls):
        """..."""
        conexion = sqlite3.connect(cls.db)
        with open(cls.sql, 'w') as a:
            for linea in conexion.iterdump():
                a.write('%s\n' % linea)

    @staticmethod
    def log_tarea(accion, clase=None):
        """..."""
        print('\n-----------------------------------------------------')
        print('\t\t{} {}'.format(accion, clase._tabla if clase else ''))
        print('-----------------------------------------------------\n')
