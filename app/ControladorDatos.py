"""

********************************************************************************
                            Controlador de Datos
********************************************************************************

Se encarga de de crear las tablas necesarias para los objetos de tipo Base;
crea y lista objetos de tipo Base, vuelca datos de prueba y respalda la BD.

"""

import sqlite3
import random

from Datos.core.Exportador import Base as Base
from Datos.core.Exportador import CSV as csv
from Datos.core.Exportador import KML as kml
from Datos.core.GeoEspacial import GeoEspacial as GE

from Datos.Arbol import Arbol
from Datos.ArbolFaltante import ArbolFaltante
from Datos.Bloque import Bloque
from Datos.Clon import Clon
from Datos.Ensayo import Ensayo
from Datos.Imagen import Imagen
from Datos.Parcela import Parcela
from Datos.Repeticion import Repeticion
from Datos.SurcoDetectado import SurcoDetectado
from Datos.SurcoDetectadoParcela import SurcoDetectadoParcela

from Utilidades import Logger as log

class ControladorDatos(object):

    db = 'Datos/store/treepy.db' # Donde se guarda la BD
    sql = 'Datos/store/treepy.sql' # Donde se exporta la BD
    csv = 'Datos/store/out/csv' # Donde se exportan los CSV
    kml = 'Datos/store/out/kml' # Donde se exportan los KML

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
        'SurcoDetectadoParcela' : SurcoDetectadoParcela,
    }

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
    def ultimos_modificados(cls, tipo, limite=9):
        """..."""
        return cls.controlados[tipo].modificados(cls.db, limite)

    @classmethod
    def obtener_relaciones_de(cls, uno, muchos, guardar=True, filtro=None, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, guardar, None, filtro, fk)

    @classmethod
    def relacionar_uno_muchos(cls, uno, muchos, guardar=True, lista=None, fk=None):
        """..."""
        return uno.lista(cls.db, muchos, guardar, lista, None, fk)

    @classmethod
    def relacionar_muchos_muchos(cls, muchos_x, muchos_y):
        """..."""
        n1 = muchos_x[0].__class__.__name__
        n2 = muchos_y[0].__class__.__name__
        k = n1 + n2 if n1 + n2 in cls.controlados else n2 + n1
        pivot = cls.controlados[k]
        for x in muchos_x:
            for y in muchos_y:
                p = pivot()
                setattr(p, x.foranea(), x.clave)
                setattr(p, y.foranea(), y.clave)
                p.guardar(cls.db, False)

    ############################################################################

    @classmethod
    def analisis_a_objetos(cls, imagen, grafo, xy2, xy3):
        xy1 = int(imagen.largo/2), int(imagen.ancho/2)
        coord1 = imagen.latitud, imagen.longitud
        coord2 = imagen.latitudCono1, imagen.longitudCono1
        coord3 = imagen.latitudCono2, imagen.longitudCono2
        g = GE.from_tiepoints([xy1, xy2, xy3], [coord1, coord2, coord3])
        for s in grafo.subgraphs:
            surcos_detectado = SurcoDetectado()
            surcos_detectado.id_imagenes = imagen.clave
            surcos_detectado.distanciaMedia = -1 # PREGUNTAR COMO OBTENER
            surcos_detectado.anguloMedio = -1 # PREGUNTAR COMO OBTENER
            surcos_detectado.guardar(cls.db)
            for n in grafo.subgraphs[s].nodes():
                c = grafo.node_props.centroids[n]
                arbol = Arbol()
                arbol.id_repeticiones = imagen.id_repeticiones
                arbol.id_surcos_detectados = surcos_detectado.clave
                arbol.latitud, arbol.longitud = g.transform(c)[0]
                arbol.areaCopa = grafo.node_props.areas[n]
                arbol.guardar(cls.db)

    ############################################################################

    @classmethod
    def exportar_informe_csv(cls):
        """..."""
        csv.informe(cls.db, cls.csv)

    @classmethod
    def exportar_informe_kml(cls):
        """..."""
        kml.informe(cls.db, cls.kml)

    ############################################################################

    @classmethod
    def crear_estructura(cls):
        """..."""
        log.debug('Creando estructura')
        q = """CREATE TABLE IF NOT EXISTS objetos (id INTEGER NOT NULL,
        tipo TEXT NOT NULL, creacion TEXT NOT NULL, modificacion TEXT NOT NULL, 
        eliminado INTEGER NOT NULL, PRIMARY KEY(id, tipo))"""
        Base.consultar(cls.db, q) # Tabla para registrar estado de objetos
        q = """CREATE TABLE IF NOT EXISTS historial (id INTEGER NOT NULL,
        tabla TEXT NOT NULL, campo TEXT NOT NULL, 
        anterior TEXT, posterior TEXT, cuando TEXT NOT NULL)"""
        Base.consultar(cls.db, q) # Tabla para guardar historial de cambios
        for nombre, clase in cls.controlados.items():
            print(nombre)
            clase.crear_tabla(cls.db)

    ############################################################################

    # @classmethod
    # def volcar_datos_prueba(cls):
    #     """..."""
    #     log.debug('Volcando datos de prueba')
    #     def f(padres, hijos, guardar):
    #         r = random.choice(padres)
    #         n = hijos[0].__class__.__name__
    #         cls.relacionar_uno_muchos(r, n, guardar, hijos)
    #     def g():
    #         return random.randint(1, 32)
    #     arboles = cls.crear_objetos_prueba(Arbol, g(), False)
    #     arboles_faltantes = cls.crear_objetos_prueba(ArbolFaltante, g(), False)
    #     bloques = cls.crear_objetos_prueba(Bloque, g(), False)
    #     clones = cls.crear_objetos_prueba(Clon, g())
    #     ensayos = cls.crear_objetos_prueba(Ensayo, g())
    #     imagenes = cls.crear_objetos_prueba(Imagen, g(), False)
    #     parcelas = cls.crear_objetos_prueba(Parcela, g(), False)
    #     repeticiones = cls.crear_objetos_prueba(Repeticion, g(), False)
    #     surcos_detectados = cls.crear_objetos_prueba(SurcoDetectado, g(), False)
    #     f(ensayos, repeticiones, True)
    #     f(repeticiones, bloques, True)
    #     f(repeticiones, imagenes, True)
    #     f(repeticiones, arboles, True)
    #     f(clones, parcelas, False)
    #     f(bloques, parcelas, True)
    #     f(parcelas, arboles, True)
    #     f(arboles, arboles_faltantes, False)
    #     f(imagenes, arboles_faltantes, True)
    #     f(imagenes, surcos_detectados, True)
    #     # cls.relacionar_muchos_muchos(surcos_detectados, parcelas) # Opcion 1
    #     cls.relacionar_muchos_muchos(parcelas, surcos_detectados) # Opcion 2

    @classmethod
    def volcar_datos_prueba(cls):
        """..."""
        log.debug('Volcando datos de prueba')
        arboles = cls.crear_objetos_prueba(Arbol, 9, False)
        arboles_faltantes = cls.crear_objetos_prueba(ArbolFaltante, 3, False)
        bloques = cls.crear_objetos_prueba(Bloque, 6, False)
        ensayos = cls.crear_objetos_prueba(Ensayo, 6)
        imagenes = cls.crear_objetos_prueba(Imagen, 3, False)
        parcelas = cls.crear_objetos_prueba(Parcela, 3, False)
        repeticiones = cls.crear_objetos_prueba(Repeticion, 3, False)
        surcos_detectados = cls.crear_objetos_prueba(SurcoDetectado, 6, False)
        def f_3(bloque):
            for p in parcelas:
                cls.relacionar_uno_muchos(p, 'Arbol', True, arboles)
            cls.relacionar_uno_muchos(bloque, 'Parcela', False, parcelas)
            cls.relacionar_uno_muchos(Clon.aleatorio(), 'Parcela', True, parcelas)
        def f_2(repeticion):
            for b in bloques:
                f_3(b)
            cls.relacionar_uno_muchos(repeticion, 'Bloque', True, bloques)
            cls.relacionar_uno_muchos(repeticion, 'Arbol', True, arboles)
        def f_1(ensayo):
            for r in repeticiones:
                f_2(r)
            cls.relacionar_uno_muchos(ensayo, 'Repeticion', True, repeticiones)
        for e in ensayos:
            f_1(e)     

    @classmethod
    def crear_objetos_prueba(cls, estatico, n, guardar=True):
        """..."""
        objetos_creados = []
        for r in range(0, n):
            if guardar:
                o = estatico.aleatorio().guardar(cls.db)
            else:
                o = estatico.aleatorio()
            objetos_creados.append(o)
            print('{} : {}'.format(r, o))
        return objetos_creados

    ############################################################################

    @classmethod
    def respaldar_datos(cls):
        """..."""
        log.debug('Respaldando datos')
        conexion = sqlite3.connect(cls.db)
        with open(cls.sql, 'w') as a:
            for linea in conexion.iterdump():
                print(linea)
                a.write('%s\n' % linea)

################################################################################

log.init(ControladorDatos) # Inicializa el Logger para que guarde correctamente
