"""..."""

from ControladorDatos import ControladorDatos as CD

CD.crear_estructura()
CD.volcar_datos_prueba()
CD.respaldar_datos()

################################################################################

# for x in CD.buscar_objetos('Ensayo', {'nro' : 123}, ['clave'], False, None):
#     print(x)
#     for r in CD.ver_relacionados_de(x, 'Repeticion', {'nro' : 987}):
#         print(r)
