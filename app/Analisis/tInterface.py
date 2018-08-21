from .utils.source.detection import *
import .utils.source.settings as config
import os
import datetime, time
import threading, queue
from shapely.geometry import Polygon

class InterfaceDeteccion(object):
	"""docstring for InterfaceDeteccion"""
	def __init__(self, arg=None):
		super(InterfaceDeteccion, self).__init__()
		self.arg = arg
		config.initConfig()
		self.grafo = None
		config.setDebugMode(0)
		config.setMinAreaSize(200)
		config.setRGBThreshold([(0,60), (0,99), (0,70)])
		config.setDistanceThreshold(200)
		config.initLog('logfile')
		config.use_autocontrast = False
		config.use_automatic_segm_threshold = True
		config.compute_VARI = True
		config.multiprocess_VARI = False
		config.algorithm = 2
		config.use_polynomial_regression = False
		self.detector = Detection()
		self.queue = queue.Queue()
	def SetImage(self, img):
		self.img = img
		dir, filename = os.path.split(self.img)
		config.setSourceFolderName(dir)
		config.setImageFilename(filename)
	def SetPoly(self, coords):
		self.polygon =  Polygon(coords)
	def Analisis(self):
		Tarea = threading.Thread(name="Analizar", target=self.Analizar)
		Tarea.deamon = True
		Tarea.start()
		self.Espera()
	def BorrarNodo(self,id):
		self.queue.put(str("Removiendo nodo" + str(id)))
		self.grafo = removeNodes(id,self.grafo)
		self.queue.put("Recalculando")
		self.grafo.findSubgraphs()
		self.queue.put("Listo")
	def BorrarArista(self, a, b):
		self.queue.put(str("Removiendo arista" + str(a) + " - " + str(b)))
		self.grafo = removeEdges((a,b),self.grafo)
		self.queue.put("Recalculando")
		self.grafo.findSubgraphs()
		self.queue.put("Listo")

	# def Espera(self):
	# 	try:
	# 		msg = self.queue.get(0)
	# 		print(msg)
	# 		if(str(msg)!="Listo"):
	# 			time.sleep(1)
	# 			self.Espera()
	# 		else:
	# 			print(self.grafo)
	# 			# import matplotlib.pyplot as plt
	# 			# fig, ax = plt.subplots()
	# 			# ax.imshow(config.arr_overlay)
	# 			# ax = self.detector.drawRegions(self.grafo, ax)
	# 			# drawGraph(self.grafo)
	# 			# ax.set_axis_off()
	# 			# plt.tight_layout()
	# 			# plt.savefig("nombre.jpg")
	# 	except queue.Empty:
	# 		time.sleep(1)
	# 		self.Espera()
	def Analizar(self):
		print("Inicio")
		self.queue.put("Inicio Segmentacion")
		arr_binary = automaticSegmentation(self.detector)
		arr_closed = closing(arr_binary, square(3))
		arr_RGB = array(self.detector.img_RGB)
		self.queue.put("Etiquetado")
		arr_labeled = label(arr_closed)
		config.arr_overlay = label2rgb(arr_labeled, image=arr_RGB, alpha=0.2)
		self.queue.put("Grafo v0 - Buscando Árboles")
		graph_props_v0 = GraphProperties()
		self.queue.put("Grafo v0 - Filtrando por area")
		graph_props_v0.node_props = self.detector.filterRegionsByArea(arr_labeled, graph_props_v0.node_props,self.polygon)
		self.queue.put("Grafo v0 - Creando Grafo")
		graph_props_v0 = createGraph(graph_props_v0)
		graph_props_v0.findSubgraphs()
		self.queue.put("Grafo v1 - Filtrando surcos")
		graph_props_v1 = filterSubgraph(graph_props_v0)
		graph_props_v1.findSubgraphs()
		self.queue.put("Grafo v3 - Filtrando Uniones")
		graph_props_v3 = setCandidatesOfEdges(graph_props_v1)
		self.queue.put("Grafo v3 - Uniones Válidas")
		graph_props_v3.addEdgesCandidates()
		graph_props_v3.findSubgraphs()
		self.queue.put("Grafo v4 - Filtrando por cantidad de uniones")
		graph_props_v4 = filterNodeDegree(graph_props_v3)
		graph_props_v4.findSubgraphs()
		self.queue.put("Grafo vf - Filtrando ultimas uniones")
		for i in range(3):
		    graph_props_vf = filterUltimasEdges(graph_props_v4)
		graph_props_vf = filterNodeDegree(graph_props_vf)
		graph_props_vf.findSubgraphs()
		self.queue.put("Grafo vf - Agregando nodos")
		AddNodes(graph_props_vf)
		self.queue.put("Grafo vf - Dividiendo Surcos")
		grf2 = dividirSurco(graph_props_vf,2,20)
		self.queue.put("Grafo final - Filtrando surcos")
		grf2.findSubgraphs()
		self.grafo = grf2
		self.queue.put("Listo")

# inicio = datetime.datetime.now()
# I = InterfaceDeteccion()
# coords = [
# 				(522.2272727272726, 846.9025974025972), 
# 				(1017.3571428571428, 733.2662337662332), 
# 				(1171.5779220779218, 156.96753246753178), 
# 				(3314.4350649350654, 205.66883116883082), 
# 				(3119.6298701298706, 1382.6168831168827), 
# 				(2064.435064935065, 2843.655844155844), 
# 				(1228.3961038961038, 2827.4220779220777), 
# 				(984.8896103896103, 2251.1233766233763), 
# 				(895.6038961038961, 1480.01948051948), 
# 				(408.5909090909089, 1755.9935064935062), 
# 				(165.0844155844154, 1228.3961038961033)
# 		]
# I.SetPoly(coords)
# I.SetImage("data/arboles_0.jpg")
# I.Analisis()
# fin = datetime.datetime.now()
# print(inicio, fin, (fin-inicio))