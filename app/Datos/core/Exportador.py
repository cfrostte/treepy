"""..."""
import csv

from .Base import Base

class CSV(object):
    @staticmethod
    def informe(db, archivo):
        # Escribir en archivo
        with open(archivo, 'w') as a:
            A = 'Ensayo'
            B = 'Repetición'
            C = 'Parcela'
            D = 'N° Árbol'
            E = 'Latitud'
            F = 'Longitud'
            G = 'Faltante'
            H = 'Área Copa'
            header = [A, B, C, D, E, F, G, H]
            dw = csv.DictWriter(a, fieldnames=header)
            dw.writeheader() # Escribir el header
            q = """SELECT DISTINCT e.nro AS A, e.nro AS B, c.nro AS C, a.clave AS D, a.latitud AS E, a.longitud AS F, 
            CASE WHEN af.clave IS NOT NULL THEN 'Si' ELSE 'No' END AS G, a.areaCopa AS H
            FROM ensayos AS e JOIN repeticiones AS r ON e.clave = r.id_ensayos
            JOIN clones AS c JOIN bloques AS b JOIN parcelas AS p ON c.clave = p.id_clones AND b.clave = p.id_bloques
            JOIN arboles AS a ON p.clave = a.id_parcelas LEFT JOIN arboles_faltantes AS af ON a.clave = af.id_arboles """
            for x in Base.consultar(db, q):
                fila = {
                    'Ensayo' : x['A'],
                    'Repetición' : x['B'],
                    'Parcela' : x['C'],
                    'N° Árbol' : x['D'],
                    'Latitud' : x['E'],
                    'Longitud' : x['F'],
                    'Faltante' : x['G'],
                    'Área Copa' : x['H']
                }
                dw.writerow(fila)
        # Debuggear el archivo
        with open(archivo, newline='\n') as a:
            dr = csv.DictReader(a)
            for fila in dr:
                print(fila)
        