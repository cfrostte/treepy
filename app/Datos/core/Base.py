"""..."""

import sqlite3

class Base(object):

    tabla = None # Nombre de la tabla en donde se persiste
    consulta = None # Consulta con la cual se crea la tabla
    clave = None # Es el 'id' (la palabra 'id' esta reservada)

    def __init__(self, clave):
        self.clave = clave

    @staticmethod
    def aleatorio():
        """Retorna un objeto con datos aleatorios"""
        pass

    @classmethod
    def consultar(cls, donde, consulta, valores=None, many=False, close=True):
        """Ejecuta cualquier tipo de consulta"""
        # print(consulta, valores)
        conexion = sqlite3.connect(donde)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        if valores:
            if many:
                cursor.executemany(consulta, valores)
            else:
                cursor.execute(consulta, valores)
        else:
            cursor.execute(consulta)
        conexion.commit()
        if close:
            filas = cursor.fetchall()
            cursor.close()
            conexion.close()
            return filas # Cursor y Conexion cerradas (utilizar filas)
        return cursor, conexion # Cursor y Conexion abiertos (cerrarlos)

    @classmethod
    def crear_tabla(cls, donde):
        """Crea la tabla en donde se almacenan los datos"""
        cls.consultar(donde, cls.consulta.format(cls.tabla))

    @classmethod
    def id_disponible(cls, donde, tabla):
        """Retorna el ID disponible para la tabla"""
        consulta = """SELECT MAX(clave) AS max_id FROM {}"""
        filas = cls.consultar(donde, consulta.format(tabla))
        for f in filas:
            max_id = f['max_id']
            return int(0 if max_id is None else max_id) + 1

    def obtener(self, donde):
        """Retorna el registro con los datos del objeto"""
        consulta = """SELECT * FROM {} WHERE clave = ?""".format(self.tabla)
        clave = int(0 if self.clave is None else self.clave)
        cursor, conexion = self.consultar(donde, consulta, (clave, ), False, False)
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def guardar(self, donde, valores):
        """Crea o modifica los datos del objeto"""
        if self.obtener(donde): # Existe, entonces modificar:
            atributos = ' = ?, '.join(self.atributos()) + ' = ?'
            consulta = """UPDATE {} SET {} WHERE clave = ?""".format(self.tabla, atributos)
            self.consultar(donde, consulta, valores + (self.clave, ))
        else: # No existe, entonces crear:
            atributos = ', '.join(self.atributos(True))
            clave = self.id_disponible(donde, self.tabla)
            def f(x):
                return '?'
            signos = ', '.join(map(f, (clave, ) + valores))
            consulta = """INSERT INTO {} ({}) VALUES ({})""".format(self.tabla, atributos, signos)
            self.consultar(donde, consulta, (clave, ) + valores)
            self.clave = clave
        return self.obtener(donde)

    def atributos(self, con_clave=False):
        """Retorna la lista de atributos del objeto (solo miembros que no son sus metodos) a excepcion de la tabla y de la clave"""
        if con_clave:
            return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) and not a == 'tabla' and not a == 'consulta']
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) and not a == 'tabla' and not a == 'consulta' and not a == 'clave']
