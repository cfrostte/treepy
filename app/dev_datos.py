"""..."""

from ControladorDatos import ControladorDatos as CD

# CD.crear_estructura()
# CD.volcar_datos_prueba()
# CD.respaldar_datos()

################################################################################

# for x in CD.buscar_objetos('Ensayo', {'nro' : 123}, ['clave'], False, None):
#     print(x)
#     for r in CD.obtener_relaciones_de(x, 'Repeticion', {'nro' : 987}):
#         print(r)

for ensayo in CD.buscar_objetos(tipo='Ensayo', filtro={'clave' : 1}, limite=1):
    for repeticion in CD.obtener_relaciones_de(ensayo, 'Repeticion'):
        print(repeticion)

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
