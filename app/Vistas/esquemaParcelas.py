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
    grilla = None

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.matriz = []
        self.matrizBloques = []
        self.parent = parent
        self.bloqueseleccionado = None
        self.controles = Frame(self)
        self.controles.pack()
        self.colores = [Bloque("Color 1", "#33FFD4"), Bloque("Color 2","#FF336B"), Bloque("Color 3", "#8b77ff")]
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
        print("------repeticion antes de guardar -------")
        print(self.repeticionClave)
        print(CD.buscar_objetos('Repeticion', {'clave' : self.repeticionClave}))
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
                    try:
                        parcela.id_bloques = bloquesObj[self.matrizBloques[x][j]].clave
                    except:
                        messagebox.showinfo("Error", "Alguna de las celdas quedo sin pintar, por favor verifique e intente nuevamente.")
                        return False
                    parcela.id_clones = clonesObj[int(self.matriz[x][j])].clave
                    parcelaGuardada = parcela.guardar(CD.db)
        messagebox.showinfo("Info", "El esquema se ha guardado satisfactoriamente")

    def seleccionarBloque(self, b):
        self.bloqueseleccionado = b
    def pegar(self):
        if self.grilla!=None:
            self.grilla.destroy()   
        self.grilla = Frame(self)     
        self.grilla.pack(padx=5, pady=5)
        if self.b2==None:
            self.b2 = EditorBloques(self.colores,self)
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
    
    def dibujar(self, claveRepeticion):
        repeticion = CD.buscar_objetos('Repeticion', {'clave' : claveRepeticion})[0]
        matrizinicial = [ [ None for i in range(int(repeticion.nroFilas)) ] for j in range(int(repeticion.nroColumnas)) ]
        bloques = CD.buscar_objetos('Bloque', {'id_repeticiones' : repeticion.clave})
        parcelas = []
        clones = []
        for bl in bloques:
            parcelas += CD.buscar_objetos('Parcela', {'id_bloques' : bl.clave})
        for x in parcelas:
            clon = CD.buscar_objetos('Clon', {'clave' : x.id_clones})
            clones += clon
            nroBloque = CD.buscar_objetos('Bloque', {'clave' : x.id_bloques})[0]
            matrizinicial[int(x.columna)][int(x.fila)] = [clon[0].nro, nroBloque.color]
        if self.grilla!=None:
            self.grilla.destroy()   
        self.grilla = Frame(self)     
        self.grilla.pack(padx=5, pady=5)
        if self.b2==None:
            self.b2 = EditorBloques(self.colores,self)
            Button(self.controles,text="Guardar",command=self.listo).pack(pady=5, padx=5, side=LEFT)
        d = []
        self.matriz = []
        self.matrizBloques = []
        for i, linea in enumerate(matrizinicial): 
            self.matriz.append([])
            self.matrizBloques.append([])
            for j,texto in enumerate(linea):
                if texto != None:
                    self.matriz[len(self.matriz) - 1].append(texto[0])                 
                    self.matrizBloques[len(self.matrizBloques) - 1].append(texto[1])                 
                    b = Celda(self.grilla, justify='center',bg=texto[1], width=8)
                    b.insert(0,texto[0])
                    b.grid(row=i + 1, column=j)
                else:
                    b = Celda(self.grilla, justify='center', width=8)
                    b.insert(0,"")
                    b.grid(row=i + 1, column=j)
                    b.config(state = DISABLED )
