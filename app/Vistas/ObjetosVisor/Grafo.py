import threading
import networkx as nx


class Grafo(object):
	"""docstring for Grafo"""
	def __init__(self, canvas, G, id, centros):
		super(Grafo, self).__init__()
		self.canvas = canvas
		self.centros = centros
		self.G = G
		self.id = id
		self.nodos = []
		self.aristas = []
		self.array_id_nodos_canvas = []
		self.array_id_aristas_canvas = []
		self.color = "#2f2"
		self.ANCHO_ARBOL = 25
		self.aspecto_x = self.canvas.aspecto_x
		self.aspecto_y = self.canvas.aspecto_y
	def GetCentrado(self):
		puntos = [n.puntos for n in self.nodos]
		xs = [p[0] and p[2] for p in puntos]
		ys = [p[1] and p[3] for p in puntos]
		offset = self.ANCHO_ARBOL / 2
		return (min(xs) - offset, min(ys) - offset, max(xs) + offset, max(ys) + offset)

	def dibujar(self):
		centros=self.centros#nx.get_node_attributes(self.G,'centro')
		for e in self.G.edges():
			if str(e[0]) in centros:
				centro_a = ((centros[str(e[0])][0][0] / self.aspecto_x), (centros[str(e[0])][0][1] / self.aspecto_y))
				centro_b = ((centros[str(e[1])][0][0] / self.aspecto_x), (centros[str(e[1])][0][1] / self.aspecto_y))
			else:
				centro_a = ((centros[e[0]][0][0] / self.aspecto_x), (centros[e[0]][0][1] / self.aspecto_y))
				centro_b = ((centros[e[1]][0][0] / self.aspecto_x), (centros[e[1]][0][1] / self.aspecto_y))
			self.unir(e[0], e[1],[centro_a,centro_b])			
		for id_nodo in self.G.nodes():
			if str(id_nodo) in centros:
				a = (centros[str(id_nodo)][0][0] - self.ANCHO_ARBOL / 2) / self.aspecto_x
				b = (centros[str(id_nodo)][0][0] + self.ANCHO_ARBOL / 2) / self.aspecto_x
				c = (centros[str(id_nodo)][0][1] - self.ANCHO_ARBOL / 2) / self.aspecto_y
				d = (centros[str(id_nodo)][0][1] + self.ANCHO_ARBOL / 2) / self.aspecto_y
			else:
				a = (centros[id_nodo][0][0] - self.ANCHO_ARBOL / 2) / self.aspecto_x
				b = (centros[id_nodo][0][0] + self.ANCHO_ARBOL / 2) / self.aspecto_x
				c = (centros[id_nodo][0][1] - self.ANCHO_ARBOL / 2) / self.aspecto_y
				d = (centros[id_nodo][0][1] + self.ANCHO_ARBOL / 2) / self.aspecto_y
			self.addNodo([a,c,b,d,],id_nodo)
	def ocultar(self):
		for n in self.nodos + self.aristas:
			threading.Thread(name="CambiarColor", target=n.ocultar).start()
	def desocultar(self):
		for n in self.nodos + self.aristas:
			threading.Thread(name="CambiarColor", target=n.desocultar).start()
	def addNodo(self, puntos, id_grafo):
		self.append(Nodo(puntos,id_grafo,self.canvas))
	def append(self, nodo):
		if nodo.canvas == None:
			nodo.canvas = self.canvas
		self.nodos.append(nodo)
		self.array_id_nodos_canvas = [n.id_canvas for n in self.nodos]
	def unir(self,  a, b, puntos):
		self.aristas.append(Arista(a, b,puntos, self.canvas))
		self.array_id_aristas_canvas = [n.id_canvas for n in self.aristas]
	def pintar(self,color):
		if self.color == color:
			return
		self.color = color
		for n in self.nodos + self.aristas:
			t = threading.Thread(name="CambiarColor", target=n.pintar, args=(color,))
			t.deamon = True
			t.start()
	def existe(self, _id):
		return _id in self.array_id_nodos_canvas
	def existe_arista(self, id_):
		return _id in self.array_id_aristas_canvas
	def GetNodo(self,_id):
		for nodo in self.nodos:
			if nodo.id_canvas == _id:
				return nodo
		return None
	def GetArista(self, _id):
		for arista in self.aristas:
			if arista.id_canvas == _id:
				return arista
		return None
	def DelNodo(self, _id):
		for nodo in self.nodos:
			if nodo.id_canvas == _id:
				for a in self.aristas:
					if a.id_a == nodo.id_grafo or a.id_b == nodo.id_grafo:
						self.DelArista(a.id_canvas)
				nodo.borrar()
				del nodo
				return
	def DelArista(self, _id):
		for arista in self.aristas:
			if arista.id_canvas == _id:
				arista.borrar()
				del arista
				return
	def borrar(self):
		for nodo in list(self.nodos):
			nodo.borrar()
			del nodo
		for arista in list(self.aristas):
			arista.borrar()
			del arista
class Nodo(object):
	"""docstring for Nodo"""
	def __init__(self, p, id_grafo, canvas):
		super(Nodo, self).__init__()
		self.canvas = canvas
		self.id_grafo = id_grafo
		self.puntos = p
		self.id_canvas = self.canvas.create_rectangle(p[0],p[1],p[2],p[3], fill="#2f2", outline="#2f2", stipple="gray12")
	def pintar(self, color):
		if color!="#2f2":
			self.canvas.tag_raise(self.id_canvas)
		self.canvas.itemconfig(self.id_canvas, fill=color,outline=color)
	def borrar(self):
		# print("Borrar ", self.id_grafo)
		self.canvas.delete(self.id_canvas)
	def ocultar(self):
		self.canvas.itemconfig(self.id_canvas, state="hidden")
	def desocultar(self):
		self.canvas.itemconfig(self.id_canvas, state="normal")

class Arista(object):
	"""docstring for Arista"""
	def __init__(self, id_a, id_b, p, canvas):
		super(Arista, self).__init__()
		self.id_a = id_a
		self.id_b = id_b
		self.canvas = canvas
		self.puntos = p
		self.id_canvas = self.canvas.create_line(p[0],p[1], fill="#2f2", width=2)
	def pintar(self, color):
		if color!="#2f2":
			self.canvas.tag_raise(self.id_canvas)
		self.canvas.itemconfig(self.id_canvas, fill=color)
	def borrar(self):
		self.canvas.delete(self.id_canvas)
	def ocultar(self):
		self.canvas.itemconfig(self.id_canvas, state="hidden")
	def desocultar(self):
		self.canvas.itemconfig(self.id_canvas, state="normal")




		