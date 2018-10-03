from tkinter import *
import ctypes
from Analisis.tInterface import InterfaceDeteccion
from .BarraControles import Controles
from .CanvasResultado import CanvasVisorResultados,GetScreensize
import threading, queue
from ControladorDatos import ControladorDatos as CD
from networkx.readwrite import json_graph
import json

class VisorResultados(Frame):
	"""docstring for VisorResultados"""
	def __init__(self, parent, controladorVista):
		Frame.__init__(self, parent)
		self.controladorVista = controladorVista
		self.deteccion = InterfaceDeteccion()
		self.poligono = []
		self.imagen = None
		self.repe = None
		self.cajaMensaje = None
		self.canvas = CanvasVisorResultados(self)
		self.canvas.pack(side=BOTTOM)
		self.Controles = Controles(self,self.canvas)
		self.Controles.pack(side=TOP,fill=X)
		self.titulo = Label(self, text = ">",fg='red')
		self.titulo.pack(side=TOP,fill=X)
		self.pack()
		self.queue = self.deteccion.queue
	def Analisis(self,imagen):
		if self.canvas : self.canvas.destroy()
		if self.titulo : self.titulo.destroy()
		if self.Controles : self.Controles.destroy()			
		self.canvas = CanvasVisorResultados(self)
		self.canvas.pack(side=BOTTOM)
		repe = CD.buscar_objetos('Repeticion', {'clave' : imagen.id_repeticiones})[0]
		ensayo = CD.buscar_objetos('Ensayo', {'clave' : repe.id_ensayos})[0]
		self.titulo = Label(self, text = ("Ensayo {} - {} ► Repetición {} ► {}").format(ensayo.establecimiento,ensayo.nro,repe.clave, imagen.fecha), font=('Courier', 16))
		self.titulo.pack(side=TOP,fill=X)
		self.Controles = Controles(self,self.canvas)
		self.Controles.pack(side=TOP,fill=X)
		self.pack()
		self.Controles.Init()
		self.deteccion = InterfaceDeteccion()
		self.imagen = imagen
		self.poligono = []
		self.queue = self.deteccion.queue
		self.deteccion.SetImage(imagen.url)
		self.canvas.Inicio(imagen.url)
		if imagen.grafo != None:
			data=json.loads(imagen.grafo)
			subgrafos = data['grafos']
			centros = data['centros']
			self.canvas.centros=centros
			for sg in subgrafos:
				self.canvas.grafos.append(json_graph.node_link_graph(sg))
			self.canvas._actualizado = False
			self.Analizado()
		else:
			self.escribirMensaje("Dibujar Polígono", "- Análisis - ", True)
	def Analizado(self):
		self.canvas.seteandoPuntos = False
		self.canvas.removiendoNodo = False
		self.canvas.agregandoNodo = False
		self.canvas.agregandoArista = False
		self.canvas.removiendoArista = False
		self.Controles.Add_Node.config(state=DISABLED)
		self.Controles.Add_Edge.config(state=DISABLED)
		self.Controles.Rem_Node.config(state=DISABLED)
		self.Controles.Rem_edge.config(state=DISABLED)
		self.Controles.analizar.config(state=DISABLED)
		self.Controles.Siguiente.config(state=DISABLED)
		self.escribirMensaje("Ya se analizó la imagen", "Analisis", True)

	def correrAnalisis(self):
		if len(self.poligono) < 3:
			respuesta = messagebox.askokcancel("Polígono", "Se recomienda dibujar un polígono, para mejorar los tiempos de detección")
			if respuesta is False:
				self.canvas.desbloquear()
				return
			self.poligono = [(0,0), (0,self.imagen.largo),(self.imagen.ancho,0),(self.imagen.ancho,self.imagen.largo)]
		self.canvas.verDeteccion()
		self.Controles.analizar.config(state=DISABLED)
		self.deteccion.SetPoly(self.poligono)
		self.poligono = []
		self.Espera()
		Tarea = threading.Thread(name="Analizar", target=self.deteccion.Analizar)
		Tarea.deamon = True
		Tarea.start()
	def BorrarNodo(self,id_nodo):
		self.Espera(True)
		Tarea = threading.Thread(name="Analizar", target=self.deteccion.BorrarNodo,args=(id_nodo,))
		Tarea.deamon = True
		Tarea.start()
	def BorrarArista(self, a,b):
		self.Espera(True)
		Tarea = threading.Thread(name="Analizar", target=self.deteccion.BorrarArista,args=(a,b))
		Tarea.deamon = True
		Tarea.start()
	def destroyCajaMensaje(self, e=None):
		if self.cajaMensaje != None:
			self.cajaMensaje.destroy()
		self.cajaMensaje = None
	def escribirMensaje(self, msg, titulo="- Análisis -", ok=None):
		if self.cajaMensaje is None:
			self.cajaMensaje = Toplevel()
			x,y = GetScreensize()
			self.cajaMensaje.geometry('%dx%d+%d+%d' % (300, 100, int(x/2)-150, int(y/2)-50))
			self.cajaMensaje.title(titulo)
			self.cajaMensaje.grab_set()
			self.cajaMensaje.overrideredirect(1)
			self.cajaMensaje.config(relief=RAISED)
			self.cajaMensaje.bind("<Destroy>", self.destroyCajaMensaje)
			self.cajaMensaje.protocol("WM_DELETE_WINDOW",self.destroyCajaMensaje)
			self.cajaMensaje.b = Button(self.cajaMensaje, text="OK", command=self.destroyCajaMensaje, width=50)
			self.cajaMensaje.b.pack(side=BOTTOM,pady=10,padx=100)
			self.cajaMensaje.mensaje = Label(self.cajaMensaje, text=msg, width=300)
			self.cajaMensaje.mensaje.pack(side=TOP, fill=BOTH)
		else:
			self.cajaMensaje.mensaje.config(text=msg)
		if ok==None or ok == False:
			self.cajaMensaje.b.pack_forget()	
		else:
			self.cajaMensaje.b.pack(side=BOTTOM,pady=10,padx=100)		
	def Espera(self, sacar=False):
		try:
			msg = self.queue.get(0)
			if sacar is True and str(msg)=="Listo":
				self.destroyCajaMensaje()
			else:
				self.escribirMensaje(msg,"- Análisis -",str(msg)=="Listo")
			if(str(msg)!="Listo"):
				self.after(1,lambda: self.Espera(sacar))
			else:
				self.canvas.ANCHO_ARBOL = 20
				self.canvas.grafos = [self.deteccion.grafo.subgraphs[i] for i in self.deteccion.grafo.subgraphs]
				self.canvas.faltantes = self.deteccion.grafo.node_props.coord_missing
				self.canvas.centros = self.deteccion.grafo.node_props.centroids
				self.canvas._actualizado = False
				self.canvas.desbloquear()
				self.Controles.activarEdicion()
		except queue.Empty:
			self.after(10,lambda: self.Espera(sacar))

	def EsperaReferenciar(self):
		try:
			msg = self.queue.get(0)
			self.escribirMensaje(msg,"- Análisis -",str(msg)=="Listo")
			if(str(msg)!="Listo"):
				self.after(1,self.EsperaReferenciar)
			else:
				self.destroyCajaMensaje()
				messagebox.showinfo("Listo","Los datos se guardaron correctamente")
				self.Controles.volver()
		except queue.Empty:
			self.after(10,self.EsperaReferenciar)

	def Georeferenciar(self):
		if self.canvas.seteandoPuntos:
			if(len(self.canvas.geoPuntos)==2):
				punto1=(0,0)
				punto2=(0,0)
				for g in self.canvas.geoPuntos:
					if g[3] == 1:
						punto1 = g[2]
					else:
						punto2 = g[2]
				self.EsperaReferenciar()
				subgrafos = [json_graph.node_link_data(self.deteccion.grafo.subgraphs[i]) for i in self.deteccion.grafo.subgraphs]
				centros=self.deteccion.grafo.node_props.centroids
				data = json.dumps({'grafos':subgrafos, 'centros':centros})
				self.imagen.grafo = data
				self.imagen.guardar(CD.db)
				Tarea = threading.Thread(
					name="Georeferenciar", 
					target=CD.analisis_a_objetos,
					args=(self.imagen, self.deteccion.grafo, punto1, punto2,self.canvas.parcelas, self.queue))
				Tarea.deamon = True
				Tarea.start()
			else:
				self.escribirMensaje("Se necesitan setar dos coordenadas en la imagen", "Error", True)
		elif not self.canvas.marcandoParcelas:
			self.Controles.mensaje.config(text="Click para marcar puntos de la parcela / Click derecho para confirmar")
			self.Controles.marcarParcelas()
			self.Controles.Siguiente.config(text="Marcar Conos")
		else:
			self.canvas.seteandoPuntos = True
			self.canvas.removiendoNodo = False
			self.canvas.agregandoNodo = False
			self.canvas.agregandoArista = False
			self.canvas.removiendoArista = False
			self.canvas.finParcelado()
			self.Controles.mensaje.config(text="Marcar los dos conos georeferenciados")
			self.Controles.Siguiente.config(text="Guardar")

