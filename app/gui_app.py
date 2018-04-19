import tkinter as tk

import CLI.deductor as d
import CLI.generador as g
import GUI.abrir as a

class Aplicacion(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.pack(expand=1)

ROOT = tk.Tk()
ROOT.minsize(400, 300)

APP = Aplicacion(master=ROOT)
APP.master.title("TreePy v1.0")

MENU = tk.Menu(ROOT)

MENU_1 = tk.Menu(MENU, tearoff=0)
MENU_1.add_command(label="Abrir", command=a.abrir)
MENU_1.add_command(label="Guardar", command=0)
MENU_1.add_separator()
MENU_1.add_command(label="Configurar", command=0)
MENU_1.add_separator()
MENU_1.add_command(label="Salir", command=ROOT.quit)

MENU_2 = tk.Menu(MENU, tearoff=0)
MENU_2.add_command(label="Generar informe", command=g.generar)
MENU_2.add_command(label="Exportar a CSV", command=0)
MENU_2.add_separator()
MENU_2.add_command(label="Ver grafica", command=0)

MENU_3 = tk.Menu(MENU, tearoff=0)
MENU_3.add_command(label="Contar arboles presentes", command=d.contar_arboles_presentes)
MENU_3.add_command(label="Contar arboles faltantes", command=d.contar_arboles_faltantes)
MENU_3.add_command(label="Contar surcos de arboles", command=d.contar_surcos_arboles)

MENU_4 = tk.Menu(MENU, tearoff=0)
MENU_4.add_command(label="Acerca de", command=0)
MENU_4.add_command(label="Manual", command=0)

MENU.add_cascade(label="TreePy", menu=MENU_1)
MENU.add_cascade(label="Analisis", menu=MENU_2)
MENU.add_cascade(label="Imagen", menu=MENU_3)
MENU.add_cascade(label="Ayuda", menu=MENU_4)

ROOT.config(menu=MENU)

APP.mainloop()
