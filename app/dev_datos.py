"""..."""

from ControladorDatos import ControladorDatos as CD

# CD.crear_estructura()
# CD.volcar_datos_prueba()
# CD.respaldar_datos()

################################################################################

# for x in CD.buscar_objetos('Ensayo', {'nro' : 123}, ['clave'], False, None):
#     print(x)
#     for r in CD.ver_relacionados_de(x, 'Repeticion', {'nro' : 987}):
#         print(r)

# CD.exportar_informe_csv()

for x in CD.buscar_objetos('Ensayo', {'clave' : 1}, ['clave'], False, None):
    print(x)
    x.nro = 1
    x.suelo = 2
    x.establecimiento = 3
    x.guardar(CD.db)