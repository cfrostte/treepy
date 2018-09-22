from ControladorDatos import ControladorDatos as CD
from Vistas.Vista_inicio import mainInicio

CD.crear_estructura()

ultimosModificados = CD.ultimos_modificados('Ensayo', 9)
todosLosEnsayos = CD.buscar_objetos('Ensayo')

mainInicio(ultimosModificados, todosLosEnsayos)
