"""..."""

from ControladorDatos import ControladorDatos as CD

# CD.crear_estructura()
# CD.volcar_datos_prueba()
# CD.respaldar_datos()

# print(CD.buscar_objetos('Ensayo'))
# a = CD.buscar_objetos('Ensayo',  {'clave' : 19})
# # print(CD.controlados['Ensayo'].buscar('Datos/store/treepy.db'))
# print(a[0])
# print(a[0].establecimiento)

# ensayo = CD.crear_objeto('Ensayo')
# print(ensayo)
# ensayo.nro = '123'
# ensayo.establecimiento = 'Hola'
# ensayo.nroCuadro = '0192233'
# ensayo.suelo = '8.742332'
# ensayo.espaciamientoX = '4'
# ensayo.espaciamientoY = '3.0'
# ensayo.plantasHa = '1000'
# ensayo.fechaPlantacion = '01/01/1970'
# ensayo.nroTratamientos = '123'
# ensayo.totalPlantas = '345'
# ensayo.totalHas = '6765'
# ensayo.plantasParcela = '534'
# ensayo.tipoClonal = '789'
# ensayo.nroRepeticiones = '567'
# print(ensayo)
# guardado = ensayo.guardar(CD.db)
# print(ensayo)
# print(guardado)
################################################################################

# for x in CD.buscar_objetos('Ensayo', {'nro' : 123}, ['clave'], False, None):
#     print(x)
#     for r in CD.obtener_relaciones_de(x, 'Repeticion', {'nro' : 987}):
#         print(r)
# for ensayo in CD.buscar_objetos(tipo='Ensayo', filtro={'clave' : 1}, limite=1):
#     for repeticion in CD.obtener_relaciones_de(ensayo, 'Repeticion'):
#         print(repeticion)

# cont = 0
# for x in CD.buscar_objetos('Ensayo', {'clave' : 4}, ['clave'], False, None):
# 	print(str(cont))
# 	print(x.establecimiento)
# 	x.establecimiento = 3
# 	x.guardar(CD.db)
# 	cont = cont +  1

# for x in CD.buscar_objetos('Ensayo', {'clave' : 2}, ['clave'], False, None):
# 	print(x)
# 	x.establecimiento = 4
# 	x.guardar(CD.db)
# 	x.eliminar(CD.db)

# for x in CD.ultimos_modificados('Ensayo', 3):
#     print(x)

for repeticion in CD.buscar_objetos(tipo='Repeticion', filtro={'clave' : 10}, limite=1):
    print(repeticion.matriz(CD.db))

# CD.exportar_informe_csv()
# CD.exportar_informe_kml()
