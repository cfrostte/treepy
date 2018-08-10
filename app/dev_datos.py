"""..."""

from ControladorDatos import ControladorDatos as CD

CD.crear_estructura()
CD.volcar_datos_prueba()
# CD.respaldar_datos()

################################################################################

# for x in CD.buscar_objetos('Ensayo', {'nro' : 123}, ['clave'], False, None):
#     print(x)
#     for r in CD.obtener_relaciones_de(x, 'Repeticion', {'nro' : 987}):
#         print(r)

# for ensayo in CD.buscar_objetos(tipo='Ensayo', filtro={'clave' : 1}, limite=1):
#     for repeticion in CD.obtener_relaciones_de(ensayo, 'Repeticion'):
#         print(repeticion)

# for x in CD.buscar_objetos('Ensayo', {'clave' : 1}, ['clave'], False, None):
#     print(x)
#     x.establecimiento = 3
#     x.guardar(CD.db)

# for x in CD.buscar_objetos('Ensayo', {'clave' : 2}, ['clave'], False, None):
#     print(x)
#     x.establecimiento = 4
#     x.guardar(CD.db)
#     x.eliminar(CD.db)

# for x in CD.ultimos_modificados('Ensayo', 3):
#     print(x)

# CD.exportar_informe_csv()
# CD.exportar_informe_kml()

# Para re-construir la matriz que representa la Repeticion:

# 1) Obtener nroFilas * nroColumnas de la Repeticion

# 2) Por cada (fila, columna) ver si existe en la Parcela

# 3) Si existe, mostrar en dicha (fila, columna) color del Bloque al que pertenece la Parcela y nro de Clon relacionado a esta.

for repeticion in CD.buscar_objetos(tipo='Repeticion', filtro={'clave' : 10}, limite=1):
    print(repeticion.matriz(CD.db))
