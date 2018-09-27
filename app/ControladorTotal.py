from ControladorDatos import ControladorDatos as CD
from Vistas.Vista_inicio import mainInicio
# from Vistas.Vista_inicio_Copia import mainInicio

ultimosModificados = CD.ultimos_modificados('Ensayo', 9)
todosLosEnsayos = CD.buscar_objetos('Ensayo')

mainInicio(ultimosModificados, todosLosEnsayos)
