# class FakeEnsayo(object):
# 	"""docstring for FakeEnsayo"""
# 	def __init__(self, arg):
# 		super(FakeEnsayo, self).__init__()
# 		self.arg
from PIL import Image, ExifTags
from datetime import datetime as dt

img = Image.open("./arboles_00.jpg")
exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }

lat = [float(x) / float(y) for x, y in exif['GPSInfo'][2]]
lon = [float(x) / float(y) for x, y in exif['GPSInfo'][4]]
alt = float(exif['GPSInfo'][6][0]) / float(exif['GPSInfo'][6][1])
timestamp = exif['DateTimeOriginal']

info = {}
info['lat'] = (lat[0] + lat[1] / 60)
info['lon'] = (lon[0] + lon[1] / 60)
info['altitude'] = alt

if exif['GPSInfo'][1] == "S":
        info['lat'] *= -1
if exif['GPSInfo'][3] == "W":
    info['lon'] *= -1
# if we're below sea level, the value's negative
if exif['GPSInfo'][5] == 1:
	info['altitude'] *= -1

info['width'] = exif['ExifImageWidth']
info['height'] = exif['ExifImageHeight']
# info['fecha'] = dt.strptime(timestamp, "%Y:%m:%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")
info['fecha'] = dt.strptime(timestamp, "%Y:%m:%d %H:%M:%S").strftime("%Y/%m/%d %H:%M:%S")

print(timestamp)
print(info['fecha'])
print(info['fecha'])
print("----------------------------------------------------------------------------------------------------------------------")
print(lat)
print("----------------------------------------------------------------------------------------------------------------------")
print(lon)
print("----------------------------------------------------------------------------------------------------------------------")
print(exif['GPSInfo'])
print("----------------------------------------------------------------------------------------------------------------------")
print(alt)
print("----------------------------------------------------------------------------------------------------------------------")
print(info)
print("----------------------------------------------------------------------------------------------------------------------")
# print(img._getexif().items())
