import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import cgitb
from inspect import getmembers
from pprint import pprint
import random
from esquemaParcelas import esquemaParcelas


actualFrame = 1
def donothing():
	print("donothing")

# def dounpack(frame):
# 	frame.pack_forget()
# 	print("forget")



# class Menu():
# 	def __init__(self, root):
# 		self.filemenu = tk.Menu(root)
# 		self.filemenu.add_command(label="New", command=donothing)
# 		self.filemenu.add_command(label="Exit", command=donothing)

class Inicio(object):
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("1280x768")
		self.root.title("TreePy Analisis de Imagenes")
		self.frameActivo = "Inicio"

		misframes = ['Inicio', 'Ensayo', 'Repeticion', 'Analisis']
		self.misframes = self.generarFrames(misframes)
		
		# self.frame = VerticalScrolledFrame(self.root)
		# self.frame.set_name("FRAME DE INICIO")
		self.misframes['Inicio'].pack(fill=tk.BOTH, padx=0, pady=0, expand=True)

		self.ensayosRecientes()
		self.verEnsayo()
		self.verRepeticion()
		# self.frame2 = VerticalScrolledFrame(self.root)
		# self.frame2.set_name("SEGUNDO FRAME")

		# self.frame.pack()
		# raise_frame(self.frame)
		# self.root.state('zoomed')
		# self.labelUno = ttk.Label(self.misframes['Inicio'].interior, text=self.misframes['Inicio'].nameFrame)
		# self.labelUno2 = ttk.Label(self.misframes['Ensayo'].interior, text=self.misframes['Ensayo'].nameFrame)
		# self.labelUno.grid(row=0, column=0, sticky=tk.W)
		# self.subframe
		# self.labelUno.pack(side=tk.TOP)
		# self.labelUno2.pack(side=tk.TOP)

		
		# self.frame.grid_rowconfigure(1, minsize=10)
		self.root.config(menu=self.mimenu(self.root))
		self.root.mainloop()

	def createCampo(self, frameContainer, texto):
		entry = tk.Entry(frameContainer)
		entry.insert(0, texto)
		entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
		entry.config(state=tk.DISABLED)
		return entry

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
		for x in range(0, 5):
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
			ensayoImage = Image.open('iconImage.png')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			fotosRepeticion.append(datos)
			label.bind("<Button-1>", lambda event, arg=datos[1]["text"]:self.clickEnsayoReciente(event,arg))
			# label.bind("<Button-1>", self.clickEnsayoReciente(self,datos[1]["text"]))
			if len(fotosRepeticion) % 3 ==0:
				print("salto imegen repe")
				# rand = random.choice(colores)
				frameContainer.append(tk.Frame(totalFrame[2]))
				frameContainer[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		#####



	def verEnsayo(self):
		print('émpieza ver ensayo')

		totalFrame = []
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		totalFrame.append(tk.Frame(self.misframes['Ensayo'].interior))
		totalFrame[-1].pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


		frameContainer = []
		frameContainer.append(tk.Frame(totalFrame[0]))
		frameContainer[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

		tituloEnsayo = 'Ensayo Nro 2131'
		titulo = tk.Label(frameContainer[-1], text=tituloEnsayo)
		titulo.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Repeticiones: ', '3')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Establecimento: ', 'La Tribu')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Cuadro: ', 'H007')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Suelo: ', '9.3')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Espaciamiento: ', '4 X 1.9')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Plantas/Ha: ', '1315')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Fecha de plantacion: ', '15/09/2017')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Tratamientos: ', '27')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Total de plantas: ', '1620')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Total Has: ', '1.23')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'N° Repeticiones: ', '3')
		self.frameCreateCampo(frameContainer, totalFrame[0], 'Plantas por parcela: ', '20')

		frameContainer.append(tk.Frame(totalFrame[1]))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

		tituloRepeticiones = 'Repeticiones'
		tituloRepeticiones = tk.Label(frameContainer[-1], text='Repeticiones')
		tituloRepeticiones.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		tituloRepeticiones.config(font=("Courier",33))

		totalRepeticiones = '3'
		for x in range(0, int(totalRepeticiones)):
			labelRepeticion = tk.Label(frameContainer[-1], text='Repeticion '+str(x+1))
			labelRepeticion.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
			labelRepeticion.bind("<Button-1>", lambda event, arg='Repeticion '+ str(x+1):self.clickVerRepeticion(event,arg))



	def frameCreateCampo(self, frameContainer, parent, textLabel, textDato):
		frameContainer.append(tk.Frame(parent))
		frameContainer[-1].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		label = tk.Label(frameContainer[-1], text=textLabel).pack(side=tk.LEFT, fill=tk.BOTH)
		entry = self.createCampo(frameContainer[-1], textDato)

	def ensayosRecientes(self):
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

		for x in range(1,10):
			frameContainerIn = []
			frameContainerIn.append(tk.Frame(frameContainer[-1]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)
			frameContainerIn.append(tk.Frame(frameContainer[-1]))
			frameContainerIn[-1].pack(side=tk.TOP,fill=tk.BOTH, expand=True)

			datos = []
			nombre = 'Ensayo' + str(x)
			nombrelabel = tk.Label(frameContainerIn[0], text=nombre)
			nombrelabel.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			ensayoImage = Image.open('Image.png')
			ensayoImage = ensayoImage.resize((175,175),Image.ANTIALIAS)
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainerIn[1], image=photo)
			label.image = photo
			label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombrelabel)
			fotosEnsayos.append(datos)
			label.bind("<Button-1>", lambda event, arg=datos[1]["text"]:self.clickEnsayoReciente(event,arg))
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
		menu_archivo.add_command(label="Abrir ensayo", command=donothing)
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

	def clickEnsayoReciente(self, event, nombre):
		print("Click izquierdo")
		print(nombre)

		self.raise_frame(self.misframes[self.frameActivo], self.misframes['Ensayo'])


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



def main():
	mi_app = Inicio()
	return 0



if __name__ == '__main__':
	main()
