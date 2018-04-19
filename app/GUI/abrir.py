from tkinter import filedialog
from matplotlib import pyplot

import cv2

def abrir():
    elegido = filedialog.askopenfilename(initialdir="/", title="Abrir", filetypes=(("JPG", "*.jpg"), ("JPEG", "*.jpeg"), ("PNG", "*.png")))
    pyplot.imshow(cv2.cvtColor(cv2.imread(elegido), cv2.COLOR_BGR2RGB))
    pyplot.show() # Mostrar la imagen elegida en color RGB, permitiendo manipularla
