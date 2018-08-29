from tkinter import *
import threading
from PIL import Image, ImageTk
import ctypes
from Analisis.tInterface import InterfaceDeteccion
from .ObjetosVisor.Grafo import Grafo, Nodo
import threading, queue

class VisorResultados(Frame):
	"""docstring for VisorResultados"""
	def __init__(self,parent):
		Frame.__init__(self, parent)
		self.deteccion = InterfaceDeteccion()
		self.poligono = []
		self.canvas = CanvasVisorResultados(self)
		self.canvas.pack(side=BOTTOM)
		self.Controles = Controles(self,self.canvas)
		self.Controles.pack(side=TOP,fill=X)
		self.pack()
		self.queue = self.deteccion.queue
	def Analisis(self,imagen):
		self.deteccion.SetImage(imagen)
		self.canvas.Inicio(imagen)
	def correrAnalisis(self):
		self.canvas.verDeteccion()
		self.Controles.analizar.config(state=DISABLED)
		self.deteccion.SetPoly(self.poligono)
		self.poligono = []
		self.Espera()
		Tarea = threading.Thread(name="Analizar", target=self.deteccion.Analizar)
		Tarea.deamon = True
		Tarea.start()
	def BorrarNodo(self,id_nodo):
		self.Espera()
		Tarea = threading.Thread(name="Analizar", target=self.deteccion.BorrarNodo,args=(id_nodo,))
		Tarea.deamon = True
		Tarea.start()
	def BorrarArista(self, a,b):
		self.Espera()
		Tarea = threading.Thread(name="Analizar", target=self.deteccion.BorrarArista,args=(a,b))
		Tarea.deamon = True
		Tarea.start()
	def Espera(self):
		try:
			msg = self.queue.get(0)
			self.Controles.mensaje.config(text=msg)
			if(str(msg)!="Listo"):
				self.after(1,self.Espera)
			else:
				self.canvas.ANCHO_ARBOL = 20
				self.canvas.grafos = [self.deteccion.grafo.subgraphs[i] for i in self.deteccion.grafo.subgraphs]
				self.canvas.centros = self.deteccion.grafo.node_props.centroids
				self.canvas._actualizado = False
				self.canvas.desbloquear()
				self.Controles.activarEdicion()
		except queue.Empty:
			self.after(10,self.Espera)

class Controles(Frame):
	def __init__(self, parent, canvas):
		Frame.__init__(self, parent)
		self.Init()
		self.parent = parent
		self.canvas = canvas
	def Init(self):		
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

		self.Volver = Button(self, text ="Volver a Repetición", command = self.addNode)
		self.Volver.pack(side=RIGHT)
		self.Guardar = Button(self, text ="Siguiente", command = self.addNode)
		self.Guardar.pack(side=RIGHT)
	def activarEdicion(self):
		self.Rem_edge.config(state=NORMAL)
		self.Rem_Node.config(state=NORMAL)
	def addNode(self):
		self.mensaje.config(text="Seleccione ubicacion del nuevo árbol")
		self.parent.canvas.agregandoNodo = True
		self.parent.canvas.removiendoNodo = False
		self.parent.canvas.agregandoArista = False
		self.parent.canvas.removiendoArista = False
	def remNode(self):
		self.mensaje.config(text="Seleccione árbol a eliminar")
		self.parent.canvas.removiendoNodo = True
		self.parent.canvas.agregandoNodo = False
		self.parent.canvas.agregandoArista = False
		self.parent.canvas.removiendoArista = False
	def addArista(self):
		self.mensaje.config(text="Seleccione dos árboles a unir")
		self.parent.canvas.removiendoNodo = False
		self.parent.canvas.agregandoNodo = False
		self.parent.canvas.agregandoArista = True
		self.parent.canvas.removiendoArista = False
	def remArista(self):		
		self.mensaje.config(text="Seleccione unión a eliminar")
		self.parent.canvas.removiendoNodo = False
		self.parent.canvas.agregandoNodo = False
		self.parent.canvas.agregandoArista = False
		self.parent.canvas.removiendoArista = True
	def correrAnalisis(self):
		self.parent.correrAnalisis()
		
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
	def bloquear(self):
		self.config(cursor="wait")
		self.objetoBloqueo = self.create_rectangle(0, 0, self.winfo_width(),self.winfo_height(),  fill='red',stipple="gray12")
	def desbloquear(self):
		self.config(cursor=self.cursor_anterior)
		if self.objetoBloqueo != None: self.delete(self.objetoBloqueo)
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
		elif self.removiendoArista:
			id_seleccionado = event.widget.find_closest(event.x, event.y)[0]
			for g in self.grafos_canvas:
				seleccionado = g.GetArista(id_seleccionado)
				if seleccionado != None:
					self.seleccionado = seleccionado
					self.bloquear()
					self.parent.BorrarArista(seleccionado.id_a,seleccionado.id_b)
					break
		else:
			id_nodo = event.widget.find_closest(event.x, event.y)[0]
			for i,g in enumerate(self.grafos_canvas):
				if g.existe(id_nodo):
					g.pintar("blue")
					self.grafo_seleccionado = g
				else:
					g.pintar("#2f2")
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
	def Inicio(self, imagen):
		self.Limpiar()
		self.im = Image.open(imagen)
		self.im_escalada = self.EscalarVista(self.im)
		self.photo = ImageTk.PhotoImage(self.im_escalada)
		self.item_image = self.create_image(0,0,anchor=NW, image=self.photo)
		self.config(width=self.im_escalada.size[0], height=self.im_escalada.size[1])

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
		for g in self.grafos_canvas: 
			g.borrar()
		self.grafos_canvas = []
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