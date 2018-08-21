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
		self.frame = tk.Frame(self.parent)
		self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
		self.listaDeEnsayos = MultiColumnListbox(self.frame, ensayos_header, self.ensayos_list)



