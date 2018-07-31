import Imge,colorsys

LenaImage1 = Image.open('../data/arboles_01.jpg')
r,g,b = LenaImage1.split()
Hdat = []
Ldat = []
Sdat = []
for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()):
    h,l,s = colorsys.rgb_to_hls(rd/255.,gn/255.,bl/255.)
    Hdat.append(int(h*255.))
    Ldat.append(int(l*255.))
    Sdat.append(int(s*255.))

r.putdata(Hdat)
g.putdata(Ldat)
b.putdata(Sdat)
newimg = Image.merge('RGB',(r,g,b))
newimg.save('lenaHSV.png')
