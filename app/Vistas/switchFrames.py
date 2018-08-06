# import tkinter as tk


# def on_entry_click(event):
#     """function that gets called whenever entry is clicked"""
#     if entry.get() == 'Enter your user name...':
#        entry.delete(0, "end") # delete all the text in the entry
#        entry.insert(0, '') #Insert blank for user input
#        entry.config(fg = 'black')
# def on_focusout(event):
#     if entry.get() == '':
#         entry.insert(0, 'Enter your username...')
#         entry.config(fg = 'grey')


# root = tk.Tk()

# label = tk.Label(root, text="User: ")
# label.pack(side="left")

# entry = tk.Entry(root, bd=1)
# entry.insert(0, 'Enter your user name...')
# entry.bind('<FocusIn>', on_entry_click)
# entry.bind('<FocusOut>', on_focusout)
# entry.config(fg = 'grey')
# entry.pack(side="left")

# root.mainloop()

import tkinter as tk

# class MainWindow(tk.Frame):
#     counter = 0
#     def __init__(self, *args, **kwargs):
#         tk.Frame.__init__(self, *args, **kwargs)
#         self.button = tk.Button(self, text="Create new window", 
#                                 command=self.create_window)
#         self.button.pack(side="top")

#     def create_window(self):
#         self.counter += 1
#         t = tk.Toplevel(self)
#         t.wm_title("Window #%s" % self.counter)
#         l = tk.Label(t, text="This is window #%s" % self.counter)
#         l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

# if __name__ == "__main__":
#     root = tk.Tk()
#     main = MainWindow(root)
#     main.pack(side="top", fill="both", expand=True)
#     root.mainloop()
class loginwindow(object):
    def __init__(self, parent):
        self.parent=parent
        self.data=None #Default value, to say its not been set yet
        self.root=tk.Toplevel(self.parent)
        self.root.transient(self.parent)
        self.username=tk.Entry(self.root); self.username.pack()
        self.password=tk.Entry(self.root, show="*"); self.password.pack()
        self.ok=tk.Button(self.root, text="Continue", command=self.checkPass); self.ok.pack()
        self.cancel=tk.Button(self.root, text="Cancel", command=self.cancelPass); self.cancel.pack()

    def checkPass(self):
        self.data=(self.username.get(), self.password.get())
        self.root.destroy()

    def cancelPass(self):
        self.data=False
        self.root.destroy()


def popup():
    passWindow=loginwindow(parent)
    passWindow.parent.wait_window(passWindow.root)
    print(passWindow.data)

parent=tk.Tk()
tk.Button(parent, text='popup', command=popup).pack()
parent.mainloop()