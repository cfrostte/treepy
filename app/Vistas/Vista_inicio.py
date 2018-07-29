import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageTk
import cgitb
from inspect import getmembers
from pprint import pprint

def donothing():
	print("donothing")

# def hello(x,y):
	# messagebox.showinfo("Say Hello", "Hello World" + str(x) + " : " + str(y))

def mimenu(root):
	MENU = tk.Menu(root)
	# MENU.post(0,768)
	

	menu_archivo = tk.Menu(MENU, tearoff=0)
	menu_edicion = tk.Menu(MENU, tearoff=0)
	menu_vista = tk.Menu(MENU, tearoff=0)
	menu_ayuda = tk.Menu(MENU, tearoff=0)

	menu_archivo.add_command(label="Nuevo ensayo", command=donothing)
	# menu_archivo.add_command(label="Nuevo ensayo", command=hello(root.winfo_screenwidth(), root.winfo_screenheight()))
	menu_archivo.add_separator()
	menu_archivo.add_command(label="Salir", command=root.quit)

	menu_edicion.add_command(label="Editar ensayo", command=donothing)
	menu_edicion.add_command(label="Editar Repeticion", command=donothing)



	MENU.add_cascade(label="Archivo", menu=menu_archivo)
	MENU.add_cascade(label="Edicion", menu=menu_edicion)
	MENU.add_cascade(label="Vista", menu=menu_vista)
	MENU.add_cascade(label="Ayuda", menu=menu_ayuda)
	


	return MENU

class Menu():
	def __init__(self, root):
		# self.menubar = tk.Menu(frame)
		self.filemenu = tk.Menu(root)
		self.filemenu.add_command(label="New", command=donothing)
		self.filemenu.add_command(label="Exit", command=donothing)

class Inicio():
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("1280x768")
		self.root.title("TreePy Analisis de Imagenes")
		# self.frame = tk.Frame(self.root)
		# self.frame = DoubleScrollbarFrame(self.root, relief="sunken")
		self.frame = VerticalScrolledFrame(self.root)
		self.frame.pack(fill=tk.BOTH, padx=0, pady=0, expand=True)
		#subframe

		#retorna una canvas
		# self.subframe = ttk.Frame( self.frame.get_frame() )

		self.root.state('zoomed')
		self.labelUno = ttk.Label(self.frame.interior, text="Label del inicio")
		# self.labelUno.grid(row=0, column=0, sticky=tk.W)
		# self.subframe

		# Relleno del frame
		# self.ensayosRecientes = []
		self.ensayosRecientes = self.ensayosRecientes()
		
		#----------------------------------------

		#----------------------------------------
		
		# self.tree = tk.Treeview(self.frame, selectmode="extended")
		# scbVDirSel = tk.Scrollbar(self.frame, orient=TKinter.HORIZONTAL, command=self.tree.xview)
		# scbHDirSel = tk.Scrollbar(self.frame, orient=TKinter.VERTICAL, command=self.tree.yview)
		# self.tree.configure(yscrollcommand=scbVDirSel.set, xscrollcommand=scbHDirSel.set)
		# self.tree.column("#0", width=40)
		# self.tree.heading("#0")
		# scrollbar = tk.Scrollbar(self.root)
		# scrollbar.pack(side = RIGHT, fill = Y)
		# scrollbar.config(command=self.frame.yview)

		# self.ensayosRecientes[0][0].grid(row=1,column=0)
		# self.ensayosRecientes[1][0].grid(row=1,column=1)
		# self.ensayosRecientes[2][0].grid(row=1,column=2)
		# self.ensayosRecientes[3][0].grid(row=2,column=0)
		# self.ensayosRecientes[4][0].grid(row=2,column=1)
		# self.ensayosRecientes[5][0].grid(row=2,column=2)
		# self.ensayosRecientes[6][0].grid(row=3,column=0)
		# self.ensayosRecientes[7][0].grid(row=3,column=1)
		# self.ensayosRecientes[8][0].grid(row=3,column=2)
		# ################## #
		
		self.labelUno.pack()
		# self.subframe.pack(padx  = 15, pady   = 15, fill = tk.BOTH, expand = tk.TRUE)
		# self.frame.pack( padx   = 5, pady   = 5, expand = True, fill = tk.BOTH)

		self.frame.grid_rowconfigure(1, minsize=10)
		# self.frame.place(x=0,y=0)

		self.root.config(menu=mimenu(self.root))
		self.root.mainloop()

	def ensayosRecientes(self):
		fotosEnsayos = []
		frameContainer=[]
		frameContainer.append(tk.Frame(self.frame.interior))
		frameContainer[-1].pack(fill=tk.BOTH, expand=True)

		for x in range(1,10):
			datos = []
			nombre = 'Ensayo' + str(x)
			ensayoImage = Image.open('Image.png')
			photo = ImageTk.PhotoImage(ensayoImage)
			label = tk.Label(frameContainer[-1], image=photo)
			label.image = photo
			label.pack(side=tk.LEFT, padx=5, pady=5, expand=True)
			datos.append(label)
			datos.append(nombre)
			fotosEnsayos.append(datos)
			if len(fotosEnsayos) % 3 ==0:
				frameContainer.append(tk.Frame(self.frame.interior))
				frameContainer[-1].pack(fill=tk.BOTH, expand=True)
		return fotosEnsayos


    

def main():
	mi_app = Inicio()
	return 0

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
	    # print(self.winfo_reqwidth())
	    # print(self.winfo_reqheight())
	    # size = ( self.winfo_reqwidth(), self.winfo_reqheight() )
	    # self.canvas.config(scrollregion="0 0 %s %s" % size)

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
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=True)
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


if __name__ == '__main__':
	main()
