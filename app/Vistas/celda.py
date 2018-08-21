from tkinter import *

class Celda(Entry):
    def __init__(self, parent, *args, **kwargs):
        Entry.__init__(self, parent, *args, **kwargs)
        self.bind("<Button-1>", self.click)
        self.bloque = None
        # self.bind("<Button-3>", self.popup)

    def click(self,event):
        if self.master.master.bloqueseleccionado != None:
            self.pintar(self.master.master.bloqueseleccionado)
    def popup(self, event):
        self.popup_menu = Menu(self, tearoff=0)
        for c in self.master.master.colores:
            self.popup_menu.add_command(label=str(c.nombre), command=lambda bloque=c: self.pintar(bloque))
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    
    def pintar(self, bloque):
        self.bloque = bloque
        self.config(bg=bloque.color)