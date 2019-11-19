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
coords = [(25,30), (2,50), (14,9), (-10,8)]

# Check if coords are in or out of the Safety zone
def checkSafety(latit, longit):
	# Establish the region and create the polygon shape to check for coordinates
	poly = Polygon(coords)
	# Create the point and check if it is within our specified region
	point = Point(latit, longit)
	if (point.within(poly) == False):
		# Return -1 if coords are in the Danger zone
		return -1
	else:
		# Return 0 if coords are in the Safety zone
		return 0

def increment(val):
    return val + 1
