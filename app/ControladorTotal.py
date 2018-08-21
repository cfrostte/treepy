from ControladorDatos import ControladorDatos as CD
from Vistas.Vista_inicio_Copia import mainInicio
# from Vistas.Vista_inicio_Copia import mainInicio

ultimosModificados = CD.ultimos_modificados('Ensayo', 9)
todosLosEnsayo = CD.buscar_objetos('Ensayo')
# ultimosModificados = CD.buscar_objetos('Ensayo',None, None , False, None)
# ensayos = []
# repeticiones = []
# print(ultimosModificados)
# for ensayo in ultimosModificados:
# 	print("+++++++++++++++++++++++++++++++++")	
# 	# print(x)
# 	print(ensayo)
# 	print("+++++++++++++++++++++++++++++++++")
# 	ensayos.append(ensayo)
# 	print("-----------------------------------")
# 	print(CD.obtener_relaciones_de(ensayo, 'Repeticion'))
# 	print("-----------------------------------")
	# for repeticion in CD.obtener_relaciones_de(ensayo, 'Repeticion'):
		# print("---------------")
		# print(repeticion)
		# print("---------------")


# inicio.miapp(ultimosModificados)

# class getAllEnsayos(object):
# 	"""docstring for getAllEnsayos"""
# 	def __init__(self):espaciamientoYtodaLaMatriz
# 		super(getAllEnsayos, self).__init__()
# 		self.arg = CD.

# print(CD.buscar_objetos('Repeticion', ))

inicio = mainInicio(ultimosModificados, todosLosEnsayo)
