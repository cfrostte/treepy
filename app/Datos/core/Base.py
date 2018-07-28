"""

-------------------------------------------------------------------
Clase de la cual deriva todo objeto almacenable en la base de datos
-------------------------------------------------------------------
Todas las clases basados en esta, pueden especificar:
    +   Diccionario con los posibles objetos relacionados a la misma
    +   Tabla en la cual se mapearan los objetos a almacenar en la BD
    +   La clave con la cual se identifica al objeto en la BD
    +   Constructor con clave opcional que derive al constructor Base
    +   Todas las funciones no implementadas en esta clase

La documentacion de los modulos que tienen a las clases derivadas de Base,
deben estar al principio del archivo y explicar su proposito como entidad;
cualquier otra documentacion debe figurar unicamente en este modulo.

Los miembros aqui listados se agrupan por tematica y cada grupo se ordena:
    1)  Primero los diccionarios y luego los atributos privados;
    2)  Luego los constructres y las funciones estaticas (primero las pass)
    3)  Todas las funciones de clase (las pass / por implementar van primero)
    4)  Por ultimo, las funciones de instancia de objetos, entre otras.

"""

import sqlite3

class Base(object):

    # Tipos de objetos con los cuales se relaciona este:
    _relacionados = {}

    # Miembros que comiencen con '_' o '__' no se persisten:
    _tabla = None # Nombre de la _tabla en donde se persiste

    # El resto de los atributos deben estar en la _tabla:
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
    def sentencia(cls):
        """Retorna la sentencia de creacion de la tabla del objeto"""
        pass

    @classmethod
    def foranea(cls):
        """Retorna el nombre por defecto de una FK de este objeto"""
        return 'id_' + cls._tabla

    @classmethod
    def consultar(cls, donde, consulta, valores=None, many=False, close=True):
        """Ejecuta cualquier tipo de consulta"""
        print('consulta = "{}", valores = {}'.format(consulta, valores))
        conexion = sqlite3.connect(donde)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        if valores and valores != (None, ):
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
        """Crea la _tabla en donde se almacenan los datos"""
        cls.consultar(donde, cls.sentencia())

    @classmethod
    def id_disponible(cls, donde):
        """Retorna el ID disponible para la _tabla de la clase"""
        consulta = """SELECT MAX(clave) AS max_id FROM {}"""
        filas = cls.consultar(donde, consulta.format(cls._tabla))
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
            campo = fk if fk else padre.foranea()
            valor = padre.clave
            condicion = 'WHERE {} = ?'.format(campo)
        else:
            campo = None
            valor = None
            condicion = ''
        consulta = """SELECT * FROM {} {} {}"""
        consulta = consulta.format(cls._tabla, condicion, limite)
        filas = cls.consultar(donde, consulta, (valor, ))
        lista = []
        for f in filas:
            lista.append(cls.desde_fila(f))
        return lista

    def obtener(self, donde):
        """Retorna el registro con los datos del objeto"""
        consulta = """SELECT * FROM {} WHERE clave = ?""".format(self._tabla)
        clave = int(0 if self.clave is None else self.clave)
        cursor, conexion = self.consultar(donde, consulta, (clave, ), False, False)
        fila = cursor.fetchone()
        cursor.close()
        conexion.close()
        return fila

    def hijos(self, donde, tipo, lista=None):
        """
        Retorna los hijos del objeto (o antes de eso los asigna):
        -   Si se llama a .hijos(donde, tipo) solo retorna la lista,
        -   Si se llama a .hijos(donde, tipo, lista) entonces:
            1)  Primero se asigna la lista y luego se retornan todos
                (la lista retornada deberia contener a los asignados)
            2)  Luego se toma el nombre de la fk por defecto del padre,
                que se supone esta presente en la tabla del hijo
                (y la misma apunta a la clave de la tabla del padre)
                para luego asignarle el valor de la 'clave' del padre
        """
        if lista:
            for l in lista:
                # ~ l.fk = self.clave (pasos 1 y 2):
                setattr(l, self.foranea(), self.clave)
                l.guardar(donde)
        return self._relacionados[tipo].todos(donde, None, self)

    def guardar(self, donde):
        """Crea o modifica los datos del objeto"""
        valores = ()
        for a in self.atributos():
            valores += (getattr(self, a), )
        if self.obtener(donde): # Existe, entonces modificar:
            atributos = ' = ?, '.join(self.atributos()) + ' = ?'
            consulta = """UPDATE {} SET {} WHERE clave = ?"""
            consulta = consulta.format(self._tabla, atributos)
            self.consultar(donde, consulta, valores + (self.clave, ))
        else: # No existe, entonces crear:
            atributos = ', '.join(self.atributos(True))
            clave = self.id_disponible(donde)
            def f(x):
                return '?'
            signos = ', '.join(map(f, (clave, ) + valores))
            consulta = """INSERT INTO {} ({}) VALUES ({})"""
            consulta = consulta.format(self._tabla, atributos, signos)
            self.consultar(donde, consulta, (clave, ) + valores)
            self.clave = clave
        return self.obtener(donde)

    def atributos(self, con_clave=False):
        """Retorna la lista de atributos del objeto, que no comiencen ni con '__' (privados) ni con '_' (reservados) ni sean metodos"""
        if con_clave:
            return [a for a in dir(self) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(self, a))]
        return [a for a in dir(self) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(self, a)) and not a == 'clave']
