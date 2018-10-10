from tkinter import *
import tkinter.ttk as ttk
from tkcolorpicker import askcolor

class Bloque(object):
	def __init__(self, nombre, color):
		super(Bloque, self).__init__()
		self.nombre  = nombre 
		self.color  = color 

# class EditorBloques(Toplevel):
class EditorBloques(Frame):
	def __init__(self, colores, parentCtr, title="Editor de Bloques", command=None):
		Frame.__init__(self)
		# self.wm_title(title)
		style = ttk.Style(self)
		self.colores = colores
		print("Colores: " )
		print(self.colores)
		self.coloresbt = []
		self.parentCtr = parentCtr
		# self.transient(self.master)
		self.pack()
		btadd = Button(self.parentCtr.controles, text="Nuevo color", command=self.add)
		btadd.pack()
		self.coloresFr = Frame(self.parentCtr.controles)
		self.coloresFr.pack(side=RIGHT, padx=5, pady=5)
		for i,c in enumerate(self.colores):
			self.coloresbt.append(Button(self.coloresFr,text=c.nombre,bg=c.color, command=lambda b=c : self.parentCtr.seleccionarBloque(b)))
			self.coloresbt[i].pack()
	   
	def add(self):
		self.colores.append(Bloque("Color " + str(len(self.colores) + 1), askcolor((0, 0, 0), self)[1]))
		self.actualizar()

	def actualizar(self):
		for i,c in enumerate(list(self.coloresbt)):
			c.destroy()
			del self.coloresbt[0]

			print(self.colores)

		for i,c in enumerate(self.colores):
			self.coloresbt.append(Button(self.coloresFr,text=c.nombre,bg=c.color, command=lambda b=c : self.parentCtr.seleccionarBloque(b)))
			# print(c.color + " " + c.nombre + " " + str(i))
			self.coloresbt[i].pack()

