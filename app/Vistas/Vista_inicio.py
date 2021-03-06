import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import cgitb
from inspect import getmembers
# from pprint import pprint
import random
from Vistas.esquemaParcelas import esquemaParcelas
# from Vistas.AbrirEnsayo import AbrirEnsayo
from ControladorDatos import ControladorDatos as CD
import tkinter.font as tkFont
import tkinter.ttk as tttk
import traceback
from Vistas.metadataInfo import metadataInfo
import shutil,os
import pathlib
from pathlib import Path
import datetime
import os
from tkinter import Widget

# import tkinter.filedialog as filedialog

from Vistas.VisorResultados import VisorResultados
import webbrowser

actualFrame = 1
def donothing():
	print("donothing")

class Inicio(object):
	__instance = None
	variableAyudaBorrar = 0

	def __new__(cls, misEnsayosRecientes, todosLosEnsayos):
		if Inicio.__instance is None:
			Inicio.__instance = object.__new__(cls)
		return Inicio.__instance

	def __init__(self, misEnsayosRecientes, todosLosEnsayos):
		self.misEnsayosRecientes = misEnsayosRecientes
		self.todosLosEnsayos = todosLosEnsayos
		self.root = tk.Tk()
		# self.root.geometry("1280x720")
		self.root.title("TreePy Análisis de Imágenes")
		self.root.state('zoomed')
		self.frameActivo = "Inicio"
		self.frameAnterior = ""

		misframes = ['Inicio', 'Ensayo', 'Repeticion', 'Analisis', 'ListaEnsayos', 'Acerca', 'Manual']
		self.misframes = self.generarFrames(misframes)
		self.misframes['Inicio'].pack(fill=tk.BOTH, padx=0, pady=0, expand=True)

		self.ensayosRecientes(self.misEnsayosRecientes)
		self.verEnsayo()
		self.verRepeticion()
		self.verAnalisis()
		self.verAyudas()
		
		self.root.config(menu=self.mimenu(self.root))
		# self.root.resizable(False, False)
		self.root.mainloop()

	def verAyudas(self):
		frame = tk.Frame(self.misframes['Manual'].interior)
		frame.pack()
		labelTitulo = ttk.Label(frame, text='Manual de usuario en linea')
		labelTitulo.pack(side=tk.TOP, fill=tk.BOTH)
		labelTitulo.config(font=("Courier", 33))
		# frameContainer = tk.Frame(self.misframes['Manual'].interior)
		# frameContainer.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
		link = ttk.Label(frame, text='Haga click aqui', foreground ="blue", cursor="hand2")
		link.pack(side=tk.TOP, fill=tk.BOTH)
		link.config(font=("Arial", 22))
		link.bind("<Button-1>", lambda event, arg='w':self.abrirLink())

		frame2 = tk.Frame(self.misframes['Acerca'].interior)
		frame2.pack()
		label1 = ttk.Label(frame2, text='TreePy Análisis de Imágenes')
		label2 = ttk.Label(frame2, text='Analizador de sobrevivencia y geolocalización de')
		label3 = ttk.Label(frame2, text='árboles en fotos aéreas de ensayos forestales.')
		label4 = ttk.Label(frame2, text='Este producto de software fue desarrollado por:')
		label5 = ttk.Label(frame2, text='• Jean Aramburu')
		label6 = ttk.Label(frame2, text='• Carlos Frostte')
		label7 = ttk.Label(frame2, text='• Guillermo Becker')
		label8 = ttk.Label(frame2, text='• Stephanie Rudenko')
		label1.pack(side=tk.TOP, fill=tk.BOTH)
		label1.config(font=("Arial", 22))
		label2.pack(side=tk.TOP, fill=tk.BOTH)
		label2.config(font=("Arial", 18))
		label3.pack(side=tk.TOP, fill=tk.BOTH)
		label3.config(font=("Arial", 18))
		label4.pack(side=tk.TOP, fill=tk.BOTH)
		label4.config(font=("Arial", 18))
		label5.pack(side=tk.BOTTOM, fill=tk.BOTH)
		label5.config(font=("Arial", 16))
		label6.pack(side=tk.BOTTOM, fill=tk.BOTH)
		label6.config(font=("Arial", 16))
		label7.pack(side=tk.BOTTOM, fill=tk.BOTH)
		label7.config(font=("Arial", 16))
		label8.pack(side=tk.BOTTOM, fill=tk.BOTH)
		label8.config(font=("Arial", 16))



		
	def abrirLink(self):
		webbrowser.open_new(r"https://docs.google.com/document/d/1_6xXUO0WHpcLgpsXxxOypeycEKFEB46O9rv-pBB8aZw/edit?usp=sharing")

	def verRepeticion(self):
		self.misframes['Repeticion'].camposEditables['totalFrame'], self.misframes['Repeticion'].camposEditables['frameContainer'] = [], []

		self.misframes['Repeticion'].camposEditables['totalFrame'].append(tk.Frame(self.misframes['Repeticion'].interior))
		self.misframes['Repeticion'].camposEditables['totalFrame'][-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['totalFrame'].append(tk.Frame(self.misframes['Repeticion'].interior))
		self.misframes['Repeticion'].camposEditables['totalFrame'][-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['totalFrame'].append(tk.Frame(self.misframes['Repeticion'].interior))
		self.misframes['Repeticion'].camposEditables['totalFrame'][-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		# self.misframes['Repeticion'].camposEditables['totalFrame'][-1].config(relief="raised", bd=8)
		# self.misframes['Repeticion'].camposEditables['totalFrame'][-1].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['totalFrame'].append(tk.Frame(self.misframes['Repeticion'].interior))
		self.misframes['Repeticion'].camposEditables['totalFrame'][-1].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		# self.misframes['Repeticion'].camposEditables['totalFrame'][-1].config(relief="raised", bd=8)

		self.misframes['Repeticion'].camposEditables['frameContainer'].append(tk.Frame(self.misframes['Repeticion'].camposEditables['totalFrame'][0]))
		self.misframes['Repeticion'].camposEditables['frameContainer'][-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.misframes['Repeticion'].camposEditables['tituloRepeticion'] = tk.Label(self.misframes['Repeticion'].camposEditables['frameContainer'][-1], text='Repeticion X')
		self.misframes['Repeticion'].camposEditables['tituloRepeticion'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['tituloRepeticion'].config(font=('Courier', 33))

		self.misframes['Repeticion'].camposEditables['frameContainer'].append(tk.Frame(self.misframes['Repeticion'].camposEditables['totalFrame'][1], height=100, background="bisque"))
		self.misframes['Repeticion'].camposEditables['frameContainer'][-1].pack(side=tk.TOP, fill=tk.BOTH)
		# self.misframes['Repeticion'].camposEditables['frameContainer'][-1].pack_propagate(0)
		# self.misframes['Repeticion'].camposEditables['frameContainer'][-1].config(relief="raised", bd=8)

		self.misframes['Repeticion'].camposEditables['subtituloEsquema'] = tk.Label(self.misframes['Repeticion'].camposEditables['frameContainer'][-1], text='Esquema de parcelas')
		self.misframes['Repeticion'].camposEditables['subtituloEsquema'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['subtituloEsquema'].config(font=('Courier', 22))
		self.misframes['Repeticion'].camposEditables['frameContainer'].append(tk.Frame(self.misframes['Repeticion'].camposEditables['totalFrame'][2]))
		self.misframes['Repeticion'].camposEditables['frameContainer'][-1].pack(side=tk.TOP, fill=tk.X, expand=True)

		self.misframes['Repeticion'].camposEditables['subtituloImagenes'] = tk.Label(self.misframes['Repeticion'].camposEditables['frameContainer'][-1], text='Imágenes')
		self.misframes['Repeticion'].camposEditables['subtituloImagenes'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['subtituloImagenes'].config(font=('Courier', 22))

		self.misframes['Repeticion'].camposEditables['frameesquema'] = esquemaParcelas(self.misframes['Repeticion'].camposEditables['totalFrame'][1])
		self.misframes['Repeticion'].camposEditables['frameesquema'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(relief="groove", bd=4)
		self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=770, height=655)
		self.misframes['Repeticion'].camposEditables['totalFrame'][1].pack_propagate(0)
		# self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=610)
		self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(relief="groove", bd=4)
		self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=770, height=655)
		self.misframes['Repeticion'].camposEditables['totalFrame'][2].pack_propagate(0)
		# self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=610)

		# self.misframes['Repeticion'].camposEditables['frameesquema'].repeticionClave = "Claveeeeee"
		# print("llllllllllllllllllllllllllllll")
		# print(self.misframes['Repeticion'].camposEditables['frameesquema'].repeticionClave)
		# print("llllllllllllllllllllllllllllll")

		self.misframes['Repeticion'].camposEditables['imagenesRepeticion'] = {}

		# self.misframes['Repeticion'].camposEditables['btnVolver'] = tk.Button(self.misframes['Repeticion'].camposEditables['totalFrame'][3], text="Volver", command=lambda: self.raise_frame(self.misframes[self.frameActivo], self.misframes[self.frameAnterior]))
		self.misframes['Repeticion'].camposEditables['btnVolver'] = tk.Button(self.misframes['Repeticion'].camposEditables['totalFrame'][3], text="Volver", command=lambda: self.raise_frame(self.misframes['Repeticion'], self.misframes['Ensayo']))
		self.misframes['Repeticion'].camposEditables['btnVolver'].pack(side=tk.BOTTOM)

	def verEnsayo(self):
		# Creo todos los campos del frame "Ver Ensayo" 
		print('émpieza ver ensayo')

		title = tk.Frame(self.misframes['Ensayo'].interior)
		title.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		tituloEnsayo = 'Ensayo Nro 2131'
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'] = tk.Label(title, text=tituloEnsayo)
		

		totalFrame = []
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		totalFrame[0].config(height=400, width=770, relief="groove", bd=4)
		totalFrame[1].config(height=400, width=770, relief="groove", bd=4)
		totalFrame[2].config(height=400, width=60)
		totalFrame[0].pack_propagate(0)
		totalFrame[1].pack_propagate(0)
		totalFrame[2].pack_propagate(0)

		self.misframes['Ensayo'].camposEditables['frameContainer'] = []
		self.misframes['Ensayo'].camposEditables['frameContainer'].append(tk.Frame(totalFrame[0]))
		self.misframes['Ensayo'].camposEditables['frameContainer'][-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

		# tituloEnsayo = 'Ensayo Nro 2131'
		# self.misframes['Ensayo'].camposEditables['tituloEnsayo'] = tk.Label(self.misframes['Ensayo'].camposEditables['frameContainer'][-1], text=tituloEnsayo)
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Ensayo'].camposEditables['numEnsayo'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'N° Ensayo: ', '3')
		self.misframes['Ensayo'].camposEditables['numRepeticiones'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'N° Repeticiones: ', '3')
		self.misframes['Ensayo'].camposEditables['establecimiento'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Establecimento: ', 'La Tribu')
		self.misframes['Ensayo'].camposEditables['numCuadro'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'N° Cuadro: ', 'H007')
		self.misframes['Ensayo'].camposEditables['suelo'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Suelo: ', '9.3')
		self.misframes['Ensayo'].camposEditables['espaciamiento'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Espaciamiento: ', '4 X 1.9')
		self.misframes['Ensayo'].camposEditables['plantasXha'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Plantas/Ha: ', '1315')
		self.misframes['Ensayo'].camposEditables['fechaPlantacion'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Fecha de plantación: ', '15/09/2017')
		self.misframes['Ensayo'].camposEditables['numTratamientos'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'N° Tratamientos: ', '27')
		self.misframes['Ensayo'].camposEditables['totalPlantas'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Total de plantas: ', '1620')
		self.misframes['Ensayo'].camposEditables['totalHas'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Total Has: ', '1.23')
		self.misframes['Ensayo'].camposEditables['plantasXparcela'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Plantas por parcela: ', '20')
		self.misframes['Ensayo'].camposEditables['tipoClonal'] = self.frameCreateCampo(self.misframes['Ensayo'].camposEditables['frameContainer'], totalFrame[0], 'Clonal: ', 'T2')

		self.misframes['Ensayo'].camposEditables['frameContainer'].append(tk.Frame(totalFrame[1]))
		self.misframes['Ensayo'].camposEditables['frameContainer'][-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		# tituloRepeticiones = 'Repeticiones'
		# self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'] = tk.Label(self.misframes['Ensayo'].camposEditables['frameContainer'][-1], text='Repeticiones')
		# self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		# self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'].config(font=("Courier",33))

		self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'] = {}

		self.misframes['Ensayo'].camposEditables['frameContainer'].append(tk.Frame(totalFrame[1]))
		self.misframes['Ensayo'].camposEditables['frameContainer'][-1].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		
		frameAbajo = tk.Frame(self.misframes['Ensayo'].camposEditables['frameContainer'][-1])
		frameAbajo.pack(side=tk.BOTTOM, expand=True)

		# self.misframes['Ensayo'].camposEditables['btnExportar'] = tk.Button(self.misframes['Ensayo'].camposEditables['frameContainer'][-1], text="Exportar", command=lambda: donothing)
		self.misframes['Ensayo'].camposEditables['btnExportar'] = tk.Button(frameAbajo, text="Exportar", command=lambda: donothing)
		self.misframes['Ensayo'].camposEditables['btnExportar'].pack(side=tk.RIGHT)
		# self.misframes['Ensayo'].camposEditables['btnModificarGuardar'] = tk.Button(self.misframes['Ensayo'].camposEditables['frameContainer'][-1], text="Modificar", command=lambda: self.clickBtnModificar('Modificar', 'Actualizar'))
		self.misframes['Ensayo'].camposEditables['btnModificarGuardar'] = tk.Button(frameAbajo, text="Modificar", command=lambda: self.clickBtnModificar('Modificar', 'Actualizar'))
		self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].pack(side=tk.RIGHT)
		# self.misframes['Ensayo'].camposEditables['btnAgregarRepeticion'] = tk.Button(self.misframes['Ensayo'].camposEditables['frameContainer'][-1], text="Agregar Repeticion", command=lambda: self.clickBtnAgregarRepeticion())
		# self.misframes['Ensayo'].camposEditables['btnAgregarRepeticion'].pack(side=tk.RIGHT, fill=tk.X)

		# self.misframes['Ensayo'].camposEditables['btn']		
		
		self.misframes['Ensayo'].camposEditables['btnVolver'] = tk.Button(totalFrame[2], text="Volver", command=lambda: self.raise_frame(self.misframes['Ensayo'], self.misframes['Inicio']))
		# self.misframes['Ensayo'].camposEditables['btnVolver'] = tk.Button(self.misframes['Ensayo'].camposEditables['frameContainer'][-1], text="Volver", command=lambda: self.raise_frame(self.misframes['Ensayo'], self.misframes['Inicio']))
		self.misframes['Ensayo'].camposEditables['btnVolver'].pack(side=tk.BOTTOM)

	def frameCreateCampo(self, frameContainer, parent, textLabel, textDato):
		frameContainer.append(tk.Frame(parent))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		frameuno = tk.Frame(frameContainer[-1])
		frameuno.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		frameuno.config(width=100)
		frameuno.config(relief="groove", bd=1)
		frameuno.pack_propagate(0)
		framedos = tk.Frame(frameContainer[-1])
		framedos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		framedos.config(width=100)
		framedos.config(relief="groove", bd=1)
		framedos.pack_propagate(0)
		# label = tk.Label(frameContainer[-1], text=textLabel).pack(side=tk.LEFT, fill=tk.BOTH)
		label = tk.Label(frameuno, text=textLabel).pack(side=tk.LEFT, fill=tk.BOTH)
		entry = self.createCampo(framedos, textDato)
		return entry

	def createCampo(self, frameContainer, texto):
		entry = tk.Entry(frameContainer)
		entry.config(width=100)
		entry.pack_propagate(0)
		entry.insert(0, texto)
		entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
		entry.config(state=tk.DISABLED)
		return entry

	def ensayosRecientes(self, ensayosRecientes):
		fotosEnsayos = []
		frameContainer=[]
		frame = tk.Frame(self.misframes['Inicio'].interior)
		frame.pack()
		labelTitulo = ttk.Label(frame, text='Ensayos Recientes')
		labelTitulo.pack(side=tk.TOP, fill=tk.BOTH)
		labelTitulo.config(font=("Courier", 33))
		frameContainer.append(tk.Frame(self.misframes['Inicio'].interior))
		frameContainer[-1].pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

		for ensayo in ensayosRecientes:
			frameContainerIn = []
			frameContainerIn.append(tk.Frame(frameContainer[-1]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			frameContainerIn.append(tk.Frame(frameContainer[-1]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

			datos = []
			nombre = 'Ensayo N° ' + str(ensayo.nro) + '\nEstablecimiento:  ' + str(ensayo.establecimiento)
			nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
			nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			ensayoImage = Image.open('Vistas/Image.jpg')
			# ensayoImage = Image.open('Vistas/Image.png')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			fotosEnsayos.append(datos)
			label.bind("<Button-1>", lambda event, arg=ensayo:self.clickEnsayoReciente(event,arg))
			if len(fotosEnsayos) % 3 ==0:
				print("salto")
				frameContainer.append(tk.Frame(self.misframes['Inicio'].interior))
				frameContainer[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		return fotosEnsayos

	def mimenu(self, root):
		self.root = root
		MENU = tk.Menu(root)	

		menu_archivo = tk.Menu(MENU, tearoff=0)
		# menu_edicion = tk.Menu(MENU, tearoff=0)
		# menu_vista = tk.Menu(MENU, tearoff=0)
		menu_ayuda = tk.Menu(MENU, tearoff=0)

		menu_archivo.add_command(label="Nuevo ensayo", command= lambda:self.NuevoEnsayo())
		menu_archivo.add_command(label="Abrir ensayo", command= lambda:self.AbrirEnsayo(self.misframes['ListaEnsayos'], self.todosLosEnsayos))
		# menu_archivo.add_command(label="Abrir ensayo", command= lambda:self.AbrirEnsayo(self.misframes['ListaEnsayos'], self.todosLosEnsayos))
		menu_archivo.add_separator()
		menu_archivo.add_command(label="Salir", command=root.quit)

		# menu_edicion.add_command(label="Editar Ensayo", command=lambda:self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo']))
		# menu_edicion.add_command(label="Editar Repeticion", command=lambda:self.raise_frame(self.misframes[self.frameActivo], self.misframes['Repeticion']))

		# menu_ayuda.add_command(label="Manual ", command=donothing)
		# menu_ayuda.add_command(label="Acerca de", command=donothing)
		menu_ayuda.add_command(label="Manual ", command=lambda:self.raise_frame(self.misframes[self.frameActivo], self.misframes['Manual']))
		menu_ayuda.add_command(label="Acerca de", command=lambda:self.raise_frame(self.misframes[self.frameActivo], self.misframes['Acerca']))

		MENU.add_cascade(label="Archivo", menu=menu_archivo)
		# MENU.add_cascade(label="Edicion", menu=menu_edicion)
		# MENU.add_cascade(label="Vista", menu=menu_vista)
		MENU.add_cascade(label="Ayuda", menu=menu_ayuda)
		
		return MENU

	def NuevoEnsayo(self):
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'].config(text='Ingrese nuevo ensayo', font=("Courier", 33))
		self.misframes['Ensayo'].camposEditables['numEnsayo'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['numEnsayo'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['numEnsayo'].insert(0, '000')
		self.misframes['Ensayo'].camposEditables['numRepeticiones'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['numRepeticiones'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['numRepeticiones'].insert(0, '3')
		self.misframes['Ensayo'].camposEditables['establecimiento'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['establecimiento'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['establecimiento'].insert(0, 'Nombre Establecimiento')
		self.misframes['Ensayo'].camposEditables['numCuadro'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['numCuadro'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['numCuadro'].insert(0, 'A000')
		self.misframes['Ensayo'].camposEditables['suelo'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['suelo'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['suelo'].insert(0, '0.0')
		self.misframes['Ensayo'].camposEditables['espaciamiento'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['espaciamiento'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['espaciamiento'].insert(0, '0 x 0.0')
		self.misframes['Ensayo'].camposEditables['plantasXha'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['plantasXha'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['plantasXha'].insert(0, '000')
		self.misframes['Ensayo'].camposEditables['fechaPlantacion'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['fechaPlantacion'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['fechaPlantacion'].insert(0, 'dd/mm/aaaa')
		self.misframes['Ensayo'].camposEditables['numTratamientos'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['numTratamientos'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['numTratamientos'].insert(0, '000')
		self.misframes['Ensayo'].camposEditables['totalPlantas'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['totalPlantas'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['totalPlantas'].insert(0, '000')
		self.misframes['Ensayo'].camposEditables['totalHas'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['totalHas'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['totalHas'].insert(0, '0.0')
		self.misframes['Ensayo'].camposEditables['plantasXparcela'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['plantasXparcela'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['plantasXparcela'].insert(0, '000')
		self.misframes['Ensayo'].camposEditables['tipoClonal'].config(state=tk.NORMAL)
		self.misframes['Ensayo'].camposEditables['tipoClonal'].delete(0, tk.END)
		self.misframes['Ensayo'].camposEditables['tipoClonal'].insert(0, 'T0')
		
		for x in range(0, len(self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'])):
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].pack_forget()
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].destroy()

		# self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].pack_forget()
		self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].config(text='Guardar', command= lambda: self.clickBtnModificar('Guardar', 'Nuevo'))
		self.misframes['Ensayo'].camposEditables['btnExportar'].pack_forget()

		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo'])

	# def AbrirEnsayo(self, frameEnsayo, todosLosEnsayos):
	def AbrirEnsayo(self, frameEnsayo, todosLosEnsayos):
		frameEnsayo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		# ok = AbrirEnsayo(frameEnsayo, todosLosEnsayos)
		# todosLosEnsayos = CD.buscar_objetos('Ensayo')
		self.openMultiColumn(frameEnsayo, todosLosEnsayos)
		self.raise_frame(self.misframes[self.frameActivo], frameEnsayo)

	def openMultiColumn(self, frameListaEnsayos, todosLosEnsayos):
		try: 
			self.misframes['ListaEnsayos'].camposEditables['titulo'].pack_forget()
			self.misframes['ListaEnsayos'].camposEditables['titulo'].destroy()
			self.misframes['ListaEnsayos'].camposEditables['lista'].pack_forget()
			self.misframes['ListaEnsayos'].camposEditables['lista'].destroy()
			self.misframes['ListaEnsayos'].camposEditables['frameTree'].pack_forget()
			self.misframes['ListaEnsayos'].camposEditables['frameTree'].destroy()
		except Exception:
			print("Error en openMulticolumn")

		self.misframes['ListaEnsayos'].interior.pack()
		self.misframes['ListaEnsayos'].camposEditables['titulo'] = tk.Frame(self.misframes['ListaEnsayos'].interior)
		self.misframes['ListaEnsayos'].camposEditables['titulo'].pack(side=tk.TOP, fill=tk.BOTH)
		self.misframes['ListaEnsayos'].camposEditables['lista'] = tk.Frame(self.misframes['ListaEnsayos'].interior)
		self.misframes['ListaEnsayos'].camposEditables['lista'].pack(side=tk.TOP, fill=tk.BOTH)

		labelTitulo = tk.Label(self.misframes['ListaEnsayos'].camposEditables['titulo'], text='Lista de ensayos')
		labelTitulo.pack(side=tk.TOP, fill=tk.BOTH)
		labelTitulo.config(font=("Courier", 33))

		# self.misframes['ListaEnsayos'].camposEditables['frameTree'] = tk.Frame(self.misframes['ListaEnsayos'].interior)
		self.misframes['ListaEnsayos'].camposEditables['frameTree'] = tk.Frame(self.misframes['ListaEnsayos'].camposEditables['lista'])
		# self.frame = tk.Frame(self.misframes['ListaEnsayos'].interior)
		self.misframes['ListaEnsayos'].camposEditables['frameTree'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		# self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		# self.ensayos_list = todosLosEnsayos
		todosLosEnsayosConsulta = CD.buscar_objetos('Ensayo')
		self.ensayos_list = todosLosEnsayosConsulta
		ensayos_header = ['Nro Ensayo', 'Establecimiento', 'Fecha de Plantacion', 'Clonal', 'Repeticiones', 'Tratamientos', 'Espaciamiento', 'Cuadro', 'Plantas por Ha', 'Plantas por parcela', 'Suelo', 'Total de Has', 'Total de plantas', '    ', '     ', '     ', '      ']
		''' Clase MultiColumnList '''
		self.tree = None
		self.car_header = ensayos_header
		self.car_list = self.ensayos_list
		# self.parent = self.frame
		self.parent = self.misframes['ListaEnsayos'].camposEditables['frameTree']

		self.tree = self._setup_widgets(self.parent, self.car_header)
		self.build_tree(self.car_list, self.car_header, self.tree)

	def _setup_widgets(self, parent, car_header):

		# style = ttk.Style()
		# style.element_create("Custom.Treeheading.border", "from", "default")
		# style.layout("Custom.Treeview.Heading", [
		#     ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
		#     ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
		#         ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
		#             ("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
		#             ("Custom.Treeheading.text", {'sticky':'we'})
		#         ]})
		#     ]}),
		# ])
		# style.configure("Custom.Treeview.Heading",
		#     background="blue", foreground="white", relief="flat")
		# style.map("Custom.Treeview.Heading",
		#     relief=[('active','groove'),('pressed','sunken')])


		self.parent = parent
		self.car_header = car_header
		# s = """click on header to sort by that column to change width of column drag boundary"""
		self.itemVar = None
		# msg = tttk.Label(wraplength="4i", justify="left", anchor="n",
            # padding=(10, 2, 10, 6), text=s)
		# msg.pack(side=tk.TOP, fill='x', expand=True)
		container = self.parent
		# self.tree = tttk.Treeview(columns=self.car_header, show="headings", style="Custom.Treeview")
		self.tree = tttk.Treeview(columns=self.car_header, show="headings")
		vsb = tttk.Scrollbar(orient="vertical", command=self.tree.yview)
		# hsb = tttk.Scrollbar(orient="horizontal", command=self.tree.xview)
		# self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
		self.tree.configure(yscrollcommand=vsb.set)
		self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
		self.tree.bind("<Double-1>", lambda event, :self.OnDoubleClick(event))
		vsb.grid(column=1, row=0, sticky='ns', in_=container)
		# hsb.grid(column=0, row=1, sticky='ew', in_=container)
		container.grid_columnconfigure(0, weight=1)
		container.grid_rowconfigure(0, weight=1)
		return self.tree

	def build_tree(self, car_list, car_header, tree):
		self.tree = tree
		self.car_header = car_header
		for col in self.car_header:
			self.tree.heading(col, text=col.title(), command=lambda c=col: self.sortby(self.tree, c, 0))
			self.tree.column(col, width=tkFont.Font().measure(col.title()))

		for item in car_list:
			itemArray = [item.nro, item.establecimiento, item.fechaPlantacion, item.tipoClonal, item.nroRepeticiones, item.nroTratamientos, item.espaciamientoX + ' X ' + item.espaciamientoY, item.nroCuadro, item.plantasHa, item.plantasParcela, item.suelo, item.totalHas, item.totalPlantas, '    ', '    ', '    ', '    ']
			self.tree.insert('', 'end', values=itemArray)
			for ix, val in enumerate(itemArray):
				col_w = tkFont.Font().measure(val)
				if self.tree.column(self.car_header[ix], width=None)<col_w:
					self.tree.column(self.car_header[ix], width=col_w)

	def OnDoubleClick(self, event):
		item = self.tree.identify('item',event.x,event.y)
		ensayo = CD.buscar_objetos('Ensayo', {'nro' : int(self.tree.item(item, "values")[0])})[0]
		self.updateFrameEnsayo(ensayo)
		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo'])

	def sortby(self, tree, col, descending):
		data = [(tree.set(child, col), child) \
			for child in tree.get_children('')]
		data.sort(reverse=descending)
		for ix, item in enumerate(data):
			tree.move(item[1], '', ix)
		# tree.heading(col, command=lambda col=col: MultiColumnListbox.sortby(tree, col, \
		tree.heading(col, command=lambda col=col: self.sortby(tree, col, \
			int(not descending)))

	def generarFrames(self, misframes):
		framesGenerados = {}
		for x in misframes:
			frame = VerticalScrolledFrame(self.root)
			frame.set_name(x)
			framesGenerados[x]=frame

		return framesGenerados

	def raise_frame(self, frame, newframe):
	    print("raise")
	    frame.pack_forget()
	    newframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	    self.frameActivo = newframe.get_name()
	    self.frameAnterior = frame.get_name()
	    print('Nuevo : '+ self.frameActivo + '___ Anterior : ' + self.frameAnterior)
	def clickVerRepeticion(self, repeticion, nroRepes, nroEnsayo, event=None,):
		self.updateFrameRepeticion(repeticion, nroRepes, nroEnsayo)
		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Repeticion'])

	def clickEnsayoReciente(self, event, ensayo):
		print("Click izquierdo")
		# print(ensayo.tipoClonal)
		self.updateFrameEnsayo(ensayo)

		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo'])

	# def borradorecursivo(self, widget):
		# for x in widget.winfo_children():


	def borrarImagen(self, imagen, frame):
		url = imagen.url.split('.jpg')[0].split('//')
		repeticion = CD.buscar_objetos(tipo='Repeticion', filtro={'clave' : imagen.id_repeticiones})[0]
		print("--------------------------Queiro ver repeticion-------------------------")
		print(repeticion)
		print("--------------------------Queiro ver repeticion-------------------------")
		nroRepes = CD.buscar_objetos(tipo='Ensayo', filtro={'clave' : url[-3]})[0].nroRepeticiones
		nroEnsayo = url[-3]
		respuesta = messagebox.askokcancel("Confirmar", "¿Está seguro que desea borrar?")
		if not respuesta:
			# print("------------------------------------")
			# print(url)
			# print("-------------------1111111111-----------------")
			return False
		# for ensayo in CD.buscar_objetos(tipo='Imagen', filtro={'clave' : imagen.clave}, limite=1):
			# print(ensayo)
		try:
			imagen.eliminar_cascada(CD.db)
		except Exception as e:
			messagebox.showinfo("Error", "Ha ocurrido un error al intentar borrar la imagen y todos sus datos asociados. \n" + str(e))
			return False
		 	# if frame.master:#padre principal
		print(frame)
		print("---------------------22222222---------------")
		print(enumerate(frame))
		print("---------------------333333333---------------")
		# print(frame[0].master)
		print("---------------------444444444---------------")
		# print(frame.winfo_children())
		print("------------------------------------")
		# if frame.master: 
		if not isinstance(frame, dict): 
			parent = frame.master 
			frame.destroy()
			for x, widget in enumerate(parent.winfo_children()):
				widget.winfo_children()[0].winfo_children()[0].winfo_children()[0].config(text="Imagen "+ str(x+1))
		else:
			# parent = self.misframes['Repeticion'].camposEditables['imagenesRepeticion']
			# self.misframes['Repeticion'].camposEditables['imagenesRepeticion'].pack_forget()
			parent = frame[0].master 
			frame[0].destroy()
		self.clickVerRepeticion(repeticion, nroRepes, nroEnsayo)
		# self.updateFrameRepeticion(repeticion, nroRepes, nroEnsayo)
			## self.misframes['Repeticion'].camposEditables['imagenesRepeticion'].destroy()

	def updateFrameRepeticion(self, repeticion=None, nroRepes=None, nroEnsayo=None):
		if 'frameAgregarNuevaImagen' in self.misframes['Repeticion'].camposEditables.keys():
			self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'].pack_forget()
			self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'].destroy()
		if 'containerImagenes' in self.misframes['Repeticion'].camposEditables.keys():
			self.misframes['Repeticion'].camposEditables['containerImagenes'].pack_forget()
			self.misframes['Repeticion'].camposEditables['containerImagenes'].destroy()
		for x in list(self.misframes['Repeticion'].camposEditables['imagenesRepeticion'].keys()):
			self.misframes['Repeticion'].camposEditables['imagenesRepeticion'][x].pack_forget()
			self.misframes['Repeticion'].camposEditables['imagenesRepeticion'][x].destroy()
		if self.misframes['Repeticion'].camposEditables['frameesquema'].grilla!=None:
			self.misframes['Repeticion'].camposEditables['frameesquema'].grilla.destroy() 
		print("--------------REPEEEEEEE-----------------")
		print(repeticion)
		print("--------------REPEEEEEEE-----------------")
		self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=770, height=655)
		self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=770, height=655)
		if repeticion.nroFilas != ' ' and repeticion.nroColumnas != ' ':
			#Dibujo el esquema de la repeticion
			self.misframes['Repeticion'].camposEditables['frameesquema'].repeticionClave = repeticion.clave
			self.misframes['Repeticion'].camposEditables['frameesquema'].dibujar(repeticion.clave)
			#
		if repeticion != None:
			pathImg = '//'+str(repeticion.id_ensayos)+'//'+str(repeticion.clave)
			imagenes = CD.buscar_objetos('Imagen', {'id_repeticiones' : repeticion.clave})
			self.misframes['Repeticion'].camposEditables['tituloRepeticion'].config(text="Ensayo N° "+str(nroEnsayo)+" ► Repetición "+str(repeticion.nro))
			self.misframes['Repeticion'].camposEditables['frameesquema'].repeticionClave = repeticion.clave
			self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'] = tk.Frame(self.misframes['Repeticion'].camposEditables['totalFrame'][2])
			self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			containerImagenes = tk.Frame(self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'])
			containerImagenes.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			containerNewImagen = tk.Frame(self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'])
			containerNewImagen.pack(side=tk.BOTTOM, fill=tk.BOTH,expand=True)
			self.misframes['Repeticion'].camposEditables['containerImagenes'] = containerImagenes

			if len(imagenes)<1:
				self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=770, height=455)
				self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=770, height=455)
			if len(imagenes)>1:
				self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_width(), height=100+( len(imagenes)*355))
				self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_width(), heigh=100+( len(imagenes)*355))


			for x in range(0, len(imagenes)):
				fotosRepeticion = []
				containerImg = tk.Frame(containerImagenes)
				containerImg.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
				containerImg.config(padx=10, pady=10, relief="raised", bd=8)
				self.misframes['Repeticion'].camposEditables['imagenesRepeticion'][x] = containerImg
				containerIzquierda = tk.Frame(containerImg)
				containerIzquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
				containerCentro = tk.Frame(containerImg)
				containerCentro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
				containerDerecha = tk.Frame(containerImg)
				containerDerecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
				frameContainerIn = []
				frameContainerIn.append(tk.Frame(containerIzquierda))
				frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
				frameContainerIn.append(tk.Frame(containerIzquierda))
				frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

				btnCambiarImagen = tk.Button(containerDerecha, text="Cambiar imagen", command=lambda accion="update", frameArg=self.misframes['Repeticion'].camposEditables['imagenesRepeticion'], claveRepeArg=repeticion.clave, claveEnsayoArg=repeticion.id_ensayos, y=x+1, izquierda=containerIzquierda, centro=containerCentro, derecha=containerDerecha, claveImagen=imagenes[x].clave: self.cambiarImagen(accion, frameArg, claveRepeArg, claveEnsayoArg, y, izquierda, centro, derecha, claveImagen))
				btnCambiarImagen.pack(side=tk.TOP)
				btnAnalizarImagen = tk.Button(containerDerecha, text="Analizar imagen", command=lambda image=imagenes[x]: self.iniciarAnalisis(image))
				btnAnalizarImagen.pack(side=tk.TOP)
				btnBorrarImagen = tk.Button(containerDerecha, text="Borrar", command=lambda image=imagenes[x], frame=containerImg: self.borrarImagen(image, frame))
				btnBorrarImagen.pack(side=tk.BOTTOM)

				subtituloDatos = tk.Label(containerCentro, text="Datos de la imagen")
				subtituloDatos.pack(side=tk.TOP, padx=5, pady=5, expand=True)
				subtituloDatos.config(font=('Courier', 16))

				etapa = tk.Label(containerCentro, text="Etapa : " + str(imagenes[x].etapa)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				ancho = tk.Label(containerCentro, text="Ancho(Pixels) : " + str(imagenes[x].ancho) + " Largo(Pixels) : " + str(imagenes[x].largo)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# largo = tk.Label(containerCentro, text="Largo(Pixels) : " + str(imagenes[x].largo)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				altitud = tk.Label(containerCentro, text="Altitud : " + str(imagenes[x].altitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				latitud = tk.Label(containerCentro, text="Lat y Lnt de la imagen : " + str(imagenes[x].latitud) + " " + str(imagenes[x].longitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# longitud = tk.Label(containerCentro, text="Longitud de la imagen : " + str(imagenes[x].longitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				latitudCono1 = tk.Label(containerCentro, text="Lat y Lnt del cono 1 : " + str(imagenes[x].latitudCono1) + " " + str(imagenes[x].longitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# longitudCono1 = tk.Label(containerCentro, text="Longitud del cono 1 : " + str(imagenes[x].longitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				latitudCono2 = tk.Label(containerCentro, text="Lat y Lnt del cono 2 : " + str(imagenes[x].latitudCono2) + " " + str(imagenes[x].longitudCono2)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# longitudCono2 = tk.Label(containerCentro, text="Longitud del cono 2 : " + str(imagenes[x].longitudCono2)).pack(side=tk.TOP, padx=5, pady=5, expand=True)

				# etapa = tk.Label(containerCentro, text="Etapa : " + str(imagenes[x].etapa)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# ancho = tk.Label(containerCentro, text="Ancho(Pixels) : " + str(imagenes[x].ancho)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# largo = tk.Label(containerCentro, text="Largo(Pixels) : " + str(imagenes[x].largo)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# altitud = tk.Label(containerCentro, text="Altitud : " + str(imagenes[x].altitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# latitud = tk.Label(containerCentro, text="Latitud de la imagen : " + str(imagenes[x].latitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# longitud = tk.Label(containerCentro, text="Longitud de la imagen : " + str(imagenes[x].longitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# latitudCono1 = tk.Label(containerCentro, text="Latitud del cono 1 : " + str(imagenes[x].latitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# longitudCono1 = tk.Label(containerCentro, text="Longitud del cono 1 : " + str(imagenes[x].longitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# latitudCono2 = tk.Label(containerCentro, text="Latitud del cono 2 : " + str(imagenes[x].latitudCono2)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
				# longitudCono2 = tk.Label(containerCentro, text="Longitud del cono 2 : " + str(imagenes[x].longitudCono2)).pack(side=tk.TOP, padx=5, pady=5, expand=True)

				
				datos = []
				nombre = 'Imagen ' + str(x+1)
				nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
				nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
				print("====================Esto es lo que preciso====================")
				print(nombrelabel)
				fechalabel = tk.Label(frameContainerIn[0], text=imagenes[x].fecha)
				fechalabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
				path = str(Path().absolute())
				try:
					ensayoImage = Image.open(imagenes[x].url)
				except:
					ensayoImage = Image.open(path + '\\Vistas\\notFound.jpg')
					# ensayoImage = Image.open('C:/Users/v785712/Desktop/projectoMerge/treepy/app/Vistas/notFound.jpg')
				ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
				photo = ImageTk.PhotoImage(ensayoImage)
				label = tk.Label(frameContainerIn[1], image=photo)
				label.image = photo
				label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
				datos.append(label)
				datos.append(nombrelabel)
				datos.append(fechalabel)
				fotosRepeticion.append(datos)
				if len(fotosRepeticion) % 3 ==0:
					print("salto imegen repe")
					self.misframes['Repeticion'].camposEditables['frameContainer'].append(tk.Frame(self.misframes['Repeticion'].camposEditables['totalFrame'][2]))
					self.misframes['Repeticion'].camposEditables['frameContainer'][-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
			containerNewImg = tk.Frame(containerNewImagen)
			containerNewImg.pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			containerNewImg.config(padx=10, pady=10, relief="raised", bd=4)
			containerNewImg.config(width=770, height=50)
			containerNewImg.pack_propagate(0)
			self.misframes['Repeticion'].camposEditables['agregar'] = containerNewImg
			btnCambiarImagen = tk.Button(containerNewImg, text="Agregar imagen", command=lambda: self.cambiarImagen("new", self.misframes['Repeticion'].camposEditables['imagenesRepeticion'], repeticion.clave, repeticion.id_ensayos, len(self.misframes['Repeticion'].camposEditables['imagenesRepeticion'])+1))
			btnCambiarImagen.pack(side=tk.TOP)


		else:
			# donothing
			self.misframes['Repeticion'].camposEditables['tituloRepeticion'].config(text="Repetición "+str(repeticion.nro))
			self.misframes['Repeticion'].camposEditables['frameesquema'].repeticionClave = repeticion.clave
			self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'] = tk.Frame(self.misframes['Repeticion'].camposEditables['totalFrame'][2])
			self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			containerNewImagen = tk.Frame(self.misframes['Repeticion'].camposEditables['frameAgregarNuevaImagen'])
			containerNewImagen.pack(side=tk.BOTTOM, fill=tk.BOTH,expand=True)
			containerNewImg = tk.Frame(containerNewImagen)
			containerNewImg.pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			containerNewImg.config(padx=10, pady=10, relief="raised", bd=4)
			containerNewImg.config(width=770, height=50)
			containerNewImg.pack_propagate(0)
			self.misframes['Repeticion'].camposEditables['agregar'] = containerNewImg
			btnCambiarImagen = tk.Button(containerNewImg, text="Agregar imagen", command=lambda: self.cambiarImagen("update", self.misframes['Repeticion'].camposEditables['imagenesRepeticion'], repeticion.clave, repeticion.id_ensayos))
			btnCambiarImagen.pack(side=tk.TOP)

	def clickGuardoImagen(self, accion, frame, claveRepe, claveEnsayo, x=None, izquierda=None, centro=None, derecha=None, claveImagen=None):
		# if not datosParaGuardar['numCuadro'] or datosParaGuardar['numCuadro'].isspace():
			# check.append('numCuadro')
		
		checkeo = self.checkearCamposDatosImagen()
		if checkeo:
			for x in checkeo:
					self.misframes['Repeticion'].camposEditables[x].config(state=tk.NORMAL, background="#ff8282")
			messagebox.showinfo("Error", "Controle el formato de datos ingresado y que no haya campos vacios e intente nuevamente.")
			return False

		if accion == 'new':
			nuevaImagen = CD.crear_objeto('Imagen')
		else:
			nuevaImagen =  CD.buscar_objetos('Imagen',  {'clave' : claveImagen})[0]
			#Tomo y guardo los datos de la imagen, y la copia al directorio del programa
		src = askopenfilename()
		if not src:
			return False
		info = metadataInfo(src)
		nuevaImagen.fecha = info['fecha']
		nuevaImagen.largo = info['height']
		nuevaImagen.ancho = info['width']
		nuevaImagen.latitud = info['lat']
		nuevaImagen.longitud = info['lon']
		nuevaImagen.altitud = info['altitud']
		nuevaImagen.id_repeticiones = claveRepe
		nuevaImagen.etapa = self.misframes['Repeticion'].camposEditables['etapaEntry'].get()
		nuevaImagen.url = ' ' # NO COMENTAR
		nuevaImagen.latitudCono1 = self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].get()
		nuevaImagen.longitudCono1 = self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].get()
		nuevaImagen.latitudCono2 = self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].get()
		nuevaImagen.longitudCono2 = self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].get()
		guardado = nuevaImagen.guardar(CD.db)
		path =  str(Path().absolute()) + '//Datos//store//img//'+str(claveEnsayo)+'//'+str(claveRepe)+'//'+str(guardado.clave)+'.jpg'
		pathlib.Path(str(Path().absolute()) + '//Datos//store//img//'+str(claveEnsayo)+'//'+str(claveRepe)+'//').mkdir(parents=True, exist_ok=True) 
		shutil.copy(src, path) 
		guardado.url = path
		nuevaImagen = guardado.guardar(CD.db)
		#Despues de guardar deberia mostrar la nueva imagen
		for widget in izquierda.winfo_children():
			widget.destroy()
		for widget in centro.winfo_children():
			widget.destroy()
		for widget in derecha.winfo_children():
			widget.destroy()
		frameContainerIn = []
		frameContainerIn.append(tk.Frame(izquierda))
		frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
		frameContainerIn.append(tk.Frame(izquierda))
		frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
		self.misframes['Repeticion'].camposEditables['btnElegirImagen'].pack_forget()
		self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'].pack_forget()
		self.misframes['Repeticion'].camposEditables['btnCambiarImagen'] = tk.Button(derecha, text="Cambiar imagen", command=lambda accion="update", frameArg=self.misframes['Repeticion'].camposEditables['imagenesRepeticion'], claveRepeArg=claveRepe, claveEnsayoArg=claveEnsayo, y=len(frame), claveImagen=nuevaImagen.clave: self.cambiarImagen(accion, frameArg, claveRepeArg, claveEnsayoArg, y, izquierda, centro, derecha, claveImagen))
		self.misframes['Repeticion'].camposEditables['btnCambiarImagen'].pack(side=tk.TOP)
		self.misframes['Repeticion'].camposEditables['btnAnalizarImagen'] = tk.Button(derecha, text="Analizar imagen", command=lambda: self.iniciarAnalisis(nuevaImagen))
		self.misframes['Repeticion'].camposEditables['btnAnalizarImagen'].pack(side=tk.TOP)
		self.misframes['Repeticion'].camposEditables['btnBorrarImagen'] = tk.Button(derecha, text="Borrar", command=lambda: self.borrarImagen(nuevaImagen, frame))
		self.misframes['Repeticion'].camposEditables['btnBorrarImagen'].pack(side=tk.BOTTOM)
		subtituloDatos = tk.Label(centro, text="Datos de la imagen")
		subtituloDatos.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		subtituloDatos.config(font=('Courier', 16))
		etapa = tk.Label(centro, text="Etapa : " + str(nuevaImagen.etapa)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		ancho = tk.Label(centro, text="Ancho : " + str(nuevaImagen.ancho)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		largo = tk.Label(centro, text="Largo : " + str(nuevaImagen.largo)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		altitud = tk.Label(centro, text="Altitud : " + str(nuevaImagen.altitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		latitudCono1 = tk.Label(centro, text="Latitud cono 1 : " + str(nuevaImagen.latitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		longitudCono1 = tk.Label(centro, text="Longitud cono 1 : " + str(nuevaImagen.longitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		latitudCono2 = tk.Label(centro, text="Latitud cono 2 : " + str(nuevaImagen.latitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		longitudCono2 = tk.Label(centro, text="Longitud cono 2 : " + str(nuevaImagen.longitudCono2)).pack(side=tk.TOP, padx=5, pady=5, expand=True)

		datos = []
		nombre = 'Imagen ' + str(x)
		# nombre = 'Imagen ' + str(len(frame))
		nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
		nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		fechalabel = tk.Label(frameContainerIn[0], text=nuevaImagen.fecha)
		fechalabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		ensayoImage = Image.open(nuevaImagen.url)
		ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(ensayoImage)
		label = tk.Label(frameContainerIn[1], image=photo)
		label.image = photo
		label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		datos.append(label)
		datos.append(nombrelabel)
		datos.append(fechalabel)

	def cambiarImagen(self, accion, frame, claveRepe, claveEnsayo, x=None, izquierda=None, centro=None, derecha=None, claveImagen=None):
		if accion == "new":
			containerImg = tk.Frame(self.misframes['Repeticion'].camposEditables['containerImagenes'])
			containerImg.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			containerImg.config(padx=10, pady=10, relief="raised", bd=8)
			if len(frame)>0:
				frame[int(list(frame.keys())[-1])+1] = containerImg
				# self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_width(),height= int(self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_height())+355)
				# self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_width(), height=int(self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_height())+355)
				# self.misframes['Repeticion'].camposEditables['totalFrame'][1].pack_propagate()
			else:
				frame[0] = containerImg
			containerIzquierda = tk.Frame(containerImg)
			containerIzquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
			containerCentro = tk.Frame(containerImg)
			containerCentro.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
			containerDerecha = tk.Frame(containerImg)
			containerDerecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
			frameContainerIn = []
			frameContainerIn.append(tk.Frame(containerIzquierda))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			frameContainerIn.append(tk.Frame(containerIzquierda))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			subtituloDatos = tk.Label(containerCentro, text="Datos de la imagen")
			subtituloDatos.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			subtituloDatos.config(font=('Courier', 16))
			self.misframes['Repeticion'].camposEditables['etapasubtitulo'] = tk.Label(containerCentro, text="Primero debe ingresar los datos de la imagen."); self.misframes['Repeticion'].camposEditables['etapasubtitulo'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['etapaLabel'] = tk.Label(containerCentro, text="¿A que etapa de la repetición pertenece la imagen?"); self.misframes['Repeticion'].camposEditables['etapaLabel'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['etapaEntry'] = tk.Entry(containerCentro); self.misframes['Repeticion'].camposEditables['etapaEntry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['etapaEntry'] .pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono1Label'] = tk.Label(containerCentro, text="Ingrese latitud cono uno."); self.misframes['Repeticion'].camposEditables['latitudCono1Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono1Entry'] = tk.Entry(containerCentro); self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono1Label'] = tk.Label(containerCentro, text="Ingrese longitud cono uno."); self.misframes['Repeticion'].camposEditables['longitudCono1Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono1Entry'] = tk.Entry(containerCentro); self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono2Label'] = tk.Label(containerCentro, text="Ingrese latitud cono dos."); self.misframes['Repeticion'].camposEditables['latitudCono2Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono2Entry'] = tk.Entry(containerCentro); self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono2Label'] = tk.Label(containerCentro, text="Ingrese longitud cono dos."); self.misframes['Repeticion'].camposEditables['longitudCono2Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono2Entry'] = tk.Entry(containerCentro); self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			datos = []
			nombre = 'Imagen ' + str(x)
			# nombre = 'Imagen ' + str(len(frame))
			nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
			nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			ensayoImage = Image.open(str(Path().absolute()) + '//Vistas//iconImage.png')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			self.misframes['Repeticion'].camposEditables['btnElegirImagen'] = tk.Button(containerCentro, text="Elegir imagen", command=lambda accion="new", : self.clickGuardoImagen(accion, frame, claveRepe, claveEnsayo, x, containerIzquierda, containerCentro, containerDerecha))
			# self.misframes['Repeticion'].camposEditables['btnElegirImagen'] = tk.Button(containerDerecha, text="Elegir imagen", command=lambda accion="new", : self.clickGuardoImagen(accion, frame, claveRepe, claveEnsayo, x, containerIzquierda, containerCentro, containerDerecha))
			self.misframes['Repeticion'].camposEditables['btnElegirImagen'].pack(side=tk.BOTTOM)
			# self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'] = tk.Button(derecha, text="Cancelar", command=lambda accion="update", : self.clickGuardoImagen(accion, frame, claveRepe, claveEnsayo, x, izquierda, centro, derecha, claveImagen))
			self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'] = tk.Button(containerDerecha, text="Cancelar", command=lambda accion="update", : containerImg.destroy())
			# self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'] = tk.Button(containerDerecha, text="Cancelar", command=lambda accion="update", : self.clickGuardoImagen(accion, frame, claveRepe, claveEnsayo, x, izquierda, centro, derecha, claveImagen))
			self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'].pack(side=tk.BOTTOM)

			# print("-----------------INFOOOOOO-------------------------")
			# print(self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_height())
			# print(self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_width())
			# print(containerImg.winfo_height())
			# print(containerImg.winfo_width())
			# print("-----------------INFOOOOOO-------------------------")
			if len(frame)==1:
				self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_width(),height= int(self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_height())+55)
				self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_width(), height=int(self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_height())+55)
			else:
				self.misframes['Repeticion'].camposEditables['totalFrame'][2].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_width(),height= int(self.misframes['Repeticion'].camposEditables['totalFrame'][2].winfo_height())+355)
				self.misframes['Repeticion'].camposEditables['totalFrame'][1].config(width=self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_width(), height=int(self.misframes['Repeticion'].camposEditables['totalFrame'][1].winfo_height())+355)

		else:

			for widget in izquierda.winfo_children():
				widget.pack_forget()
			for widget in centro.winfo_children():
				widget.pack_forget()
			for widget in derecha.winfo_children():
				widget.pack_forget()

			frameContainerIn = []
			frameContainerIn.append(tk.Frame(izquierda))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			frameContainerIn.append(tk.Frame(izquierda))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			subtituloDatos = tk.Label(centro, text="Datos de la imagen"); subtituloDatos.pack(side=tk.TOP, padx=5, pady=5, expand=True); subtituloDatos.config(font=('Courier', 16))
			self.misframes['Repeticion'].camposEditables['etapasubtitulo'] = tk.Label(centro, text="Primero debe ingresar los datos de la imagen."); self.misframes['Repeticion'].camposEditables['etapasubtitulo'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['etapaLabel'] = tk.Label(centro, text="¿A que etapa de la repetición pertenece la imagen?"); self.misframes['Repeticion'].camposEditables['etapaLabel'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['etapaEntry'] = tk.Entry(centro); self.misframes['Repeticion'].camposEditables['etapaEntry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['etapaEntry'] .pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono1Label'] = tk.Label(centro, text="Ingrese latitud cono uno."); self.misframes['Repeticion'].camposEditables['latitudCono1Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono1Entry'] = tk.Entry(centro); self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono1Label'] = tk.Label(centro, text="Ingrese longitud cono uno."); self.misframes['Repeticion'].camposEditables['longitudCono1Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono1Entry'] = tk.Entry(centro); self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono2Label'] = tk.Label(centro, text="Ingrese latitud cono dos."); self.misframes['Repeticion'].camposEditables['latitudCono2Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['latitudCono2Entry'] = tk.Entry(centro); self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono2Label'] = tk.Label(centro, text="Ingrese longitud cono dos."); self.misframes['Repeticion'].camposEditables['longitudCono2Label'].pack(side=tk.TOP, fill=tk.X, expand=True)
			self.misframes['Repeticion'].camposEditables['longitudCono2Entry'] = tk.Entry(centro); self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].insert(0, ' '); self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].pack(side=tk.TOP, fill=tk.X, expand=True)
			datos = []
			nombre = 'Imagen ' + str(x)
					# nombre = 'Imagen ' + str(len(frame))
			nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
			nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			ensayoImage = Image.open(str(Path().absolute()) + '//Vistas//iconImage.png')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			self.misframes['Repeticion'].camposEditables['btnElegirImagen'] = tk.Button(centro, text="Elegir imagen", command=lambda accion="update", : self.clickGuardoImagen(accion, frame, claveRepe, claveEnsayo, x, izquierda, centro, derecha, claveImagen))
					# self.misframes['Repeticion'].camposEditables['btnElegirImagen'] = tk.Button(derecha, text="Elegir imagen", command=lambda accion="update", : self.clickGuardoImagen(accion, frame, claveRepe, claveEnsayo, x, izquierda, centro, derecha, claveImagen))
			self.misframes['Repeticion'].camposEditables['btnElegirImagen'].pack(side=tk.BOTTOM)
			self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'] = tk.Button(derecha, text="Cancelar", command=lambda claveImg=claveImagen, : self.cancelarNewImage(claveImg, x, derecha, centro, izquierda))
			self.misframes['Repeticion'].camposEditables['btnElegirImagenCancelar'].pack(side=tk.BOTTOM)
					#Busco el objeto imagen y me quedo con el para editarlo y despues guardarlo.

			#######################################################################
			#######################################################################
			#######################################################################
	def cancelarNewImage(self, claveImg, x, derecha, centro, izquierda):
		imagen = CD.buscar_objetos("Imagen", {'clave' : claveImg})[0]
		print("---------CANCELANDO----------")
		print(claveImg)
		print(imagen)
		print("---------CANCELANDO----------")
		# imagen = CD.buscar_objetos("Imagen", {'clave' : claveImg})[0]
		repeticion = CD.buscar_objetos('Repeticion', {'clave' : imagen.id_repeticiones})[0]

		for widget in izquierda.winfo_children():
			widget.pack_forget()
			# widget.destroy()
		for widget in centro.winfo_children():
			widget.pack_forget()
			# widget.destroy()
		for widget in derecha.winfo_children():
			widget.pack_forget()
			# widget.destroy()

		frameContainerIn = []
		frameContainerIn.append(tk.Frame(izquierda))
		frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
		frameContainerIn.append(tk.Frame(izquierda))
		frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

		btnCambiarImagen = tk.Button(derecha, text="Cambiar imagen", command=lambda accion="update", frameArg=self.misframes['Repeticion'].camposEditables['imagenesRepeticion'], claveRepeArg=imagen.id_repeticiones, claveEnsayoArg=repeticion.id_ensayos, y=x+1, izquierda=izquierda, centro=centro, derecha=derecha, claveImagen=imagen.clave: self.cambiarImagen(accion, frameArg, claveRepeArg, claveEnsayoArg, y, izquierda, centro, derecha, claveImagen))
		btnCambiarImagen.pack(side=tk.TOP)
		btnAnalizarImagen = tk.Button(derecha, text="Analizar imagen", command=lambda image=imagen: self.iniciarAnalisis(image))
		btnAnalizarImagen.pack(side=tk.TOP)
		btnBorrarImagen = tk.Button(derecha, text="Borrar", command=lambda image=imagen, frame=self.misframes['Repeticion'].camposEditables['imagenesRepeticion']: self.borrarImagen(image, frame))
		btnBorrarImagen.pack(side=tk.BOTTOM)

		subtituloDatos = tk.Label(centro, text="Datos de la imagen")
		subtituloDatos.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		subtituloDatos.config(font=('Courier', 16))

		etapa = tk.Label(centro, text="Etapa : " + str(imagen.etapa)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		ancho = tk.Label(centro, text="Ancho(Pixels) : " + str(imagen.ancho) + " Largo(Pixels) : " + str(imagen.largo)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		altitud = tk.Label(centro, text="Altitud : " + str(imagen.altitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		latitud = tk.Label(centro, text="Lat y Lnt de la imagen : " + str(imagen.latitud) + " " + str(imagen.longitud)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		latitudCono1 = tk.Label(centro, text="Lat y Lnt del cono 1 : " + str(imagen.latitudCono1) + " " + str(imagen.longitudCono1)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		latitudCono2 = tk.Label(centro, text="Lat y Lnt del cono 2 : " + str(imagen.latitudCono2) + " " + str(imagen.longitudCono2)).pack(side=tk.TOP, padx=5, pady=5, expand=True)
		datos = []
		nombre = 'Imagen ' + str(x)
		nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
		nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		fechalabel = tk.Label(frameContainerIn[0], text=imagen.fecha)
		fechalabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		path = str(Path().absolute())
		try:
			ensayoImage = Image.open(imagen.url)
		except:
			ensayoImage = Image.open(path + '\\Vistas\\notFound.jpg')
		ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(ensayoImage)
		label = tk.Label(frameContainerIn[1], image=photo)
		label.image = photo
		label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
		datos.append(label)
		datos.append(nombrelabel)
		datos.append(fechalabel)
		# fotosRepeticion.append(datos)



	def verAnalisis(self):
		self.visorAnalisis = VisorResultados(self.misframes['Analisis'].interior, self)

	def iniciarAnalisis(self, imagen):
		self.visorAnalisis.Analisis(imagen)
		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Analisis'])

	def updateFrameEnsayo(self, ensayo):

		def exportar(clave):
			print('Exportando CSV y KML para el ensayo.clave={}'.format(clave))
			CD.exportar_informe_csv(clave)
			CD.exportar_informe_kml(clave)
			# path="C:/Users"
			path=CD.out
			path=os.path.realpath(path)
			os.startfile(path)

		for x in range(0, len(self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'])):
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].pack_forget()
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].destroy()

		self.misframes['Ensayo'].camposEditables['ensayoClave'] = ensayo.clave
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'].config(text='Ensayo N° ' + str(ensayo.nro),font=('Courier', 33))
		self.updateEntry(self.misframes['Ensayo'].camposEditables['numEnsayo'], ensayo.nro)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['numRepeticiones'], ensayo.nroRepeticiones)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['establecimiento'], ensayo.establecimiento)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['numCuadro'], ensayo.nroCuadro)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['suelo'], ensayo.suelo)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['espaciamiento'], ensayo.espaciamientoX +' X '+ ensayo.espaciamientoY)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['plantasXha'], ensayo.plantasHa)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['fechaPlantacion'], ensayo.fechaPlantacion)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['numTratamientos'], ensayo.nroTratamientos)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['totalPlantas'], ensayo.totalPlantas)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['totalHas'], ensayo.totalHas)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['plantasXparcela'], ensayo.plantasParcela)
		self.updateEntry(self.misframes['Ensayo'].camposEditables['tipoClonal'], ensayo.tipoClonal)
		self.misframes['Ensayo'].camposEditables['btnExportar'].config(command = lambda: exportar(ensayo.clave))
		self.misframes['Ensayo'].camposEditables['btnExportar'].pack()

		print("Antes de buscar la repeticionne: ", ensayo.clave)
		repes = CD.buscar_objetos('Repeticion', {'id_ensayos' : ensayo.clave})
		print("Despues que busco: ", repes, "Largo: ", len(repes))
		if len(repes) > 0:
			print("Entro al for de las repes")
			for x in range(0, len(repes)):
				label = tk.Label(self.misframes['Ensayo'].camposEditables['frameContainer'][-2], text='Repetición '+str(x+1), relief="solid", borderwidth=2)
				label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
				label.bind("<Leave>", lambda event, esteLabel=label :esteLabel.config(relief="solid", bd=1))
				label.bind("<Enter>", lambda event, esteLabel=label :esteLabel.config(relief="raised", bd=8))
				label.bind("<Button-1>", lambda event, repe=repes[x], nroRepes=ensayo.nroRepeticiones:self.clickVerRepeticion(repe, nroRepes, ensayo.nro, event))

				self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x] = label
			# self.misframes['Ensayo'].camposEditables['btnAgregarRepeticion'].pack_forget()
		else:
			self.misframes['Ensayo'].camposEditables['btnAgregarRepeticion'].pack()


	def clickBtnAgregarRepeticion(self):
		print("------AGREGAR REPETICION~!!!!!!!!!!!!!!!!!!!!!!!!!!------------------------")
		self.updateFrameRepeticion()
		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Repeticion'])

	def updateEntry(self, entry, text):
		entry.config(state=tk.NORMAL)
		entry.delete(0, tk.END)
		entry.insert(0, text)
		entry.config(state=tk.DISABLED)

	def clickBtnModificar(self, accion, tipo):
		datosParaGuardar = {}
		if accion == 'Modificar':
			self.misframes['Ensayo'].camposEditables['numEnsayo'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['establecimiento'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['numCuadro'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['suelo'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['espaciamiento'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['plantasXha'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['fechaPlantacion'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['numTratamientos'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['totalPlantas'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['totalHas'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['plantasXparcela'].config(state=tk.NORMAL, background="#fff")
			self.misframes['Ensayo'].camposEditables['tipoClonal'].config(state=tk.NORMAL, background="#fff")
			if tipo != "Nuevo":
				self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].config(text='Guardar', command= lambda: self.clickBtnModificar('Guardar', 'Actualizar'))
			else:
				self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].config(text='Guardar', command= lambda: self.clickBtnModificar('Guardar', 'Nuevo'))

		else:
			checkSave = []
			if tipo != "Nuevo":
				datosParaGuardar['ensayoClave'] = self.misframes['Ensayo'].camposEditables['ensayoClave']
			datosParaGuardar['numEnsayo'] = self.misframes['Ensayo'].camposEditables['numEnsayo'].get()
			self.misframes['Ensayo'].camposEditables['numEnsayo'].config(state=tk.DISABLED)
			datosParaGuardar['numRepeticiones'] = self.misframes['Ensayo'].camposEditables['numRepeticiones'].get()
			self.misframes['Ensayo'].camposEditables['numRepeticiones'].config(state=tk.DISABLED, )
			datosParaGuardar['establecimiento'] = self.misframes['Ensayo'].camposEditables['establecimiento'].get()
			self.misframes['Ensayo'].camposEditables['establecimiento'].config(state=tk.DISABLED)
			datosParaGuardar['numCuadro'] = self.misframes['Ensayo'].camposEditables['numCuadro'].get()
			self.misframes['Ensayo'].camposEditables['numCuadro'].config(state=tk.DISABLED)
			datosParaGuardar['suelo'] = self.misframes['Ensayo'].camposEditables['suelo'].get()
			self.misframes['Ensayo'].camposEditables['suelo'].config(state=tk.DISABLED)
			datosParaGuardar["espaciamientoSplit"] = self.misframes['Ensayo'].camposEditables['espaciamiento'].get()
			# espaciamientoSplit = self.misframes['Ensayo'].camposEditables['espaciamiento'].get().split(" X ")
			# datosParaGuardar['espaciamientoX'] = espaciamientoSplit[0]
			# datosParaGuardar['espaciamientoY'] = espaciamientoSplit[1]
			datosParaGuardar['espaciamientoX'] = ""
			datosParaGuardar['espaciamientoY'] = ""
			self.misframes['Ensayo'].camposEditables['espaciamiento'].config(state=tk.DISABLED)
			datosParaGuardar['plantasXha'] = self.misframes['Ensayo'].camposEditables['plantasXha'].get()
			self.misframes['Ensayo'].camposEditables['plantasXha'].config(state=tk.DISABLED)
			datosParaGuardar['fechaPlantacion'] = self.misframes['Ensayo'].camposEditables['fechaPlantacion'].get()
			self.misframes['Ensayo'].camposEditables['fechaPlantacion'].config(state=tk.DISABLED)
			datosParaGuardar['numTratamientos'] = self.misframes['Ensayo'].camposEditables['numTratamientos'].get()
			self.misframes['Ensayo'].camposEditables['numTratamientos'].config(state=tk.DISABLED)
			datosParaGuardar['totalPlantas'] = self.misframes['Ensayo'].camposEditables['totalPlantas'].get()
			self.misframes['Ensayo'].camposEditables['totalPlantas'].config(state=tk.DISABLED)
			datosParaGuardar['totalHas'] = self.misframes['Ensayo'].camposEditables['totalHas'].get()
			self.misframes['Ensayo'].camposEditables['totalHas'].config(state=tk.DISABLED)
			datosParaGuardar['plantasXparcela'] = self.misframes['Ensayo'].camposEditables['plantasXparcela'].get()
			self.misframes['Ensayo'].camposEditables['plantasXparcela'].config(state=tk.DISABLED)
			datosParaGuardar['tipoClonal'] = self.misframes['Ensayo'].camposEditables['tipoClonal'].get()
			self.misframes['Ensayo'].camposEditables['tipoClonal'].config(state=tk.DISABLED)
			self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].config(text='Modificar', command= lambda: self.clickBtnModificar('Modificar', 'Actualizar'))

			checkeo = self.checkearCamposEnsayo(datosParaGuardar)
			if not checkeo:
				espaciamientoSplit = datosParaGuardar["espaciamientoSplit"].lower().replace(" ","").split("x")
				datosParaGuardar['espaciamientoX'] = espaciamientoSplit[0]
				datosParaGuardar['espaciamientoY'] = espaciamientoSplit[1]
				self.guardarEnsayo(datosParaGuardar, tipo)
			else:
				messagebox.showinfo("Error", "Controle el formato de datos ingresado y que no haya campos vacios e intente nuevamente.")
				# self.clickBtnModificar('Modificar', tipo)
				if tipo != "Nuevo":
					self.clickBtnModificar('Modificar', 'Actualizar')
				else:
					self.clickBtnModificar('Modificar', 'Nuevo')
				for x in checkeo:
					self.misframes['Ensayo'].camposEditables[x].config(state=tk.NORMAL, background="#ff8282")
					

	def checkearCamposDatosImagen(self):
		check = []
		
		try:
			if int(self.misframes['Repeticion'].camposEditables['etapaEntry'].get()) < 0:
				check.append('etapaEntry')
			if not self.misframes['Repeticion'].camposEditables['etapaEntry'].get() or self.misframes['Repeticion'].camposEditables['etapaEntry'].get().isspace():
				check.append('etapaEntry')
		except:
			check.append('etapaEntry')
		
		try:
			float(self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].get())
			if not self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].get() or self.misframes['Repeticion'].camposEditables['latitudCono1Entry'].get().isspace():
				check.append('latitudCono1Entry')
		except:
			check.append('latitudCono1Entry')
		try:
			float(self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].get())
			if not self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].get() or self.misframes['Repeticion'].camposEditables['longitudCono1Entry'].get().isspace():
				check.append('longitudCono1Entry')
		except:
			check.append('longitudCono1Entry')
		try:
			float(self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].get())
			if not self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].get() or self.misframes['Repeticion'].camposEditables['latitudCono2Entry'].get().isspace():
				check.append('latitudCono2Entry')
		except:
			check.append('latitudCono2Entry')
		try:
			float(self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].get())
			if not self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].get() or self.misframes['Repeticion'].camposEditables['longitudCono2Entry'].get().isspace():
				check.append('longitudCono2Entry')
		except:
			check.append('longitudCono2Entry')
		return check

	def checkearCamposEnsayo(self, datosParaGuardar):
		check = []
		try:
			if int(datosParaGuardar['numEnsayo']) < 0:
				check.append('numEnsayo')
			if not datosParaGuardar['numEnsayo']:
				check.append('numEnsayo')
		except:
			check.append('numEnsayo')
		try:
			if int(datosParaGuardar['numRepeticiones']) < 1:
				check.append('numRepeticiones')
		except:
			check.append('numRepeticiones')
		if datosParaGuardar['establecimiento'] == "" or  datosParaGuardar['establecimiento'].isspace():
			check.append('establecimiento')
		if not datosParaGuardar['numCuadro'] or datosParaGuardar['numCuadro'].isspace():
			check.append('numCuadro')
		try:
			float(datosParaGuardar['suelo'])
		except:
			check.append('suelo')
		try:
			espaciamientoSplit = datosParaGuardar["espaciamientoSplit"].lower().split('x')
			if float(espaciamientoSplit[0]) <= 0:
				check.append('espaciamiento')
			if float(espaciamientoSplit[1]) <=0:
				check.append('espaciamiento')
		except:
			check.append('espaciamiento')
		try:
			if int(datosParaGuardar['plantasXha']) < 0:
				check.append('plantasXha')
		except:
			check.append('plantasXha')
		if not validate(datosParaGuardar['fechaPlantacion']):
			check.append('fechaPlantacion')
		try:
			if int(datosParaGuardar['numTratamientos']) < 1:
				check.append('numTratamientos')
		except:
			check.append('numTratamientos')
		try:
			if int(datosParaGuardar['totalPlantas']) < 1:
				check.append('totalPlantas')
		except:
			check.append('totalPlantas')
		try:
			if float(datosParaGuardar['totalHas']) < 0:
				check.append('totalHas')
		except:
			check.append('totalHas')
		try:
			if int(datosParaGuardar['plantasXparcela']) < 1:
				check.append('plantasXparcela')
		except:
			check.append('plantasXparcela')
		if not datosParaGuardar['tipoClonal'] or datosParaGuardar['tipoClonal'].isspace():
			check.append('tipoClonal')
		return check




	def guardarEnsayo(self, datosParaGuardar, tipo):
		if tipo == "Nuevo":
			ensayo = CD.crear_objeto('Ensayo')
		else:
			ensayo = CD.buscar_objetos('Ensayo', {'Clave' : datosParaGuardar['ensayoClave']})[0]
		
		print(ensayo)
		
		ensayo.nro = datosParaGuardar['numEnsayo']
		ensayo.nroRepeticiones = datosParaGuardar['numRepeticiones']
		ensayo.establecimiento = datosParaGuardar['establecimiento']
		ensayo.nroCuadro = datosParaGuardar['numCuadro']
		ensayo.suelo = datosParaGuardar['suelo']
		ensayo.espaciamientoX = datosParaGuardar['espaciamientoX']
		ensayo.espaciamientoY = datosParaGuardar['espaciamientoY' ]
		ensayo.plantasHa = datosParaGuardar['plantasXha']
		ensayo.fechaPlantacion = datosParaGuardar['fechaPlantacion']
		ensayo.nroTratamientos = datosParaGuardar['numTratamientos']
		ensayo.totalPlantas = datosParaGuardar['totalPlantas']
		ensayo.totalHas = datosParaGuardar['totalHas']
		ensayo.plantasParcela = datosParaGuardar['plantasXparcela']
		ensayo.tipoClonal =datosParaGuardar['tipoClonal']
		# print(ensayo)
		try:
			guardado = ensayo.guardar(CD.db)
		except Exception:
			messagebox("Error", "Ha ocurrido un error al guardar. Intente mas tarde.")
			return

		messagebox.showinfo("Info", "Se ha guardado correctamente") # if guardado else messagebox("Error", "Ha ocurrido un error al guardar. Intente mas tarde.")

		self.misframes['Ensayo'].camposEditables['tituloEnsayo'].config(text="Ensayo N° "+str(ensayo.nro))
		self.misframes['Ensayo'].camposEditables['ensayoClave'] = ensayo.clave
		#Si es nuevo creao tantas repeticiones vacias como diga el nro de repeticiones
		if tipo == "Nuevo":
			for x in range(0, int(guardado.nroRepeticiones)):
				new = CD.crear_objeto('Repeticion')
				new.nro = str(x + 1); new.nroFilas = ' '; new.nroColumnas = ' '; new.id_ensayos = guardado.clave
				new.guardar(CD.db) 

		# Actulizar numRepeticion
		for x in range(0, len(self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'])):
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].pack_forget()
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].destroy()

		repes = CD.buscar_objetos('Repeticion', {'id_ensayos' : ensayo.clave})

		for x in range(0, len(repes)):
			label = tk.Label(self.misframes['Ensayo'].camposEditables['frameContainer'][-2], text='Repetición '+str(x+1), relief="solid", borderwidth=2)
			label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			# label.bind("<Leave>", lambda event, :label.config(relief="solid", bd=1))
			label.bind("<Leave>", lambda event, esteLabel=label :esteLabel.config(relief="solid", bd=1))
			label.bind("<Enter>", lambda event, esteLabel=label :esteLabel.config(relief="raised", bd=8))
			# label.bind("<Button-1>", lambda event, arg=repes[x]:self.clickVerRepeticion(event,arg))
			label.bind("<Button-1>", lambda event, repe=repes[x], nroRepes=guardado.nroRepeticiones:self.clickVerRepeticion(repe, nroRepes, ensayo.nro, event))

			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x] = label



class DoubleScrollbarFrame(ttk.Frame):

	def __init__(self, master, **kwargs):
	    ttk.Frame.__init__(self,  master, **kwargs)
	    # Canvas creation with double scrollbar
	    self.hscrollbar = ttk.Scrollbar(self, orient = tk.HORIZONTAL)
	    self.vscrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL)
	    self.sizegrip = ttk.Sizegrip(self)
	    self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand = self.vscrollbar.set, xscrollcommand = self.hscrollbar.set)
	    self.vscrollbar.config(command = self.canvas.yview)
	    self.hscrollbar.config(command = self.canvas.xview)

	def pack(self, **kwargs):
		self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.FALSE)
		self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y,  expand=tk.FALSE)
		self.sizegrip.pack(in_ = self.hscrollbar, side = tk.BOTTOM, anchor = "se")
		self.canvas.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=tk.TRUE)

		ttk.Frame.pack(self, **kwargs)
    


	def get_frame(self):
		'''
		Return the "frame" useful to place inner controls.
		'''
		return self.canvas


class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
        # create a canvas object and a vertical scrollbar for scrolling it
        self.nameFrame = ""
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        # self.interior.Ensayos pack(side=tk.TOP)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        self.camposEditables = {}
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
    def get_name(self):
    	return self.nameFrame

    def set_name(self, nameFrame):
    	self.nameFrame = nameFrame

class mainInicio(object):
	"""docstring for mainInicio"""
	def __init__(self, ensayosRecientes, todosLosEnsayos):
		super(mainInicio, self).__init__()
		self.miapp = Inicio(ensayosRecientes, todosLosEnsayos)



def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        # raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return False

	# @property
	# def miapp(self):
	# 	return self._miapp

	# @miapp.setter
	# def miapp(self, value):
	# 	self._miapp = value

	# @miapp.deleter
	# def miappy(self):
	# 	del self._miapp
		

# class mainInicio(object):

	# mi_app = Inicio(ensayosRecientes)
	# def mi_app(self, ensayosRecientes):



# if __name__ == '__main__':
# 	main()
