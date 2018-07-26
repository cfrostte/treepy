"""..."""

import sqlite3

class Base(object):

    """..."""

    tabla = None # Nombre de la tabla en donde se persiste
    clave = None # Es el 'id' (pylint pide mas de dos letras)

    def __init__(self, clave):
        self.clave = clave

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
    def id_disponible(cls, donde, tabla):
        """Retorna el ID disponible para la tabla"""
        consulta = """SELECT MAX(id) AS max_id FROM {}"""
        filas = cls.consultar(donde, consulta.format(tabla))
        for f in filas:
            max_id = f['max_id']
            return int(0 if max_id is None else max_id) + 1

    def obtener(self, donde):
        """..."""
        consulta = """SELECT * FROM {} WHERE id = ?""".format(self.tabla)
        clave = int(0 if self.clave is None else self.clave)
        cursor, conexion = self.consultar(donde, consulta, (clave, ), False, False)
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def guardar(self, donde):
        """..."""
        pass

    @staticmethod
    def aleatorio():
        """..."""
        pass
