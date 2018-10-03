class Parcela(object):
	"""docstring for Grafo"""
	def __init__(self, canvas, id_p):
		self.canvas = canvas 
		self.id = id_p
		self.aspecto_x = canvas.aspecto_x
		self.aspecto_y = canvas.aspecto_y
		self.puntos = []
		self.poligono = None
		self.parcelaDB = None
	def addPunto(self,x,y):
		self.puntos.append([x,y])
		self.dibujar()
	def dibujar(self):
		if self.poligono: self.canvas.delete(self.poligono)
		self.poligono = self.canvas.create_polygon(self.puntos, outline='blue', width=1,fill='white',stipple="gray12")
	def borrar(self):
		if self.poligono: self.canvas.delete(self.poligono)
	def getPoligono(self):
		poly = [(punto[0] * self.aspecto_x, punto[1] * self.aspecto_y) for punto in self.puntos]
		return poly
	def setParcelaDB(self, db):
		self.parcelaDB = db
