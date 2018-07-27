"""Clase de la cual deriva todo objeto almacenable en la BD"""

import sqlite3

class Base(object):

    # Atributos que comiencen con '_' no se persisten:
    _tabla = None # Nombre de la _tabla en donde se persiste
    _consulta = None # Consulta con la cual se crea la _tabla

    clave = None # Es el 'id' (la palabra 'id' esta reservada)

    def __init__(self, clave):
        self.clave = clave

    def __str__(self):
        texto = '<{}>'.format(self.__class__.__name__)
        tuplas = ()
        for atributo in self.atributos(True):
            texto += ' {}=%s,'.format(atributo)
            tuplas += (getattr(self, atributo), )
        return texto % tuplas

    @staticmethod
    def desde_fila(f):
        """Instancia un objeto a partir de una fila 'f'"""
        pass

    @staticmethod
    def aleatorio():
        """Retorna un objeto con datos aleatorios"""
        pass

    @classmethod
    def consultar(cls, donde, _consulta, valores=None, many=False, close=True):
        """Ejecuta cualquier tipo de _consulta"""
        print('q={}, v={}'.format(_consulta, valores))
        conexion = sqlite3.connect(donde)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        if valores and valores != (None, ):
            if many:
                cursor.executemany(_consulta, valores)
            else:
                cursor.execute(_consulta, valores)
        else:
            cursor.execute(_consulta)
        conexion.commit()
        if close:
            filas = cursor.fetchall()
            cursor.close()
            conexion.close()
            return filas # Cursor y Conexion cerradas (utilizar filas)
        return cursor, conexion # Cursor y Conexion abiertos (cerrarlos)

    @classmethod
    def crear_tabla(cls, donde):
        """Crea la _tabla en donde se almacenan los datos"""
        cls.consultar(donde, cls._consulta.format(cls._tabla))

    @classmethod
    def id_disponible(cls, donde, _tabla):
        """Retorna el ID disponible para la _tabla"""
        _consulta = """SELECT MAX(clave) AS max_id FROM {}"""
        filas = cls.consultar(donde, _consulta.format(_tabla))
        for f in filas:
            max_id = f['max_id']
            return int(0 if max_id is None else max_id) + 1

    @classmethod
    def todos(cls, donde, limite=None, padre=None, fk=None):
        """
        Retorna todos los registros de la tabla del objeto;
        tambien puede filtrarse por valor de un campo:
            -   El campo puede ser una clave foranea 'fk' custom,
                pero igual debe pasarse un padre para usarla.
            -   Por defecto, la fk se llama id_<tabla del padre>
        """
        limite = 'LIMIT {}'.format(limite) if limite else ''
        if padre:
            campo = fk if fk else 'id_' + padre._tabla
            valor = padre.clave
            condicion = 'WHERE {} = ?'.format(campo)
        else:
            campo = None
            valor = None
            condicion = ''
        _consulta = """SELECT * FROM {} {} {}"""
        _consulta = _consulta.format(cls._tabla, condicion, limite)
        filas = cls.consultar(donde, _consulta, (valor, ))
        lista = []
        for f in filas:
            lista.append(cls.desde_fila(f))
        return lista

    def obtener(self, donde):
        """Retorna el registro con los datos del objeto"""
        _consulta = """SELECT * FROM {} WHERE clave = ?""".format(self._tabla)
        clave = int(0 if self.clave is None else self.clave)
        cursor, conexion = self.consultar(donde, _consulta, (clave, ), False, False)
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def guardar(self, donde, valores):
        """Crea o modifica los datos del objeto"""
        if self.obtener(donde): # Existe, entonces modificar:
            atributos = ' = ?, '.join(self.atributos()) + ' = ?'
            _consulta = """UPDATE {} SET {} WHERE clave = ?""".format(self._tabla, atributos)
            self.consultar(donde, _consulta, valores + (self.clave, ))
        else: # No existe, entonces crear:
            atributos = ', '.join(self.atributos(True))
            clave = self.id_disponible(donde, self._tabla)
            def f(x):
                return '?'
            signos = ', '.join(map(f, (clave, ) + valores))
            _consulta = """INSERT INTO {} ({}) VALUES ({})""".format(self._tabla, atributos, signos)
            self.consultar(donde, _consulta, (clave, ) + valores)
            self.clave = clave
        return self.obtener(donde)

    def atributos(self, con_clave=False):
        """Retorna la lista de atributos del objeto, que no comiencen ni con '__' (privados) ni con '_' (reservados) ni sean metodos"""
        if con_clave:
            return [a for a in dir(self) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(self, a))]
        return [a for a in dir(self) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(self, a)) and not a == 'clave']
