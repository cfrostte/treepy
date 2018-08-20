from tkinter import *   # from x import * is bad practice
# import tkinter as tk
# from ttk import *
from tkinter import ttk
from PIL import Image, ImageTk
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

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


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)
            # root = self.Tk()
            # root.state('zoomed') 
            print(type(root))
            # root.geometry("1280x768")


            self.frame = VerticalScrolledFrame(root)
            self.frame.pack(fill=BOTH, padx=0, pady=0, expand=True)
            # self.frameContainer=[]
            # self.frameContainer.append(Frame(self.frame.interior))
            # self.frameContainer[-1].pack(fill=BOTH, expand=True)

            # self.label = Label(text="Shrink the window to activate the scrollbar.")
            # self.label.pack()
            # buttons = []
            # for i in range(10):
            #     buttons.append(Button(self.frame.interior, text="Button " + str(i)))
            #     buttons[-1].pack()
            self.ensayosRecientes = self.ensayosRecientes()
            # self.ensayosRecientes[0][0].pack(side=LEFT)  
            # self.ensayosRecientes[1][0].pack(side=LEFT) 
            # self.ensayosRecientes[2][0].pack(side=LEFT)  
            # self.ensayosRecientes[3][0].pack(side=LEFT)
            # self.ensayosRecientes[4][0].pack(side=LEFT)
            # self.ensayosRecientes[5][0].pack(side=LEFT)
            # self.ensayosRecientes[6][0].pack(side=LEFT)
            # self.ensayosRecientes[7][0].pack(side=LEFT)
            # self.ensayosRecientes[8][0].pack(side=LEFT)

        def ensayosRecientes(self):
            fotosEnsayos = []
            frameContainer=[]
            frameContainer.append(Frame(self.frame.interior))
            frameContainer[-1].pack(fill=BOTH, expand=True)

            # fotitos = []
            for x in range(1,10):
                datos = []
                nombre = 'Ensayo' + str(x)
                ensayoImage = Image.open('Image.png')
                photo = ImageTk.PhotoImage(ensayoImage)
                # label = Label(self.frame.interior, image=photo)
                label = Label(frameContainer[-1], image=photo)
                label.image = photo
                label.pack(side=LEFT, padx=5, pady=5, expand=True)
                print(len(fotosEnsayos))
                print(len(fotosEnsayos) % 3)
                datos.append(label)
                datos.append(nombre)
                fotosEnsayos.append(datos)
                if len(fotosEnsayos) % 3 == 0:
                    frameContainer.append(Frame(self.frame.interior))
                    frameContainer[-1].pack(fill=BOTH, expand=True)
            return fotosEnsayos

    app = SampleApp()
app.mainloop()