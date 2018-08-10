import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from Vistas.MultiColumnListbox import MultiColumnListbox

ensayos_header = ['Nro Ensayo', 'Establecimiento', 'Fecha de Plantacion', 'Clonal', 'Repeticiones', 'Tratamientos', 'Espaciamiento', 'Cuadro', 'Plantas por Ha', 'Plantas por parcela', 'Suelo', 'Total de Has', 'Total de plantas', '    ', '     ', '     ', '      ']
# car_list = [
# ('Hyundai', 'brakes', 'Uruguay') ,
# ('Honda', 'light', 'Brasil') ,
# ('Lexus', 'battery', 'Uruguay') ,
# ('Benz', 'wiper', 'Uruguay') ,
# ('Ford', 'tire', 'India') ,
# ('Chevy', 'air','Mexico') ,
# ('Chrysler', 'piston', 'India') ,
# ('Toyota', 'brake pedal', 'Chile') ,
# ('BMW', 'seat', 'Italia')
# ]
class AbrirEnsayo(object):
	def __init__(self, parent, todosLosEnsayos):
		self.parent=parent
		self.data=None #Default value, to say its not been set yet
		self.ensayos_list = todosLosEnsayos
		# self.root=tk.Toplevel(self.parent)
		# self.root=tk.Toplevel()
		# self.root=tk.Tk()
		# self.root.transient(self.parent)
		# self.username=tk.Entry(self.root); self.username.pack()
		# self.password=tk.Entry(self.root, show="*"); self.password.pack()
		self.frame = tk.Frame(self.parent)
		self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.listaDeEnsayos = MultiColumnListbox(self.frame, ensayos_header, self.ensayos_list)
		# self.ok=tk.Button(self.frame, text="Continue", command=self.checkPass); self.ok.grid()
		# self.cancel=tk.Button(self.frame, text="Cancel", command=self.cancelPass); self.cancel.grid()

	# def checkPass(self):
	# 	self.data=(self.username.get(), self.password.get())
	# 	self.root.destroy()

	# def cancelPass(self):
	# 	self.data=False
	# 	self.root.destroy()



