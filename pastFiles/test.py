

def dms_to_dd(d, m, s):
	dd = float(d) + float(m)/60 + float(s)/3600/1000
	return dd

def test(latit, lon):
	print lon[0:3]
	print lon[3:5]
	print lon[6:]
	finalLatit = dms_to_dd(latit[0:2],latit[2:4],latit[5:])
	finalLong = dms_to_dd(lon[0:3], lon[3:5],lon[6:])
	return finalLatit, finalLong

latit = '3404.12119'
lon = '11826.59633'
print test(latit, lon)