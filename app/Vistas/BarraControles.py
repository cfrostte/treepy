from tkinter import *

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
		self.Siguiente = Button(self, state=DISABLED, text ="Marcar Parcelas", command = self.parent.Georeferenciar)
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
	def marcarParcelas(self):
		self.parent.canvas.inicioParcelado()
	def correrAnalisis(self):
		self.parent.correrAnalisis()