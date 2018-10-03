"""

********************************************************************************
                            Controlador de Datos
********************************************************************************

Se encarga de de crear las tablas necesarias para los objetos de tipo Base;
crea y lista objetos de tipo Base, vuelca datos de prueba y respalda la BD.

"""

import sqlite3

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

from shapely.geometry import LineString, Polygon, Point

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
    def analisis_a_objetos(cls, imagen, grafo, xy2, xy3, parcelas, q=None):
        """..."""
        def parcelaPertenece(arbol,c, parcels):
            for p in parcels:
                if Point(tuple(c)).within(Polygon(p.getPoligono())):
                    arbol.id_parcelas = p.parcelaDB.clave
        def areaCopaMetros(distanciaMediaMetros, distanciaMediaPixeles, areaCopaPixeles):
            """Retorna el area de la copa de un arbol, expresada en metros cuadrados"""
            try:
                pixelesPorCadaMetro = float(distanciaMediaPixeles)/float(distanciaMediaMetros)
                pixelesPorCadaMetroCuadrado = pixelesPorCadaMetro**2
                return float(areaCopaPixeles)/float(pixelesPorCadaMetroCuadrado)
            except Exception as e:
                print(e)
                return 0
        repeticion = cls.buscar_objetos('Repeticion', {'clave' : imagen.id_repeticiones})[0]
        matrizinicial = [ [ None for i in range(int(repeticion.nroFilas)) ] for j in range(int(repeticion.nroColumnas)) ]
        bloques = cls.buscar_objetos('Bloque', {'id_repeticiones' : imagen.id_repeticiones})
        parcelas_db = []
        for bl in bloques:
            parcelas_db += cls.buscar_objetos('Parcela', {'id_bloques' : bl.clave})
        for i,x in enumerate(parcelas_db):
            nroBloque = cls.buscar_objetos('Bloque', {'clave' : x.id_bloques})[0]
            matrizinicial[int(x.columna)][int(x.fila)] = x
        pos = 0
        print("printear Matriz")
        for fila in matrizinicial:
            for columna in fila:
                if type(fila) is Parcela:
                    print("Fila es igual", fila)
                    parcelas[pos].setParcelaDB(fila)
                    pos+=1
                else:
                    print("Fila no es igual None")
        xy1 = int(imagen.largo/2), int(imagen.ancho/2)
        coord1 = imagen.latitud, imagen.longitud
        coord2 = imagen.latitudCono1, imagen.longitudCono1
        coord3 = imagen.latitudCono2, imagen.longitudCono2
        # Este objeto permite obtener cualquier coordenada de un punto:
        g = GE.from_tiepoints([xy1, xy2, xy3], [coord1, coord2, coord3])
        total = len(grafo.subgraphs)
        contador = 0
        for s in grafo.subgraphs:
            contador += 1
            surcos_detectado = SurcoDetectado()
            surcos_detectado.id_imagenes = imagen.clave
            surcos_detectado.distanciaMedia = -1 # PREGUNTAR COMO OBTENER
            surcos_detectado.anguloMedio = -1 # PREGUNTAR COMO OBTENER
            surcos_detectado.guardar(cls.db)
            arboles_total = len(grafo.subgraphs[s].nodes())
            contador_arboles = 0
            for n in grafo.subgraphs[s].nodes():
                contador_arboles += 1
                if q != None:
                    q.put("Surco " + str(contador) + " de " + str(total) + " | Árbol " + str(contador_arboles) + " de " + str(arboles_total))
                c = grafo.node_props.centroids[n]
                arbol = Arbol()
                arbol.id_repeticiones = imagen.id_repeticiones
                arbol.id_surcos_detectados = surcos_detectado.clave
                arbol.latitud, arbol.longitud = g.transform(c)[0]
                repeticion = cls.buscar_objetos('Repeticion', {'clave' : imagen.id_repeticiones})[0]
                ensayo = cls.buscar_objetos('Ensayo', {'clave' : repeticion.id_ensayos})[0]
                dMMetros = ensayo.espaciamientoY
                dMPixeles = grafo.subgraph_props.mean_dist[s]
                aCPixeles = int(grafo.node_props.areas[n])
                arbol.areaCopa = areaCopaMetros(dMMetros, dMPixeles, aCPixeles)
                arbol.primero = 0 # PREGUNTAR COMO OBTENER
                parcelaPertenece(arbol, c, parcels)
                arbol.guardar(cls.db)
        if q != None:
            q.put("Listo")

    ############################################################################

    @classmethod
    def exportar_informe_csv(cls, clave=None):
        """..."""
        csv.informe(cls.db, cls.csv, clave)

    @classmethod
    def exportar_informe_kml(cls, clave=None):
        """..."""
        kml.informe(cls.db, cls.kml, clave)

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

    @classmethod
    def volcar_datos_prueba(cls, iteraciones):
        """..."""
        for iteracion in range(0, iteraciones):
            log.debug('Volcando datos de prueba iteracion={}'.format(iteracion))
            ensayo = Ensayo.aleatorio().guardar(cls.db)
            repeticiones = cls.crear_objetos_prueba(Repeticion, ensayo.nroRepeticiones, False)
            cls.relacionar_uno_muchos(ensayo, 'Repeticion', True, repeticiones)
            for r in repeticiones:
                imagenes = cls.crear_objetos_prueba(Imagen, 2, False)
                surcos_detectados = cls.crear_objetos_prueba(SurcoDetectado, 1, False)
                arboles = cls.crear_objetos_prueba(Arbol, 10, False)
                arboles_faltantes = cls.crear_objetos_prueba(ArbolFaltante, 1, False)
                cls.relacionar_uno_muchos(r, 'Imagen', True, imagenes)
                cls.relacionar_uno_muchos(r, 'Arbol', False, arboles)
                cls.relacionar_uno_muchos(imagenes[0], 'SurcoDetectado', True, surcos_detectados)
                cls.relacionar_uno_muchos(imagenes[1], 'ArbolFaltante', False, arboles_faltantes)
                cls.relacionar_uno_muchos(surcos_detectados[0], 'Arbol', True, arboles)
                cls.relacionar_uno_muchos(arboles[0], 'ArbolFaltante', True, arboles_faltantes)

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
