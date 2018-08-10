import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import cgitb
from inspect import getmembers
from pprint import pprint
import random
from Vistas.esquemaParcelas import esquemaParcelas
from Vistas.AbrirEnsayo import AbrirEnsayo
# from app.ControladorTotal import 

actualFrame = 1
def donothing():
	print("donothing")

car_list = [
('Hyundai', 'brakes', 'Uruguay') ,
('Honda', 'light', 'Brasil') ,
('Lexus', 'battery', 'Uruguay') ,
('Benz', 'wiper', 'Uruguay') ,
('Ford', 'tire', 'India') ,
('Chevy', 'air','Mexico') ,
('Chrysler', 'piston', 'India') ,
('Toyota', 'brake pedal', 'Chile') ,
('BMW', 'seat', 'Italia')
]
# def dounpack(frame):
# 	frame.pack_forget()
# 	print("forget")



# class Menu():
# 	def __init__(self, root):
# 		self.filemenu = tk.Menu(root)
# 		self.filemenu.add_command(label="New", command=donothing)
# 		self.filemenu.add_command(label="Exit", command=donothing)

class Inicio(object):
	def __init__(self, misEnsayosRecientes, todosLosEnsayos):
		self.misEnsayosRecientes = misEnsayosRecientes
		self.todosLosEnsayos = todosLosEnsayos
		self.root = tk.Tk()
		self.root.geometry("1280x768")
		self.root.title("TreePy Analisis de Imagenes")
		self.root.state('zoomed')
		self.frameActivo = "Inicio"

		misframes = ['Inicio', 'Ensayo', 'Repeticion', 'Analisis', 'ListaEnsayos']
		self.misframes = self.generarFrames(misframes)
		self.misframes['Inicio'].pack(fill=tk.BOTH, padx=0, pady=0, expand=True)

		self.ensayosRecientes(self.misEnsayosRecientes)
		self.verEnsayo()
		self.verRepeticion()

		self.root.config(menu=self.mimenu(self.root))
		self.root.mainloop()

	def verRepeticion(self):
		totalFrame, frameContainer = [], []

		totalFrame.append(tk.Frame(self.misframes['Repeticion'].interior))
		totalFrame[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Repeticion'].interior))
		totalFrame[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Repeticion'].interior))
		totalFrame[-1].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		frameContainer.append(tk.Frame(totalFrame[0]))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		tituloRepeticion = tk.Label(frameContainer[-1], text='Repeticion X')
		tituloRepeticion.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		tituloRepeticion.config(font=('Courier', 33))

		frameContainer.append(tk.Frame(totalFrame[1], height=100, background="bisque"))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH)
		frameContainer[-1].pack_propagate(0)
		# frameContainer[-1].place(relx=.5, rely=.5, anchor="c")
		# frameContainer[-1].config(height=5)

		subtituloEsquema = tk.Label(frameContainer[-1], text='Esquema de parcelas')
		subtituloEsquema.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		subtituloEsquema.config(font=('Courier', 22))
		# subtituloEsquema.config(height=5)

		frameContainer.append(tk.Frame(totalFrame[2]))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		subtituloImagenes = tk.Label(frameContainer[-1], text='Imagenes')
		subtituloImagenes.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		subtituloImagenes.config(font=('Courier', 22))

		# cargo el frame de esquema parcelas
		frameesquema = esquemaParcelas(totalFrame[1])
		frameesquema.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		# 

		# cargo la imagenes de la repeticion
		for x in range(0, 3):
			fotosRepeticion = []
			frameContainerIn = []
			frameContainerIn.append(tk.Frame(totalFrame[2]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			frameContainerIn.append(tk.Frame(totalFrame[2]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

			datos = []
			nombre = 'Imagen ' + str(x)
			nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
			nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			ensayoImage = Image.open('Vistas/arboles_00.jpg')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			fotosRepeticion.append(datos)
			label.bind("<Button-1>", lambda event, arg=x:self.clickEnsayoReciente(event,arg))
			# label.bind("<Button-1>", self.clickEnsayoReciente(self,datos[1]["text"]))
			if len(fotosRepeticion) % 3 ==0:
				print("salto imegen repe")
				# rand = random.choice(colores)
				frameContainer.append(tk.Frame(totalFrame[2]))
				frameContainer[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		#####



	def verEnsayo(self):
		# Creo todos los campos del frame "Ver Ensayo" 
		print('émpieza ver ensayo')

		# camposEditables = {}
		# claveEnsayo = ensayo.clave
		totalFrame = []
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


		frameContainer = []
		frameContainer.append(tk.Frame(totalFrame[0]))
		frameContainer[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

		tituloEnsayo = 'Ensayo Nro 2131'
		# camposEditables['titulo'] = tk.Label(frameContainer[-1], text=tituloEnsayo)
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'] = tk.Label(frameContainer[-1], text=tituloEnsayo)
		# camposEditables['titulo'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.misframes['Ensayo'].camposEditables['numRepeticiones'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Repeticiones: ', '3')
		self.misframes['Ensayo'].camposEditables['establecimiento'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Establecimento: ', 'La Tribu')
		self.misframes['Ensayo'].camposEditables['numCuadro'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Cuadro: ', 'H007')
		self.misframes['Ensayo'].camposEditables['suelo'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Suelo: ', '9.3')
		self.misframes['Ensayo'].camposEditables['espaciamiento'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Espaciamiento: ', '4 X 1.9')
		self.misframes['Ensayo'].camposEditables['plantasXha'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Plantas/Ha: ', '1315')
		self.misframes['Ensayo'].camposEditables['fechaPlantacion'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Fecha de plantacion: ', '15/09/2017')
		self.misframes['Ensayo'].camposEditables['numTratamientos'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Tratamientos: ', '27')
		self.misframes['Ensayo'].camposEditables['totalPlantas'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Total de plantas: ', '1620')
		self.misframes['Ensayo'].camposEditables['totalHas'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Total Has: ', '1.23')
		self.misframes['Ensayo'].camposEditables['plantasXparcela'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Plantas por parcela: ', '20')
		self.misframes['Ensayo'].camposEditables['tipoClonal'] = self.frameCreateCampo(frameContainer, totalFrame[0], 'Clonal: ', 'T2')

		frameContainer.append(tk.Frame(totalFrame[1]))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		tituloRepeticiones = 'Repeticiones'
		self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'] = tk.Label(frameContainer[-1], text='Repeticiones')
		# tituloRepeticiones = tk.Label(frameContainer[-1], text='Repeticiones')
		self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'].config(font=("Courier",33))

		self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'] = {}

		totalRepeticiones = '3'
		for x in range(0, int(totalRepeticiones)):
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x] = tk.Label(frameContainer[-1], text='Repeticion '+str(x+1))
			# labelRepeticion = tk.Label(frameContainer[-1], text='Repeticion '+str(x+1))
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			# labelRepeticion.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			self.misframes['Ensayo'].camposEditables['todasLasRepeticiones'][x].bind("<Button-1>", lambda event, arg='Repeticion '+ str(x+1):self.clickVerRepeticion(event,arg))
			# labelRepeticion.bind("<Button-1>", lambda event, arg='Repeticion '+ str(x+1):self.clickVerRepeticion(event,arg))

		frameContainer.append(tk.Frame(totalFrame[1]))
		frameContainer[-1].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
		self.misframes['Ensayo'].camposEditables['btnExportar'] = tk.Button(frameContainer[-1], text="Exportar", command=lambda: donothing)
		self.misframes['Ensayo'].camposEditables['btnExportar'].pack(side=tk.RIGHT, fill=tk.X)
		self.misframes['Ensayo'].camposEditables['btnModificarGuardar'] = tk.Button(frameContainer[-1], text="Modificar", command=lambda: self.clickBtnModificar('Modificar'))
		self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].pack(side=tk.RIGHT, fill=tk.X)


	def frameCreateCampo(self, frameContainer, parent, textLabel, textDato):
		frameContainer.append(tk.Frame(parent))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		label = tk.Label(frameContainer[-1], text=textLabel).pack(side=tk.LEFT, fill=tk.BOTH)
		entry = self.createCampo(frameContainer[-1], textDato)
		# return [label, entry]
		return entry

	def createCampo(self, frameContainer, texto):
		entry = tk.Entry(frameContainer)
		entry.insert(0, texto)
		entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
		entry.config(state=tk.DISABLED)
		return entry

	def ensayosRecientes(self, ensayosRecientes):
		fotosEnsayos = []
		frameContainer=[]
		# colores = ['blue', 'red', 'green','black', 'yellow', 'white']
		# rand = random.choice(colores)

		labelTitulo = ttk.Label(self.misframes['Inicio'].interior, text='Ensayos Recientes')
		labelTitulo.pack(side=tk.TOP, fill=tk.BOTH)
		labelTitulo.config(font=("Courier", 33))
		frameContainer.append(tk.Frame(self.misframes['Inicio'].interior))
		# frameContainer[-1].geometry("175x75")
		frameContainer[-1].pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

		# for x in range(1,10):
		for ensayo in ensayosRecientes:
			frameContainerIn = []
			frameContainerIn.append(tk.Frame(frameContainer[-1]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			frameContainerIn.append(tk.Frame(frameContainer[-1]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

			datos = []
			nombre = 'Ensayo' + str(ensayo.clave) + ' ' + str(ensayo.establecimiento)
			nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
			nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			ensayoImage = Image.open('Vistas/Image.png')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			fotosEnsayos.append(datos)
			label.bind("<Button-1>", lambda event, arg=ensayo:self.clickEnsayoReciente(event,arg))
			# label.bind("<Button-1>", self.clickEnsayoReciente(self,datos[1]["text"]))
			if len(fotosEnsayos) % 3 ==0:
				print("salto")
				# rand = random.choice(colores)
				frameContainer.append(tk.Frame(self.misframes['Inicio'].interior))
				frameContainer[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		return fotosEnsayos

	def mimenu(self, root):
		MENU = tk.Menu(root)	

		menu_archivo = tk.Menu(MENU, tearoff=0)
		menu_edicion = tk.Menu(MENU, tearoff=0)
		menu_vista = tk.Menu(MENU, tearoff=0)
		menu_ayuda = tk.Menu(MENU, tearoff=0)

		menu_archivo.add_command(label="Nuevo ensayo", command=donothing)
		menu_archivo.add_command(label="Abrir ensayo", command= lambda:self.AbrirEnsayo(self.misframes['ListaEnsayos'], self.todosLosEnsayos))
		# menu_archivo.add_command(label="Abrir ensayo", command=AbrirEnsayo(self.root))
		menu_archivo.add_separator()
		menu_archivo.add_command(label="Salir", command=root.quit)

		menu_edicion.add_command(label="Editar Ensayo", command=lambda:self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo']))
		menu_edicion.add_command(label="Editar Repeticion", command=lambda:self.raise_frame(self.misframes[self.frameActivo], self.misframes['Repeticion']))

		menu_ayuda.add_command(label="Documentacion", command=donothing)
		menu_ayuda.add_command(label="Acerca de", command=donothing)

		MENU.add_cascade(label="Archivo", menu=menu_archivo)
		MENU.add_cascade(label="Edicion", menu=menu_edicion)
		MENU.add_cascade(label="Vista", menu=menu_vista)
		MENU.add_cascade(label="Ayuda", menu=menu_ayuda)
		
		return MENU

	def AbrirEnsayo(self, frameEnsayo, todosLosEnsayos):
		frameEnsayo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		ok = AbrirEnsayo(frameEnsayo, todosLosEnsayos)
		# ok.listaDeEnsayos.build_tree(car_list)
		self.raise_frame(self.misframes[self.frameActivo], frameEnsayo)

	def generarFrames(self, misframes):
		framesGenerados = {}
		for x in misframes:
			frame = VerticalScrolledFrame(self.root)
			frame.set_name(x)
			framesGenerados[x]=frame

		return framesGenerados

	def raise_frame(self, frame, newframe):
	    # frame.tkraise()
	    frame.pack_forget()
	    newframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	    self.frameActivo = newframe.get_name()
	    print("raise")

	def clickVerRepeticion(self, event, nombre):
		print("Click REPE")
		print(nombre)
		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Repeticion'])

	def clickEnsayoReciente(self, event, ensayo):
		print("Click izquierdo")
		print(ensayo.tipoClonal)
		self.updateFrameEnsayo(ensayo)
		# self.misframes['Ensayo'].camposEditables['tituloRepeticionesRight'].config(text='change the value')

		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo'])

	def updateFrameEnsayo(self, ensayo):

		self.misframes['Ensayo'].camposEditables['ensayoClave'] = ensayo.clave
		self.misframes['Ensayo'].camposEditables['tituloEnsayo'].config(text='Ensayoooo N° ' + str(ensayo.clave))
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

	def updateEntry(self, entry, text):
		entry.config(state=tk.NORMAL)
		entry.delete(0, tk.END)
		entry.insert(0, text)
		entry.config(state=tk.DISABLED)

	def clickBtnModificar(self, accion):
		datosParaGuardar = {}
		if accion == 'Modificar':
			self.misframes['Ensayo'].camposEditables['numRepeticiones'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['establecimiento'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['numCuadro'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['suelo'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['espaciamiento'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['plantasXha'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['fechaPlantacion'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['numTratamientos'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['totalPlantas'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['totalHas'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['plantasXparcela'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['tipoClonal'].config(state=tk.NORMAL)
			self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].config(text='Guardar', command= lambda: self.clickBtnModificar('Guardar'))
		else:
			datosParaGuardar['numRepeticiones'] = self.misframes['Ensayo'].camposEditables['numRepeticiones'].get()
			self.misframes['Ensayo'].camposEditables['numRepeticiones'].config(state=tk.DISABLED)
			datosParaGuardar['establecimiento'] = self.misframes['Ensayo'].camposEditables['establecimiento'].get()
			self.misframes['Ensayo'].camposEditables['establecimiento'].config(state=tk.DISABLED)
			datosParaGuardar['numCuadro'] = self.misframes['Ensayo'].camposEditables['numCuadro'].get()
			self.misframes['Ensayo'].camposEditables['numCuadro'].config(state=tk.DISABLED)
			datosParaGuardar['suelo'] = self.misframes['Ensayo'].camposEditables['suelo'].get()
			self.misframes['Ensayo'].camposEditables['suelo'].config(state=tk.DISABLED)
			datosParaGuardar['espaciamiento'] = self.misframes['Ensayo'].camposEditables['espaciamiento'].get()
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
			self.misframes['Ensayo'].camposEditables['btnModificarGuardar'].config(text='Modificar', command= lambda: self.clickBtnModificar('Modificar'))
			# Funcion para tomar los datos y guardar
			print("GUARDANDO-------------------------------------------------------------------")
			print(datosParaGuardar)
			print("GUARDANDO-------------------------------------------------------------------")

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
