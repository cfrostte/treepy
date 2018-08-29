import pyperclip
import tkinter
from tkinter import *
from Vistas.bloques import EditorBloques, Bloque
from Vistas.celda import Celda
from tkinter import messagebox
from ControladorDatos import ControladorDatos as CD

class esquemaParcelas(Frame):
    todaLaMatriz = None
    repeticionClave = None

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
        bloques = []
        bloquesObj = {}
        clones = []
        clonesObj = {}
        repe = CD.buscar_objetos('Repeticion', {'clave' : self.repeticionClave})[0]
        # repe.nro
        repe.nroColumnas = len(self.matriz)
        repe.nroFilas    = len(self.matriz[0])
        repe.guardar(CD.db)
        for celda in self.grilla.winfo_children():
            pos = celda.grid_info()
            self.matrizBloques[pos["row"]-1][pos["column"]] = celda.bloque.color if celda.bloque!=None else None
            if celda.bloque!=None:
                print("------Dentro de if")
                print(celda.bloque.color)
                if not celda.bloque.color in bloques:
                    bloque = CD.buscar_objetos('Bloque', {'id_repeticiones' : self.repeticionClave, 'color' : celda.bloque.color})
                    if bloque==[]:
                        new = CD.crear_objeto('Bloque')
                        new.color = celda.bloque.color
                        new.id_repeticiones = self.repeticionClave
                        new.tipoSuelo = ' '
                        bloque = new.guardar(CD.db)
                        bloquesObj[bloque.color] = bloque
                        bloques.append(bloque.color)
                    else:
                        bloquesObj[bloque[0].color] = bloque[0]
                        bloques.append(bloque[0].color)

        for x in range(len(self.matriz)):
            for j in range(len(self.matriz[x])):
                if self.matriz[x][j].strip() != '':
                    clon = CD.buscar_objetos('Clon', {'nro' : self.matriz[x][j]})
                    if clon==[]:
                        newClon = CD.crear_objeto('Clon')
                        newClon.nro = self.matriz[x][j]
                        clon = newClon.guardar(CD.db)
                        clonesObj[clon.nro] = clon
                        clones.append(clon.nro)
                    else:
                        clonesObj[clon[0].nro] = clon[0]
                        clones.append(clon[0].nro)

        for x in range(len(self.matriz)):
            for j in range(len(self.matriz[x])):
                if self.matriz[x][j].strip() != '':
                    #Guardo la parcela
                    parcela = CD.crear_objeto('Parcela')
                    parcela.columna = str(x)
                    parcela.fila = str(j)
                    parcela.id_bloques = bloquesObj[self.matrizBloques[x][j]].clave
                    parcela.id_clones = clonesObj[int(self.matriz[x][j])].clave
                    parcelaGuardada = parcela.guardar(CD.db)
                    print("Parcela guardada")
                    print(parcelaGuardada)
                    print("Parcela guardada")
                    #

        #Primero guardo los bloques y me quedo con la clave
        
        messagebox.showinfo("Info", "El esquema se ha guardado satisfactoriamente")

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




