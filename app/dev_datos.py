"""..."""

from ControladorDatos import ControladorDatos as CD

# CD.crear_estructura()
# CD.volcar_datos_prueba()
# CD.respaldar_datos()

for x in CD.buscar_objetos('Ensayo', None, ['clave'], False, None):
    for r in CD.ver_relacionados_entre(x, 'Repeticion'):
        print(r)
