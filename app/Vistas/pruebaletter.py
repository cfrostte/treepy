import random
from tkinter import *

root = Tk()
root.geometry("1000x500")

w = Label(root, text="GAME")
w.pack(side=TOP)
frameContainer=[]
frameContainer.append(Frame(root))
frameContainer[-1].pack(fill=BOTH, expand=True)
# there are 40 tiles
tiles_letter = ['a', 'b', 'c', 'c', 'c', 'd', 'd', 'e', 'e', 'e', 'e', 'f', 'f', 'g', 'g', 'h', 'i', 'j', 'k', 'k', 'a', 'b', 'c', 'c', 'c', 'd', 'd', 'e', 'e', 'e', 'e', 'f', 'f', 'g', 'g', 'h', 'i', 'j', 'k', 'k']

tiles_make_word = []

def add_letter():
    global frameContainer
    if not tiles_letter:
        return
    rand = random.choice(tiles_letter)
    tiles_make_word.append(rand)
    print(len(tiles_make_word))
    tile_frame_column = Label(frameContainer[-1], text=rand, bg="red", fg="white")
    tile_frame_column.config()
    tile_frame_column.pack(side=LEFT, fill=BOTH, padx=0, pady=0, expand=True)
    tiles_letter.remove(rand)  # remove that tile from list of tiles
    print( len(tiles_make_word),'***********')
    if len(tiles_make_word) % 3 == 0:
        frameContainer.append(Frame(root,height=100))
        frameContainer[-1].pack(fill=BOTH, expand=True)
    # root.after(50, add_letter)

# root.after(50, add_letter)
for x in range(1,10):
    add_letter()
root.mainloop()