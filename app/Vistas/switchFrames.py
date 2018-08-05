import tkinter as tk


def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if entry.get() == 'Enter your user name...':
       entry.delete(0, "end") # delete all the text in the entry
       entry.insert(0, '') #Insert blank for user input
       entry.config(fg = 'black')
def on_focusout(event):
    if entry.get() == '':
        entry.insert(0, 'Enter your username...')
        entry.config(fg = 'grey')


root = tk.Tk()

label = tk.Label(root, text="User: ")
label.pack(side="left")

entry = tk.Entry(root, bd=1)
entry.insert(0, 'Enter your user name...')
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry.config(fg = 'grey')
entry.pack(side="left")

root.mainloop()