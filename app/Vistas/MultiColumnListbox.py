import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, parent, car_header, car_list=None):
        self.tree = None
        self.car_header = car_header
        self.car_list = car_list
        self.parent = parent
       
        self._setup_widgets()
        self.build_tree(self.car_list)

    def _setup_widgets(self):
        s = """\click on header to sort by that column
to change width of column drag boundary
        """
        # contenedor = tk.Frame()
        # contenedor.pack()
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(side=tk.TOP, fill='x', expand=True)
        # container = ttk.Frame()
        container = self.parent
        # container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=self.car_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        self.tree.bind("<Double-1>", lambda event, :self.OnDoubleClick(event))
                                    # lambda event, arg=x:self.clickEnsayoReciente(event,arg)
        # self.tree.pack(fill=tk.BOTH, expand=True, in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def build_tree(self, car_list):
        for col in self.car_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in car_list:
            itemArray = [item.nro, item.establecimiento, item.fechaPlantacion, item.tipoClonal, item.nroRepeticiones, item.nroTratamientos, item.espaciamientoX + ' X ' + item.espaciamientoY, item.nroCuadro, item.plantasHa, item.plantasParcela, item.suelo, item.totalHas, item.totalPlantas, '    ', '    ', '    ', '    ']
            self.tree.insert('', 'end', values=itemArray)
            # adjust column's width if necessary to fit each value
            
            # print("=======ITEM ITEM ITEM ITEM ITEM========")
            # print(item)
            # print("=======ITEM ITEM ITEM ITEM ITEM ========")
            for ix, val in enumerate(itemArray):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.car_header[ix],width=None)<col_w:
                    self.tree.column(self.car_header[ix], width=col_w)

    # @staticmethod
    def OnDoubleClick(self, event):
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item, "values"))
        
    @staticmethod
    def sortby(tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float
        #data =  change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so it will sort in the opposite direction
        tree.heading(col, command=lambda col=col: MultiColumnListbox.sortby(tree, col, \
            int(not descending)))

    # @staticmethod
    # def convertObjetToArray(item):


'''
	Datos de ejemplo
	car_header = ['car', 'repair', 'Country']
    car_list = [
    ('Hyundai', 'brakes', 'Uruguay') ,
    ('Honda', 'light', 'Brasil') ,
    ('Lexus', 'battery', 'Uruguay') ,
    ('Benz', 'wiper', 'Uruguay') ,
    ('Ford', 'tire', 'India') ,
    ('Chevy', 'air','Mexico') ,
    ('Chrysler', 'piston', 'India') ,
    ('Toyota', 'brake pedal', 'Chile') ,
    ('BMW', 'seat', 'Italia')
    ]
'''