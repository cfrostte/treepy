import copy

class Prueba1(object):

    def __init__(self):
        self.g = [4,3,3]

class Prueba(object):

    def __init__(self):
        self.n = [4,3,3]
        self.m = [1,2,544,15,6]        
        self.p1 = Prueba1()

#a = Prueba()
b = Prueba()
a = copy.deepcopy(b)
b.n.append(888)
b.p1.g.append(1111111)
print(a.n,a.m,a.p1.g)
print(b.n,b.m,b.p1.g)
