import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

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
		self.frame = tk.Frame(self.root)
		# self.root.state('zoomed')
		self.labelUno = tk.Label(self.frame, text="Label del inicio", padx=10)
		self.labelUno.grid(row=0, column=0, sticky=tk.W)
		self.frame.grid_rowconfigure(1, minsize=10)
		self.frame.place(x=0,y=0)


		self.root.config(menu=mimenu(self.root))
		self.root.mainloop()

def main():
	mi_app = Inicio()
	return 0

if __name__ == '__main__':
	main()
