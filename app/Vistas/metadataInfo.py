from PIL import Image, ExifTags
from datetime import datetime as dt

def metadataInfo(image):
	"""docstring for metadataInfo"""
	
	# img = Image.open("./arboles_00.jpg")
	img = Image.open(image)

	info = {}
	getExif = img._getexif()
	if not getExif:
		info['lat'] = ' '
		info['lon'] = ' '
		info['altitud'] =' '
		info['width'] = ' '
		info['height'] = ' '
		info['fecha'] = ' '
		return info

	exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }

	lat = [float(x) / float(y) for x, y in exif['GPSInfo'][2]]
	lon = [float(x) / float(y) for x, y in exif['GPSInfo'][4]]
	alt = float(exif['GPSInfo'][6][0]) / float(exif['GPSInfo'][6][1])
	timestamp = exif['DateTimeOriginal']

	info['lat'] = (lat[0] + lat[1] / 60)
	info['lon'] = (lon[0] + lon[1] / 60)
	info['altitud'] = alt

	if exif['GPSInfo'][1] == "S":
	        info['lat'] *= -1
	if exif['GPSInfo'][3] == "W":
	    info['lon'] *= -1
	# if we're below sea level, the value's negative
	if exif['GPSInfo'][5] == 1:
		info['altitud'] *= -1

	info['width'] = exif['ExifImageWidth']
	info['height'] = exif['ExifImageHeight']
	info['fecha'] = dt.strptime(timestamp, "%Y:%m:%d %H:%M:%S").strftime("%d/%m/%Y")

	return info