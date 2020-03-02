import time

# The PITS outputs dms format for coordinates so we must convert to dd to read properly
def dms_to_dd(d, m, s):
	dd = float(d) + float(m)/60 + float(s)/3600/1000
	return dd

# Go to the end of gps.txt and grab valid lines, if not wait for a valid line
def follow(file):
	file.seek(0,2)
	while True:
		l = file.readline()
		if not l:
			time.sleep(0.1)
			continue
		yield l

# Leftover function for testing
def returntoGeo(finalLat, finalLon):
	return finalLat, finalLon

# Grab the lines from the follow() function, then split them nicely with .split(). Afterwards, just index the split string and extract GPS.
# Must include the break statement at the end or else the for loop will continue despite returning.
def generateCoords():
	logfile = open("/home/pi/pits/tracker/gps.txt", "r")
	loglines = follow(logfile)
	for line in loglines:
		splitLine = line.split(",")
		if splitLine[0] == "$GNGGA":
			currLat = splitLine[2]
			currLon = splitLine[4]
			finalLat = dms_to_dd(currLat[0:2], currLat[2:4], currLat[5:])
			finalLon = -1*dms_to_dd(currLon[0:3], currLon[3:5],currLon[6:])
			return finalLat, finalLon
			break
