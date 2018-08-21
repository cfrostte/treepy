import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import cgitb
from inspect import getmembers
from pprint import pprint
import random


actualFrame = 1
def donothing():
	print("donothing")

def raise_frame(frame, newframe):
    # frame.tkraise()
    frame.pack_forget()
    newframe.pack()
    print("raise")

def dounpack(frame):
	frame.pack_forget()
	print("forget")

def mimenu(root, frame, newframe):
	MENU = tk.Menu(root)

	menu_archivo = tk.Menu(MENU, tearoff=0)
	menu_edicion = tk.Menu(MENU, tearoff=0)
	menu_vista = tk.Menu(MENU, tearoff=0)
	menu_ayuda = tk.Menu(MENU, tearoff=0)

	menu_archivo.add_command(label="Nuevo ensayo", command=donothing)
	menu_archivo.add_separator()
	menu_archivo.add_command(label="Salir", command=root.quit)

	menu_edicion.add_command(label="Editar ensayo", command=donothing)
	menu_edicion.add_command(label="Editar Repeticion", command=lambda:raise_frame(frame, newframe))

	MENU.add_cascade(label="Archivo", menu=menu_archivo)
	MENU.add_cascade(label="Edicion", menu=menu_edicion)
	MENU.add_cascade(label="Vista", menu=menu_vista)
	MENU.add_cascade(label="Ayuda", menu=menu_ayuda)
	
	return MENU

class Menu():
	def __init__(self, root):
		self.filemenu = tk.Menu(root)
		self.filemenu.add_command(label="New", command=donothing)
		self.filemenu.add_command(label="Exit", command=donothing)

class Inicio():
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("1280x768")
		self.root.title("TreePy Analisis de Imagenes")
		self.frame2 = VerticalScrolledFrame(self.root)

		self.frame = VerticalScrolledFrame(self.root)
		self.frame.pack(fill=tk.BOTH, padx=0, pady=0, expand=True)
		# raise_frame(self.frame)
		self.root.state('zoomed')
		self.labelUno = ttk.Label(self.frame.interior, text="Bienvenido al inicio")
		self.labelUno2 = ttk.Label(self.frame2.interior, text="Bienvenido FRAME DOSSSS")
		# self.labelUno.grid(row=0, column=0, sticky=tk.W)
		# self.subframe
		self.labelUno.pack(side=tk.TOP)
		self.labelUno2.pack(side=tk.TOP)

		self.ensayosRecientes = self.ensayosRecientes()
		
		# self.frame.grid_rowconfigure(1, minsize=10)
		self.root.config(menu=mimenu(self.root, self.frame, self.frame2))
		self.root.mainloop()

	def ensayosRecientes(self):
		fotosEnsayos = []
		frameContainer=[]
		colores = ['blue', 'red', 'green','black', 'yellow', 'white']
		# rand = random.choice(colores)

		frameContainer.append(tk.Frame(self.frame.interior))
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
			if len(fotosEnsayos) % 3 ==0:
				print("salto")
				# rand = random.choice(colores)
				frameContainer.append(tk.Frame(self.frame.interior))
				frameContainer[-1].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		return fotosEnsayos


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

def main():
	mi_app = Inicio()
	return 0

if __name__ == '__main__':
	main()
