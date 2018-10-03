from tkinter import *
from ctypes import windll
import threading, queue
from .ObjetosVisor.Grafo import Grafo, GrafoFaltantes, Nodo, Arista
from .ObjetosVisor.Parcela import Parcela
from math import acos, sqrt, pi
import networkx as nx
from PIL import Image, ImageTk
def _angulo(p0,p1,p2):  
	a = (p1[0]-p0[0])**2 + (p1[1]-p0[1])**2
	b = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
	c = (p2[0]-p0[0])**2 + (p2[1]-p0[1])**2
	return acos( (a+b-c) / sqrt(4*a*b) ) * 180/pi

def colorTriangulo(puntos):
	A,B,C = puntos
	return "#00D0FF" if _angulo(A,B,C)<130 and _angulo(C,A,B)<130 and _angulo(B,C,A)<130 else "#EE5500"
def GetScreensize():
	return windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1) - 140
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
		self.faltantes = []
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
		self.marcandoParcelas = False
		self.parcelas = []
		self.nuevaParcela = False
		self.parcelaAcual = None
        self.contadorParcela = 0

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
		if self.marcandoParcelas:
			self.nuevaParcela = True
			self.AddParcela()
		else:
			self.finEdicion()
	def AddParcela(self):
		if self.parcelaAcual is not None and len(self.parcelaAcual.puntos) > 2:
			self.parcelas.append(self.parcelaAcual)
		else:
			if self.parcelaAcual is not None:
				self.parcelaAcual.borrar()
			del self.parcelaAcual
        self.contadorParcela += 1
		self.parcelaAcual = Parcela(self,self.contadorParcela)
	def finEdicion(self):
		self.parent.Controles.mensaje.config(text="")
		self.agregandoNodo = False
		self.removiendoNodo = False
		self.agregandoArista = False
		self.removiendoArista = False
		self.deseleccionarNuevaArista()
	def inicioParcelado(self):
		self.finEdicion()
		self.marcandoParcelas = True
		self.nuevaParcela = True
		self.parcelaAcual = Parcela(self)
	def finParcelado(self):
		self.ClickDerecho(None)
		self.marcandoParcelas = False

	def ClickEvent(self,event):
		if self.marcandoParcelas:
			if self.nuevaParcela:
				self.parcelaAcual.addPunto(event.x,event.y)
			else:
				self.parcelaAcual.addPunto(event.x,event.y)
		elif not self.editando:
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
					g.pintar()
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
		G_faltante = GrafoFaltantes(self,self.faltantes)
		G_faltante.dibujar()
		self.grafos_canvas.append(G_faltante)
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
	def EscalarVista(self, imagen):
		Screen = GetScreensize() 
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
		