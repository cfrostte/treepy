import os,sys
# sys.path.append("Analisis\\utils\\source")
from Analisis.utils.source.detection import *
import Analisis.utils.source.settings as config
# import settings as config
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
		config.use_auto_distance_thresh = False
		config.compute_VARI = True
		config.multiprocess_VARI = False
		config.algorithm = 2
		config.use_polynomial_regression = False
		self.detector = None
		self.queue = queue.Queue()
	def SetImage(self, img):
		self.img = img
		dir, filename = os.path.split(self.img)
		config.setSourceFolderName(dir)
		config.setImageFilename(filename)
		self.detector = Detection()
	def SetPoly(self, coords):
		self.polygon =  Polygon(coords)

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
	def AgregarArbol(self, x, y, id_sub=None):
		pass
	def AgregarArista(self, a, b):
		pass
	def Analizar(self):
		print("Inicio")
		self.queue.put("Inicio Segmentación")
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
		self.queue.put("Grafo final - Filtrando últimas uniones")
		for i in range(3):
		    graph_props_vf = filterUltimasEdges(graph_props_v4)
		graph_props_vf = filterNodeDegree(graph_props_vf)
		graph_props_vf.findSubgraphs()
		self.queue.put("Grafo final - Agregando nodos")
		AddNodes(graph_props_vf)
		self.queue.put("Grafo final - Dividiendo Surcos")
		grf2 = dividirSurco(graph_props_vf,2,20)
		self.queue.put("Grafo final - Filtrando surcos")
		grf2.findSubgraphs()
		self.grafo = grf2
		self.queue.put("Listo")