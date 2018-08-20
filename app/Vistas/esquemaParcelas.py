import pyperclip
import tkinter
from tkinter import *
from Vistas.bloques import EditorBloques, Bloque
from Vistas.celda import Celda        

class esquemaParcelas(Frame):
    todaLaMatriz = None

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.matriz = []
        self.matrizBloques = []
        self.parent = parent
        self.bloqueseleccionado = None
        self.controles = Frame(self)
        self.controles.pack()
        self.colores = [Bloque("Bloque 1", "#33FFD4"), Bloque("Bloque 2","#FF336B"), Bloque("Bloque 3", "#311F63")]
        # self.colores = ['#33FFD4', '#FF336B', '#311F63']
        self.grilla = None
        self.b1 = Button(self.controles,text="Pegar",command=self.pegar)
        self.b1.pack(pady=5, padx=5, side=LEFT)
        self.b2 = None
    def listo(self):
        for celda in self.grilla.winfo_children():
            pos = celda.grid_info()
            self.matrizBloques[pos["row"]-1][pos["column"]] = celda.bloque.color if celda.bloque!=None else None
        print("printing matriz")
        print(self.matriz)
        print("------------printing matriz--------------")
        todaLaMatriz = self.matrizBloques
        print(self.matrizBloques)
        print("printing matriz")
    def seleccionarBloque(self, b):
        self.bloqueseleccionado = b
    def pegar(self):
        if self.grilla!=None:
            self.grilla.destroy()   
        self.grilla = Frame(self)     
        self.grilla.pack(padx=5, pady=5)
        if self.b2==None:
            # self.b2 = Button(self.controles,text="Colorear bloque",command=lambda:EditorBloques(self.colores,self))
            self.b2 = EditorBloques(self.colores,self)
            # self.b2.pack(pady=5, padx=5, side=LEFT)
            Button(self.controles,text="Guardar",command=self.listo).pack(pady=5, padx=5, side=LEFT)
        copiado = pyperclip.paste()
        d = []
        self.matriz = []
        self.matrizBloques = []
        for line in copiado.split('\r\n'):
                if line != "" and line != " ":
                    fields = line.split('\t')
                    d.append(fields)
        for i, linea in enumerate(d): 
            self.matriz.append([])
            self.matrizBloques.append([])
            for j,texto in enumerate(linea):
                self.matriz[len(self.matriz) - 1].append(texto)                 
                self.matrizBloques[len(self.matrizBloques) - 1].append(None)                 
                b = Celda(self.grilla, justify='center', width=8)
                b.insert(0,texto)
                b.grid(row=i + 1, column=j)
                if(texto == "" or texto == " "):
                    b.config(state = DISABLED )


# if __name__ == "__main__":
#     root = Tk()
#     root.title("Creando Repetición")
#     mainapp = esquemaParcelas(root).pack(side="top", fill="both", expand=True)
#     print(mainapp)
#     root.mainloop()




