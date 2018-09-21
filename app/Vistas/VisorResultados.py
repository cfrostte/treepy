from tkinter import *
import threading
from PIL import Image, ImageTk
import ctypes
from Analisis.tInterface import InterfaceDeteccion
from .ObjetosVisor.Grafo import Grafo, Nodo, Arista
import threading, queue
from ControladorDatos import ControladorDatos as CD
from math import acos, sqrt, pi
from networkx.readwrite import json_graph
import networkx as nx
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
			self.cajaMensaje.geometry('%dx%d+%d+%d' % (300, 100, 600, 300))
			self.cajaMensaje.title(titulo)
			self.cajaMensaje.grab_set()
			self.cajaMensaje.overrideredirect(1)
			self.cajaMensaje.config(relief=RAISED)
			self.cajaMensaje.bind("<Destroy>", self.destroyCajaMensaje)
			self.cajaMensaje.protocol("WM_DELETE_WINDOW",self.destroyCajaMensaje)
			self.cajaMensaje.b = Button(self.cajaMensaje, text="OK", command=self.destroyCajaMensaje, width=50)
			self.cajaMensaje.b.pack(side=BOTTOM,pady=10,padx=100)
			self.cajaMensaje.mensaje = Message(self.cajaMensaje, text=msg, width=300)
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
					args=(self.imagen, self.deteccion.grafo, punto1, punto2, self.queue))
				Tarea.deamon = True
				Tarea.start()
			else:
				self.escribirMensaje("Se necesitan setar dos coordenadas en la imagen", "Error", True)
		else:
			self.canvas.seteandoPuntos = True
			self.canvas.removiendoNodo = False
			self.canvas.agregandoNodo = False
			self.canvas.agregandoArista = False
			self.canvas.removiendoArista = False
			self.Controles.Siguiente.config(text="Guardar")

class Controles(Frame):
	def __init__(self, parent, canvas):
		Frame.__init__(self, parent)
		self.parent = parent
		self.Add_Node=None
		self.Add_Edge=None
		self.Rem_Node=None
		self.Rem_edge=None
		self.mensaje=None
		self.analizar=None
		self.Siguiente=None
		self.Volver=None
		self.Init()
		self.canvas = canvas
	def Init(self):	
		if self.Add_Node!=None: self.Add_Node.destroy()
		if self.Add_Edge!=None: self.Add_Edge.destroy()
		if self.Rem_Node!=None: self.Rem_Node.destroy()
		if self.Rem_edge!=None: self.Rem_edge.destroy()
		if self.mensaje!=None: self.mensaje.destroy()
		if self.analizar!=None:  self.analizar.destroy()
		if self.Siguiente!=None: self.Siguiente.destroy()
		if self.Volver!=None: self.Volver.destroy()

		self.Add_Node = Button(self, text ="Agregar Árbol", state=DISABLED, command = self.addNode)
		self.Add_Node.pack(side=LEFT)
		self.Add_Edge = Button(self, text ="Agregar Unión", state=DISABLED, command = self.addArista)
		self.Add_Edge.pack(side=LEFT)
		self.Rem_Node = Button(self, text ="Remover Árbol", state=DISABLED, command = self.remNode)
		self.Rem_Node.pack(side=LEFT)
		self.Rem_edge = Button(self, text ="Remover Unión", state=DISABLED, command = self.remArista)
		self.Rem_edge.pack(side=LEFT)
		self.mensaje = Label(self, text = "Dibujar poligono",fg='red')
		self.mensaje.pack(side=LEFT)
		self.analizar = Button(self, text ="Analizar", command = self.correrAnalisis)
		self.analizar.pack(side=RIGHT)
		self.Siguiente = Button(self, state=DISABLED, text ="Siguiente", command = self.parent.Georeferenciar)
		self.Siguiente.pack(side=RIGHT)
		self.Volver = Button(self, text ="Volver", command=self.volver)
		self.Volver.pack(side=RIGHT)

	def volver(self):
		aux = self.parent.controladorVista
		aux.raise_frame(aux.misframes["Analisis"], aux.misframes["Repeticion"])

	def activarEdicion(self):
		self.Rem_edge.config(state=NORMAL)
		self.Rem_Node.config(state=NORMAL)
		self.Add_Edge.config(state=NORMAL)
		self.Siguiente.config(state=NORMAL)
	def addNode(self):
		self.mensaje.config(text="Seleccione ubicacion del nuevo árbol / Click derecho para finalizar")
		self.parent.canvas.agregandoNodo = True
		self.parent.canvas.removiendoNodo = False
		self.parent.canvas.agregandoArista = False
		self.parent.canvas.removiendoArista = False
		self.parent.canvas.deseleccionarNuevaArista()
	def remNode(self):
		self.mensaje.config(text="Seleccione árbol a eliminar / Click derecho para finalizar")
		self.parent.canvas.removiendoNodo = True
		self.parent.canvas.agregandoNodo = False
		self.parent.canvas.agregandoArista = False
		self.parent.canvas.removiendoArista = False
		self.parent.canvas.deseleccionarNuevaArista()
	def addArista(self):
		self.mensaje.config(text="Seleccione dos árboles a unir / Click derecho para finalizar")
		self.parent.canvas.removiendoNodo = False
		self.parent.canvas.agregandoNodo = False
		self.parent.canvas.agregandoArista = True
		self.parent.canvas.removiendoArista = False
		self.parent.canvas.deseleccionarNuevaArista()
	def remArista(self):		
		self.mensaje.config(text="Seleccione unión a eliminar / Click derecho para finalizar")
		self.parent.canvas.removiendoNodo = False
		self.parent.canvas.agregandoNodo = False
		self.parent.canvas.agregandoArista = False
		self.parent.canvas.removiendoArista = True
		self.parent.canvas.deseleccionarNuevaArista()
	def correrAnalisis(self):
		self.parent.correrAnalisis()

def _angulo(p0,p1,p2):  
	a = (p1[0]-p0[0])**2 + (p1[1]-p0[1])**2
	b = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
	c = (p2[0]-p0[0])**2 + (p2[1]-p0[1])**2
	return acos( (a+b-c) / sqrt(4*a*b) ) * 180/pi

def colorTriangulo(puntos):
	A,B,C = puntos
	return "#00D0FF" if _angulo(A,B,C)<130 and _angulo(C,A,B)<130 and _angulo(B,C,A)<130 else "#EE5500"
"""
	Este objeto se encarga del dibujado de todos los resultados y permite la edicion del mismo,
	asi como setear los conos de muestra para la georeferenciacion

"""
class CanvasVisorResultados(Canvas):
	"""docstring for CanvasVisorResultados"""
	def __init__(self, parent):
		Canvas.__init__(self, parent)
		self.parent = parent
		self.pos_x = 0
		self.pos_y = 0
		self.aspecto_x = 1
		self.aspecto_y = 1
		self.bind("<Button-1>", self.ClickEvent)
		self.bind("<Button-3>", self.ClickDerecho)
		self._actualizado = False
		self.editando = False
		self.grafos = []
		self.centros = []
		self.grafos_canvas = []
		self.ANCHO_ARBOL = 1
		self.imagen = None
		self.seleccionado = None
		self.grafo_seleccionado = None

		self.agregandoNodo=False
		self.agregandoArista=False
		self.removiendoNodo=False
		self.removiendoArista=False

		self.after(10,self._Update)
		self.oculto = False
		self.agregando_arista = None

		self.poligono = None
		self.puntospoligono=[]

		self.objetoBloqueo = None
		self.cursor_anterior = "arrow"

		self.geoPuntos = []
		self.seteandoPuntos = False
		self.puntoCentro = None
		self.triangulo = None

		self.seleccionNuevaArista = None
		self.GrafoAgregado = Grafo(self, nx.Graph(), -1, self.centros)

	def Inicio(self, imagen):
		self.Limpiar()
		self.im = Image.open(imagen)
		self.im_escalada = self.EscalarVista(self.im)
		self.photo = ImageTk.PhotoImage(self.im_escalada)
		self.item_image = self.create_image(0,0,anchor=NW, image=self.photo)
		self.config(width=self.im_escalada.size[0], height=self.im_escalada.size[1])
	def getCentro(self):
		return int(self.winfo_width()/2), int(self.winfo_height()/2)
	def bloquear(self):
		self.config(cursor="wait")
		self.objetoBloqueo = self.create_rectangle(0, 0, self.winfo_width(),self.winfo_height(),  fill='red',stipple="gray12")
	def desbloquear(self):
		self.config(cursor=self.cursor_anterior)
		if self.objetoBloqueo != None: self.delete(self.objetoBloqueo)
	def ClickDerecho(self,event):
		self.finEdicion()
	def finEdicion(self):
		self.parent.Controles.mensaje.config(text="")
		self.agregandoNodo = False
		self.removiendoNodo = False
		self.agregandoArista = False
		self.removiendoArista = False
		self.deseleccionarNuevaArista()
	def ClickEvent(self,event):
		if not self.editando:
			self.AddPuntoPoligono(event.x,event.y)
		elif self.removiendoNodo:
			id_seleccionado = event.widget.find_closest(event.x, event.y)[0]
			for g in self.grafos_canvas:
				seleccionado = g.GetNodo(id_seleccionado)
				if seleccionado != None:
					self.bloquear()
					self.parent.BorrarNodo(seleccionado.id_grafo)
					break
		elif self.agregandoNodo:
			id_seleccionado = event.widget.find_closest(event.x, event.y)[0]
			for g in self.grafos_canvas:
				seleccionado = g.GetNodo(id_seleccionado)
				if seleccionado != None:
					self.NodoSeleccionado =  seleccionado
					break
			if seleccionado is None:
				pass 
				''' 
				aca agregariamos un nodo utilizando "self.NodoSeleccionado" y event.x, 
				event.y, pero tendria que modificar el diccionadio de centroides 
				y no esta contemplado en el alcanse de nuestro desarrollo, nos vimo en Narnia.
				''' 
		elif self.removiendoArista:
			id_seleccionado = event.widget.find_closest(event.x, event.y)[0]
			for g in self.grafos_canvas:
				seleccionado = g.GetArista(id_seleccionado)
				if seleccionado != None:
					self.seleccionado = seleccionado
					self.bloquear()
					self.parent.BorrarArista(seleccionado.id_a,seleccionado.id_b)
					break
		elif self.agregandoArista:
			id_seleccionado = event.widget.find_closest(event.x, event.y)[0]
			seleccionado = None
			for g in self.grafos_canvas:
				seleccionado = g.GetNodo(id_seleccionado)
				if seleccionado is not None:
					break
			if self.seleccionNuevaArista is None:
				if seleccionado is not None:
					self.seleccionNuevaArista = seleccionado
					self.seleccionNuevaArista.pintar("blue")				
			elif seleccionado is not None and self.seleccionNuevaArista.id_grafo != seleccionado.id_grafo:
				self.nuevaArista(self.seleccionNuevaArista, seleccionado)
			else:
				self.deseleccionarNuevaArista()
		elif self.seteandoPuntos:
			if self.puntoCentro==None:
				centro = self.getCentro()
				x,y = centro
				self.puntoCentro = [self.create_oval(x-6,y-6,x+6,y+6,fill="#AA3595"),self.create_text(x,y,text="c")]
			x, y = event.x, event.y
			num = 1 if len(self.geoPuntos)==0 or self.geoPuntos[len(self.geoPuntos) - 1][3] == 2 else 2
			self.geoPuntos.append([
									self.create_oval(x-6,y-6,x+6,y+6,fill="red"),
									self.create_text(x,y,text=str(num)),
									(int(x*self.aspecto_x), int(y*self.aspecto_y)),
									num
								  ])
			if len(self.geoPuntos) > 2:				
				self.delete(self.geoPuntos[0][0])
				self.delete(self.geoPuntos[0][1])
				del(self.geoPuntos[0])
			if len(self.geoPuntos) == 2:
				if self.triangulo != None:
					self.delete(self.triangulo)
				triangulo = [[int(a[2][0]/self.aspecto_x),int(a[2][1]/self.aspecto_y)] for a in self.geoPuntos]
				triangulo.append(self.getCentro())
				color = colorTriangulo(triangulo)
				self.triangulo = self.create_polygon(triangulo,stipple="gray12", outline=color, fill=color, width=1)
		else:
			id_nodo = event.widget.find_closest(event.x, event.y)[0]
			for i,g in enumerate(self.grafos_canvas):
				if g.existe(id_nodo):
					g.pintar("blue")
					self.grafo_seleccionado = g
				else:
					g.pintar("#2f2")
	def nuevaArista(self, a, b):
		centros = self.centros
		centro_a = ((centros[a.id_grafo][0][0] / self.aspecto_x), (centros[a.id_grafo][0][1] / self.aspecto_y))
		centro_b = ((centros[b.id_grafo][0][0] / self.aspecto_x), (centros[b.id_grafo][0][1] / self.aspecto_y))
		self.grafos_canvas[0].unir(a.id_grafo, b.id_grafo,[centro_a,centro_b])

		_a = (centros[a.id_grafo][0][0] - self.ANCHO_ARBOL / 2) / self.aspecto_x
		_b = (centros[a.id_grafo][0][0] + self.ANCHO_ARBOL / 2) / self.aspecto_x
		_c = (centros[a.id_grafo][0][1] - self.ANCHO_ARBOL / 2) / self.aspecto_y
		_d = (centros[a.id_grafo][0][1] + self.ANCHO_ARBOL / 2) / self.aspecto_y
		self.grafos_canvas[0].addNodo([_a,_c,_b,_d], self.centros[a.id_grafo])

		_a = (centros[b.id_grafo][0][0] - self.ANCHO_ARBOL / 2) / self.aspecto_x
		_b = (centros[b.id_grafo][0][0] + self.ANCHO_ARBOL / 2) / self.aspecto_x
		_c = (centros[b.id_grafo][0][1] - self.ANCHO_ARBOL / 2) / self.aspecto_y
		_d = (centros[b.id_grafo][0][1] + self.ANCHO_ARBOL / 2) / self.aspecto_y
		self.grafos_canvas[0].addNodo([_a,_c,_b,_d], self.centros[b.id_grafo])
		self.deseleccionarNuevaArista()

	def deseleccionarNuevaArista(self):
		if self.seleccionNuevaArista is None:
			return
		self.seleccionNuevaArista.pintar("#2f2")
		self.seleccionNuevaArista = None

	def verDeteccion(self):
		if self.poligono: self.delete(self.poligono)
		self.puntospoligono = []
		self.bloquear()
		self.editando=True
	def AddPuntoPoligono(self, x,y):
		self.parent.poligono.append((x*self.aspecto_x,y*self.aspecto_y))
		self.puntospoligono.append((x,y))
		if self.poligono: self.delete(self.poligono)
		self.poligono = self.create_polygon(self.puntospoligono,stipple="gray12", outline='red', width=1)
	def CambiarImagen(self,imagen):
		self.imagen = imagen
		self.im = Image.open(imagen)
		self.im_escalada = self.EscalarVista(self.im)
		self.photo = ImageTk.PhotoImage(self.im_escalada)
		self.itemconfigure(self.item_image, image=self.photo)
		self.config(width=self.im_escalada.size[0], height=self.im_escalada.size[1])
		self.scale("all",0,0,self.aspecto_y,self.aspecto_x)
	def _Update(self):
		if not self._actualizado and self.grafos != []:
			self._actualizado = True
			self.editando = True
			self.dibujarGrafos()
		self.after(1,self._Update)
	def dibujarGrafos(self):
		grafoRespaldo = Grafo(self,nx.Graph(),-1,self.centros)	
		if len(self.grafos_canvas) > 0:
			grafoRespaldo = self.grafos_canvas[0]
		for i,g in enumerate(self.grafos_canvas): 
			if i > 0:
				g.borrar()
		self.grafos_canvas = [grafoRespaldo]
		grafoRespaldo.dibujar()
		for i,G in enumerate(self.grafos):
			G_canvas = Grafo(self,G,i,self.centros)
			G_canvas.dibujar()
			self.grafos_canvas.append(G_canvas)
	def AlternarVisibilidad(self):
		if self.oculto:
			Tarea = threading.Thread(name="alternar", target=self.desocultarResultados)
		else:
			Tarea = threading.Thread(name="alternar", target=self.ocultarResultados)
		Tarea.deamon = True
		Tarea.start()
	def ocultarResultados(self):
		for g in self.grafos_canvas:
			threading.Thread(name="ocultar", target=g.ocultar()).start()
		self.oculto = not self.oculto
	def desocultarResultados(self):
		for g in self.grafos_canvas:
			threading.Thread(name="desocultar", target=g.desocultar()).start()
		self.oculto = not self.oculto
	def Limpiar(self):
		self.editando = False
		for g in self.grafos_canvas: 
			g.borrar()
		self.grafos_canvas = []
	def PopOPAddFN(self):
		self.grafo_seleccionado = None
	def AddArista(self):
		self.agregando_arista = self.seleccionado
	def finAgregarArista(self,id_canvas_b):
		nodo = None
		grafo = None
		for g in self.grafos_canvas:
			grafo = g
			nodo = g.GetNodo(id_canvas_b)
			if nodo != None: 
				break
		if nodo == None:
			return
		self.parent.unir(self.agregando_arista.id_grafo, nodo.id_grafo)
		self.agregando_arista = None
	def GetScreensize(self):
		return 1200, 680#self.parent.winfo_width(), self.parent.winfo_height() - 50
	def EscalarVista(self, imagen):
		Screen = self.GetScreensize() 
		original_size = imagen.size		
		if original_size[0] > original_size[1]:
			new_width  = Screen[0]
			new_height = new_width * original_size[1] / original_size[0] 
			if new_height > Screen[1]:
				new_height = Screen[1]
				new_width  = new_height * original_size[0] / original_size[1]
		else:
			new_height = Screen[1]
			new_width  = new_height * original_size[0] / original_size[1]
		new_height = int(new_height)
		new_width = int(new_width)
		self.aspecto_x = original_size[0] / new_width
		self.aspecto_y = original_size[1] / new_height
		new_res = (new_width,new_height)
		return imagen.resize(new_res)
		