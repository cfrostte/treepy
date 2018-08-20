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
        """Crea toda la ruta"""
        if not os.path.exists(r):
            os.makedirs(r)
            print("'", r, "' creado")

    @staticmethod
    def nuevo_archivo(carpeta, extencion):
        Exportador.crear_ruta(carpeta)
        n = datetime.datetime.now()
        o = "{}/Informe del día {} de {} de {}.{}"
        d = n.day
        m = Exportador.meses[n.month]
        y = n.year
        return o.format(carpeta, d, m, y, extencion)

    @staticmethod
    def correr_consulta(db):
        q = """SELECT e.nro AS A, r.nro AS B, c.nro AS C,
        a.clave AS D, a.latitud AS E, a.longitud AS F, 
        CASE WHEN (SELECT 1 FROM arboles_faltantes 
        WHERE id_arboles = a.clave) THEN 'Si' ELSE 'No' END AS G, 
        a.areaCopa AS H FROM arboles AS a JOIN parcelas AS p 
        JOIN bloques AS b JOIN repeticiones AS r JOIN ensayos AS e 
        JOIN clones AS c WHERE a.id_parcelas = p.clave 
        AND p.id_bloques = b.clave AND b.id_repeticiones = r.clave 
        AND r.id_ensayos = e.clave AND c.clave = p.id_clones"""
        return Base.consultar(db, q)

class CSV(Exportador):
    @staticmethod
    def informe(db, carpeta):
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
            for x in Exportador.correr_consulta(db):
                fila = {
                    '{}'.format(header[0]) : x['A'],
                    '{}'.format(header[1]) : x['B'],
                    '{}'.format(header[2]) : x['C'],
                    '{}'.format(header[3]) : x['D'],
                    '{}'.format(header[4]) : x['E'],
                    '{}'.format(header[5]) : x['F'],
                    '{}'.format(header[6]) : x['G'],
                    '{}'.format(header[7]) : x['H']
                }
                dw.writerow(fila)
        # Debuggear el archivo
        with open(archivo, newline='\n') as a:
            dr = csv.DictReader(a)
            for fila in dr:
                print(fila)

# class KML(Exportador):
#     @staticmethod
#     def informe(db, carpeta):
#         """Opcion 1 : Exportar datos sin utilizar jerarquia"""
#         kml = simplekml.Kml()
#         for x in Exportador.correr_consulta(db):
#             p = kml.newpoint(name=str(x['D']), coords=[(x['E'], x['F'])])
#             p.style.labelstyle.color = simplekml.Color.red if x['G'] == 'Si' else simplekml.Color.green
#         kml.save(Exportador.nuevo_archivo(carpeta, 'kml'))

class KML(Exportador):
    @staticmethod
    def informe(db, carpeta):
        """Opcion 2 : Exportar datos de forma jerarquica"""
        kml = simplekml.Kml()
        q_ensayos = """SELECT ensayos.* FROM ensayos JOIN objetos
        WHERE clave = id AND tipo = 'Ensayo' AND eliminado = 0 AND EXISTS
        (SELECT 1 FROM repeticiones WHERE id_ensayos = ensayos.clave)"""
        r_ensayos = Base.consultar(db, q_ensayos)
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
                        q_arboles = """SELECT arboles.*, CASE WHEN (SELECT 1 FROM arboles_faltantes
                        WHERE id_arboles = arboles.clave) THEN 1 ELSE 0 END AS faltante FROM arboles 
                        JOIN objetos WHERE clave = id AND tipo = 'Arbol' AND eliminado = 0 AND id_repeticiones = ?"""
                        r_arboles = Base.consultar(db, q_arboles, (r['clave'], ))
                        if r_arboles:
                            faltantes = f_r.newfolder(name='Árboles Faltantes')
                            presentes = f_r.newfolder(name='Árboles Presentes')
                            for a in r_arboles:
                                name = str(a['clave'])
                                coords = [(a['latitud'], a['longitud'])]
                                if a['faltante']:
                                    p = faltantes.newpoint(name=name, coords=coords)
                                    p.style.labelstyle.color = simplekml.Color.red
                                else:
                                    p = presentes.newpoint(name=name, coords=coords)
                                    p.style.labelstyle.color = simplekml.Color.green
        kml.save(Exportador.nuevo_archivo(carpeta, 'kml'))
