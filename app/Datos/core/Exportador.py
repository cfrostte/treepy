"""..."""

import csv
import datetime
import os
import simplekml

from .Base import Base

class Exportador(object):

    meses = {
        0 : '',
        1 : 'enero',
        2 : 'febrero',
        3 : 'marzo',
        4 : 'abril',
        5 : 'mayo',
        6 : 'junio',
        7 : 'julio',
        8 : 'agosto',
        9 : 'setiembre',
        10 : 'octubre',
        11 : 'noviembre',
        12 : 'diciembre'
    }

    @staticmethod
    def crear_ruta(r):
        if not os.path.exists(r):
            os.makedirs(r)
            print("'", r, "' creado")

    @staticmethod
    def nuevo_archivo(carpeta, extencion):
        Exportador.crear_ruta(carpeta)
        n = datetime.datetime.now()
        o = "{}/Informe del {} de {} de {} a las {} y {}.{}"
        d = n.day
        m = Exportador.meses[n.month]
        y = n.year
        hh = n.hour
        mm = n.minute
        return o.format(carpeta, d, m, y, hh, mm, extencion)

class CSV(Exportador):
    @staticmethod
    def informe(db, carpeta, clave=None):
        archivo = Exportador.nuevo_archivo(carpeta, 'csv')
        # Escribir en archivo
        with open(archivo, 'w') as a:
            A = 'N° de Ensayo'
            B = 'N° de Repetición'
            C = 'N° de Clon'
            D = 'ID del Árbol'
            E = 'Latitud del Árbol'
            F = 'Longitud del Árbol'
            G = '¿Árbol Faltante?'
            H = 'Área de la Copa del Árbol'
            header = [A, B, C, D, E, F, G, H]
            dw = csv.DictWriter(a, fieldnames=header)
            dw.writeheader() # Escribir el header
            # consulta = """SELECT e.nro AS A, r.nro AS B, 'S/N' AS C, a.clave AS D, a.latitud AS E, a.longitud AS F, 
            # CASE WHEN (SELECT 1 FROM arboles_faltantes WHERE id_arboles = a.clave) THEN 'Si' ELSE 'No' END AS G, 
            # a.areaCopa AS H FROM arboles AS a JOIN repeticiones AS r JOIN ensayos AS e 
            # WHERE r.id_ensayos = e.clave AND a.id_repeticiones = r.clave {}""".format('AND e.clave = ?' if clave else '')
            consulta = """SELECT e.nro AS A, r.nro AS B, 'S/N' AS C, a.clave AS D, a.latitud AS E, a.longitud AS F, 
            CASE WHEN (SELECT 1 FROM arboles_faltantes AS a_f JOIN objetos AS o 
            WHERE a_f.id_arboles = a.clave AND o.tipo = 'ArbolFaltante' AND o.id = a_f.clave AND o.eliminado = 0) 
            THEN 'Si' ELSE 'No' END AS G, a.areaCopa AS H FROM arboles AS a JOIN repeticiones AS r JOIN ensayos AS e 
            JOIN objetos AS o_1 JOIN objetos AS o_2 JOIN objetos AS o_3
            WHERE r.id_ensayos = e.clave AND a.id_repeticiones = r.clave
            AND o_1.tipo = 'Arbol' AND o_1.id = a.clave AND o_1.eliminado = 0
            AND o_2.tipo = 'Repeticion' AND o_2.id = r.clave AND o_2.eliminado = 0
            AND o_3.tipo = 'Ensayo' AND o_3.id = e.clave AND o_3.eliminado = 0 {}""".format('AND e.clave = ?' if clave else '')
            resultado = Base.consultar(db, consulta, (clave, )) if clave else Base.consultar(db, consulta)
            if resultado:
                for r in resultado:
                    fila = {
                        '{}'.format(header[0]) : r['A'],
                        '{}'.format(header[1]) : r['B'],
                        '{}'.format(header[2]) : r['C'],
                        '{}'.format(header[3]) : r['D'],
                        '{}'.format(header[4]) : r['E'],
                        '{}'.format(header[5]) : r['F'],
                        '{}'.format(header[6]) : r['G'],
                        '{}'.format(header[7]) : r['H']
                    }
                    dw.writerow(fila)
        # Debuggear el archivo
        with open(archivo, newline='\n') as a:
            dr = csv.DictReader(a)
            for fila in dr:
                print(fila)

class KML(Exportador):
    @staticmethod
    def informe(db, carpeta, clave=None):
        kml = simplekml.Kml()
        q_ensayos = """SELECT ensayos.* FROM ensayos JOIN objetos
        WHERE clave = id AND tipo = 'Ensayo' AND eliminado = 0 AND EXISTS
        (SELECT 1 FROM repeticiones WHERE id_ensayos = ensayos.clave) {}""".format('AND clave = ?' if clave else '')
        r_ensayos = Base.consultar(db, q_ensayos, (clave, )) if clave else Base.consultar(db, q_ensayos)
        if r_ensayos:
            for e in r_ensayos:
                f_e = kml.newfolder(name='Ensayo nro {}'.format(e['nro']))
                q_repeticiones = """SELECT repeticiones.* FROM repeticiones JOIN objetos
                WHERE clave = id AND tipo = 'Repeticion' AND eliminado = 0 AND EXISTS 
                (SELECT 1 FROM arboles WHERE id_repeticiones = repeticiones.clave) AND id_ensayos = ?"""
                r_repeticiones = Base.consultar(db, q_repeticiones, (e['clave'], ))
                if r_repeticiones:
                    for r in r_repeticiones:
                        f_r = f_e.newfolder(name='Repeticion nro {}'.format(r['nro']))
                        q_imagenes = """SELECT imagenes.* FROM imagenes JOIN objetos
                        WHERE clave = id AND tipo = 'Imagen' AND eliminado = 0 AND id_repeticiones = ?"""
                        r_imagenes = Base.consultar(db, q_imagenes, (r['clave'], ))
                        if r_imagenes:
                            for i in r_imagenes:
                                f_i = f_r.newfolder(name="Imágen {} / etapa '{}'".format(i['clave'], i['etapa']))
                                faltantes = f_i.newfolder(name='Árboles Faltantes')
                                presentes = f_i.newfolder(name='Árboles Presentes')
                                q_arboles_1 = """SELECT arboles.* FROM arboles JOIN surcos_detectados JOIN objetos
                                WHERE arboles.clave = id AND tipo = 'Arbol' AND eliminado = 0 
                                AND id_surcos_detectados = surcos_detectados.clave AND id_repeticiones = ? AND id_imagenes = ?"""
                                q_arboles_2 = """SELECT arboles.* FROM arboles JOIN arboles_faltantes JOIN objetos
                                WHERE arboles.clave = id AND tipo = 'Arbol' AND eliminado = 0 
                                AND id_arboles = arboles.clave AND id_repeticiones = ? AND id_imagenes = ?"""
                                r_arboles_1 = Base.consultar(db, q_arboles_1, (r['clave'], i['clave']))
                                r_arboles_2 = Base.consultar(db, q_arboles_2, (r['clave'], i['clave']))
                                if r_arboles_1:
                                    for a in r_arboles_1:
                                        name = str(a['clave'])
                                        # coords = [(a['latitud'], a['longitud'])]
                                        coords = [(a['longitud'], a['latitud'])]
                                        p = presentes.newpoint(name=name, coords=coords)
                                        p.style.labelstyle.color = simplekml.Color.green
                                if r_arboles_2:
                                    for a in r_arboles_2:
                                        name = str(a['clave'])
                                        # coords = [(a['latitud'], a['longitud'])]
                                        coords = [(a['longitud'], a['latitud'])]
                                        p = faltantes.newpoint(name=name, coords=coords)
                                        p.style.labelstyle.color = simplekml.Color.red
        kml.save(Exportador.nuevo_archivo(carpeta, 'kml'))
