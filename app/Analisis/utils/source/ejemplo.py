from PIL import Image
from PIL import ImageDraw
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon, Point
import numpy as np

img = Image.new("RGB", (512,512), "black")
draw = ImageDraw.Draw(img)
plt.imshow(img)
coords = plt.ginput(-1)

dotSize = 3
draw.line(coords, width=dotSize, fill="red")

# coords = np.asarray(coords)
p = Polygon(coords)

a = Point(400,250)
b = Point(1, 1)


print(b.within(p))
print(a.within(p))

print(p)
img.show()
