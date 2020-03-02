from shapely.geometry import Point, Polygon

# test cases
#outside of region
# p1 = Point(34.614549, -118.560853)
#within region
# p2 = Point(34.542620, -117.883676)
# p3 = Point(34.528728, -117.922478)
# p4 = Point(34.540518, -117.940722)
# p5 = Point(34.547257, -117.919958)
# p6 = Point(34.566803, -117.916212)
coords = [(34.398664,-117.989882), (34.65823,-117.924462), (34.586997,-117.510929), (34.346296,-117.557277)]

# Check if coords are in or out of the Danger zone
def inDangerZone(latit, longit):
	# Establish the region and create the polygon shape to check for coordinates
	poly = Polygon(coords)
	# Create the point and check if it is within our specified region
	point = Point(latit, longit)
	if (point.within(poly) == False):
		# Return True if coords are in the Danger zone
		return True
	else:
		# Return False if coords are in the Safety zone
		return False
