"""..."""

from ControladorDatos import ControladorDatos as CD
# from Datos.core.GeoEspacial import GeoEspacial as GE


CD.crear_estructura()
CD.volcar_datos_prueba(3)
# CD.respaldar_datos()

# print(CD.buscar_objetos('Ensayo'))
# a = CD.buscar_objetos('Ensayo',  {'clave' : 19})
# # print(CD.controlados['Ensayo'].buscar('Datos/store/treepy.db'))
# print(a[0])
# print(a[0].establecimiento)

# ensayo = CD.crear_objeto('Ensayo')
# print(ensayo)
# print('-----------------------')
# ensayo.nro = '44444'
# ensayo.establecimiento = 'nananana'
# ensayo.nroCuadro = '5555'
# ensayo.suelo = '55555555742355532'
# ensayo.espaciamientoX = '555'
# ensayo.espaciamientoY = '5.55555'
# ensayo.plantasHa = '5555555'
# ensayo.fechaPlantacion = '01/01/5555'
# ensayo.nroTratamientos = '5555'
# ensayo.totalPlantas = ''
# ensayo.totalHas = '5555'
# ensayo.plantasParcela = '55555'
# ensayo.tipoClonal = '555555'
# ensayo.nroRepeticiones = '555555'
# # print(ensayo)
# print(ensayo)
# print('-----------------------')
# guardado = ensayo.guardar(CD.db)
# print(guardado)
# guardado.totalPlantas = '1111111'
# print('-------anten----------------')
# print(guardado)
# print('------------antes-----------')
# guardado2 =  guardado.guardar(CD.db)

# clone = CD.buscar_objetos('Clon', {'nro' : '700'})
# print(clone)
# if clone:
# 	clone[0].nro = '777'
# 	g = clone[0].guardar(CD.db)
# else:
# 	clone = CD.crear_objeto('Clon')
# 	clone.nro = '7777'
# 	g = clone.guardar(CD.db)
# print(g)

# bloque = CD.buscar_objetos('Bloque', {'id_repeticiones' : '7', 'color' : 'rojsdo'})
# for x in bloque:self.repeticionClave
# print(bloque)
# print(bloque == [])
# print(bloque == None)

# repeticion = CD.buscar_objetos('Repeticion', {'clave' : '12'})[0]
# print(repeticion)
# bloques = CD.buscar_objetos('Bloque', {'id_repeticiones' : repeticion.clave})
# parcelas = []
# clones = []
# for bl in bloques:
# 	print(bl)
# 	parcelas += CD.buscar_objetos('Parcela', {'id_bloques' : bl.clave})

# for x in parcelas:
# 	print(x)
# 	clones += CD.buscar_objetos('Clon', {'clave' : x.id_clones})

# for x in clones:
# 	print(x)

# print(bloques[1])
# print(bloques[2])

# print(guardado2)
# print('-----------------------')
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

# for repeticion in CD.buscar_objetos(tipo='Repeticion', filtro={'clave' : 10}, limite=1):
#     print(repeticion.matriz(CD.db))

# CD.exportar_informe_csv(1)
# CD.exportar_informe_kml(1)

# CD.exportar_informe_csv()
# CD.exportar_informe_kml()

# for repeticion in CD.buscar_objetos(tipo='Repeticion', filtro={'clave' : 10}, limite=1):
#     print(repeticion.matriz(CD.db))

# for x in CD.buscar_objetos('Ensayo'):
#     print(x)

# cnvSz = 1000, 600

# cor1 = -32.316830, -58.087159
# cor2 = -32.317897, -58.086486
# cor3 = -32.317942, -58.085295

# xy1 = 349, 142
# xy2 = 469, 448
# xy3 = 698, 472

# g = GE.from_tiepoints([xy1, xy2, xy3], [cor1, cor2, cor3])
# print(g.transform([cnvSz])[0])

for ensayo in CD.buscar_objetos(tipo='Ensayo', filtro={'clave' : 1}, limite=1):
    print(ensayo)
    ensayo.eliminar_cascada(CD.db)
    