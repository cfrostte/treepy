"""

-------------------------------------------------------------------
Clase de la cual deriva todo objeto almacenable en la base de datos
-------------------------------------------------------------------
Todas las clases basadas en esta, pueden o deben especificar:
    +   Diccionario con los posibles objetos relacionados a la misma
    +   Tabla en la cual se mapearan los objetos a almacenar en la BD
    +   La clave con la cual se identifica al objeto en la BD ('clave')
    +   Constructor con clave opcional que derive al constructor Base
    +   Todas las funciones no implementadas en esta clase

La documentacion de los modulos que tienen a las clases derivadas de Base,
deben estar al principio del archivo y explicar su proposito como entidad;
cualquier otra documentacion debe figurar unicamente en este modulo.

"""

import sqlite3

class Base(object):

    # Tipos de objetos con los cuales se relaciona este:
    _relacionados = {}

    # Miembros que comiencen con '_' o '__' no se persisten:
    _tabla = None # Nombre de la _tabla en donde se persiste

    # El resto de los atributos deben estar en la _tabla:
    clave = None # Es el 'id' (la palabra 'id' esta reservada)

    ############################################################################

    def __init__(self, clave=None):
        self.clave = clave

    def __str__(self):
        texto = '<{}>'.format(self.__class__.__name__)
        tuplas = ()
        for atributo in self.atributos(True):
            texto += ' {}=%s,'.format(atributo)
            tuplas += (getattr(self, atributo), )
        return texto % tuplas

    ############################################################################

    @staticmethod
    def aleatorio():
        """Retorna un objeto con datos aleatorios"""
        pass

    ############################################################################

    @classmethod
    def sentencia(cls):
        """Retorna la sentencia de creacion de la _tabla"""
        pass

    @classmethod
    def foranea(cls):
        """Retorna el nombre estandar de la clave foranea que apunta a la _tabla"""
        return 'id_' + cls._tabla

    @classmethod
    def crear_tabla(cls, donde):
        """Crea la _tabla en donde se almacenan los datos"""
        cls.consultar(donde, cls.sentencia())

    @classmethod
    def desde_fila(cls, fila):
        """Instancia un objeto a partir de una fila"""
        objeto = cls.__new__(cls)
        for a in objeto.atributos(True):
            setattr(objeto, a, fila[a])
        return objeto

    @classmethod
    def obtener(cls, donde, filtro):
        """Retorna el registro con los datos del objeto"""
        resultado = cls.buscar(donde=donde, filtro=filtro, limite=1)
        if resultado:
            return resultado[0]
        return None

    @classmethod
    def id_disponible(cls, donde):
        """Retorna el ID disponible para la _tabla"""
        consulta = """SELECT MAX(clave) AS max_id FROM {}"""
        filas = cls.consultar(donde, consulta.format(cls._tabla))
        for f in filas:
            max_id = f['max_id']
            return int(0 if max_id is None else max_id) + 1

    @classmethod
    def consultar(cls, donde, consulta, valores=None, many=False, close=True):
        """Ejecuta cualquier tipo de consulta"""
        print('consulta = "{}" | valores = {}'.format(consulta, valores))
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
    def buscar(cls, donde, filtro=None, orden=None, asc=True, limite=None):
        """Retorna todos los registros que coinciden con el filtro"""
        if filtro:
            condiciones = ' = ? AND '.join(list(filtro.keys())) + ' = ?'
            valores = ()
            for v in list(filtro.values()):
                valores += (v, )
        else:
            condiciones = 1
        asc = ' ASC' if asc else ' DESC'
        orden = 'ORDER BY ' + (', '.join(orden)) + asc if orden else ''
        limite = 'LIMIT {}'.format(limite) if limite else ''
        consulta = """SELECT * FROM {} WHERE {} {} {}"""
        consulta = consulta.format(cls._tabla, condiciones, orden, limite)
        filas = cls.consultar(donde, consulta, valores if filtro else None)
        lista = []
        for f in filas:
            lista.append(cls.desde_fila(f))
        return lista

    @classmethod
    def atributos(cls, con_clave=False):
        """Retorna la lista de atributos del objeto, que no comiencen ni con '__' (privados) ni con '_' (reservados) ni sean metodos"""
        if con_clave:
            return [a for a in dir(cls) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(cls, a))]
        return [a for a in dir(cls) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(cls, a)) and not a == 'clave']

    ############################################################################

    def guardar(self, donde, modificable=True):
        """Crea o modifica los datos del objeto y lo retorna (si se guardo)"""
        m = modificable and self.obtener(donde, {'clave' : self.clave})
        if m: # Modificar (se actualizan los campos):
            atributos_sin_clave = self.atributos()
            valores_sin_clave = ()
            for a in atributos_sin_clave:
                valores_sin_clave += (getattr(self, a), )
            atributos = ' = ?, '.join(atributos_sin_clave) + ' = ?'
            consulta = """UPDATE {} SET {} WHERE clave = ?"""
            consulta = consulta.format(self._tabla, atributos)
            self.consultar(donde, consulta, valores_sin_clave + (self.clave, ))
        else: # Crear (se obtiene una nueva clave para el filtro):
            atributos_con_clave = self.atributos(True)
            valores_con_clave = ()
            self.clave = self.id_disponible(donde)
            for a in atributos_con_clave:
                valores_con_clave += (getattr(self, a), )
            atributos = ', '.join(atributos_con_clave)
            def f(x):
                return '?'
            signos = ', '.join(map(f, valores_con_clave))
            consulta = """INSERT INTO {} ({}) VALUES ({})"""
            consulta = consulta.format(self._tabla, atributos, signos)
            self.consultar(donde, consulta, valores_con_clave)
        return self.obtener(donde, {'clave' : self.clave})

    def lista(self, donde, tipo, guardar=True, lista=None, filtro=None, fk=None):
        """
        Retorna la lista de todos los objetos relacionados a este:
        -   Si se llama a .lista(donde, tipo) solo retorna la lista,
        -   Si se llama a .lista(donde, tipo, lista) entonces:
            1)  Primero se asigna la lista y luego se retornan todos
                (la lista retornada deberia contener a los asignados)
            2)  Luego se toma el nombre de la clave foranea 'fk'
                y se le asigna el valor de la clave del objeto apuntado
        """
        fk = fk if fk else self.foranea()
        filtro_fk = {fk : self.clave}
        if filtro:
            filtro_fk = dict(list(filtro_fk.items()) + list(filtro.items()))
        if lista:
            for l in lista:
                setattr(l, fk, self.clave)
                if guardar:
                    l.guardar(donde)
        return self._relacionados[tipo].buscar(donde, filtro_fk)
