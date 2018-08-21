# import tkinter as tk
# import tkinter.font as tkFont
# import tkinter.ttk as ttk

# class ModifiedMcListBox(object):

#     def __init__(self):
#         self.root= tk.Tk()
#         self.tree = None
#         self.element_header = ["Device", "Type", "LETs Threshold (L0)"]
#         self.element_list =  [('93L422', 'Bipolar', '0.6')]
#         self._setup_widgets()
#         self._build_tree()
#         self.root.mainloop()

#     def _setup_widgets(self):
#         s = """
#         """
#         msg = ttk.Label(wraplength="4i", justify="right", anchor="n",
#             padding=(6, 6, 6, 6, 6 ,6), text=s)
#         msg.pack(fill='x')
#         container = ttk.Frame()
#         container.pack(fill='both', expand=True)
#         self.tree = ttk.Treeview(columns=self.element_header, show="headings")
#         vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
#         hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
#         self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
#         self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
#         vsb.grid(column=1, row=0, sticky='ns', in_=container)
#         hsb.grid(column=0, row=1, sticky='ew', in_=container)
#         container.grid_columnconfigure(0, weight=1)
#         container.grid_rowconfigure(0, weight=1)
#         tk.Button(self.root, text='Bring up Message', command=self.Child_Window).pack()

#     def _build_tree(self):
#         for col in self.element_header:
#             self.tree.heading(col, text=col.title(),
#                 command=lambda c=col: self.sortby(self.tree, c, 0))
#             self.tree.column(col, width=tkFont.Font().measure(col.title()))
#         for item in self.element_list:
#             self.tree.insert('', 'end', values=item)
#             for ix, val in enumerate(item):
#                 col_w = tkFont.Font().measure(val)
#                 if self.tree.column(self.element_header[ix], width=None) < col_w:
#                     self.tree.column(self.element_header[ix], width=col_w)

#     def isnumeric(self,s):
#         for c in s:
#             if c in "0000123456789000-.":
#                 numeric = True
#             else:
#                 return False
#         return numeric

#     def change_numeric(self,data):
#         new_data = []
#         if self.isnumeric(data[0][0]):
#             for child, col in data:
#                 new_data.append((float(child), col))
#             return new_data
#         return data

#     def sortby(self,tree, col, descending):
#         data = [(tree.set(child, col), child) for child in tree.get_children('')]
#         data = self.change_numeric(data)
#         data.sort(reverse=descending)
#         for ix, item in enumerate(data):
#             tree.move(item[1], '', ix)
#         tree.heading(col,
#             command=lambda col=col: sortby(tree, col, int(not descending)))

#     def Child_Window(self):
#         win2 = tk.Toplevel()
#         message = "This is the child window"
#         tk.Label(win2, text=message).pack()
#         new_element_header=['1st','2nd','3rd']
#         treeScroll = ttk.Scrollbar(win2)
#         treeScroll.pack(side=tk.RIGHT, fill=tk.Y)
#         tree = ttk.Treeview(win2,columns=new_element_header, show="headings", yscrollcommand = treeScroll)
#         tree.heading("1st", text="1st")
#         tree.heading("2nd", text="2nd")
#         tree.heading("3rd", text="3rd")
#         tree.pack(side=tk.LEFT, fill=tk.BOTH)
#         treeScroll.config(command=tree.yview)

# mc_listbox = ModifiedMcListBox()

# import tkinter
# import tkinter.filedialog
# import getpass
# # Need this for the `os.path.split` function
# import os
# gui = tkinter.Tk()
# user = getpass.getuser()
# def click():
#     # Get the file
#     file = tkinter.filedialog.askopenfilename(initialdir='C:/Users/%s' % user)
#     # Split the filepath to get the directory
#     print(file)
#     print(os.path)
#     directory = os.path.split(file)[0]
#     print(directory)
# button = tkinter.Button(gui, command=click)
# button.grid()
# gui.mainloop()

import shutil,os
import tkinter as tk
import tkinter.filedialog as filedialog
import pathlib

def callback():
  src = filedialog.askopenfilename()

  # des = 'C://Users//priyanka.rani//.spyder-py3'
  pathlib.Path('C://Users//v785712//Desktop//micarpetitia//').mkdir(parents=True, exist_ok=True) 
  des = 'C://Users//v785712//Desktop//micarpetitia//algo.jpg'
  print(src)
  shutil.copy(src, des)

gui = tk.Tk()
errmsg = 'Error!'
tk.Button(gui, text='File Open', command=callback).pack(fill=tk.X)# calling function to add in Tkinter GUI
gui.mainloop()