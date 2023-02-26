import matplotlib.pyplot as plt
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import geopandas as gpd


def baseFromPoint(x, y):
    point = Point(x, y)

    foundIndex = -1
    for i, polygon in enumerate(reds):
        if polygon.contains(point):
            foundIndex = i

    if (foundIndex == -1):
        return None
    else:
        return site_dict[foundIndex]


# load data
data = gpd.read_file('military-bases.shp')

# list of redzones
reds = []

# dictionary of site ids and names
site_dict = dict()

index = 0
for i in range(len(data["geometry"])):
    if (data["geometry"][i] is not None and data["oper_stat"][i] != "Inactive"):

        reds.append(data["geometry"][i])
        site_dict[index] = {"id": data["objectid"]
                            [i], "name": data["site_name"][i]}
        index += 1

# check if a point is in the polygon

# lon, lat
x, y = -121.397, 38.682
point = Point(x, y)

tf = False
poly = None
for i, x in enumerate(reds):
    if x.contains(point):
        tf = True
        poly = x
        print("Pos in Reds:", i)
print("In Red:", tf)

# visualize

plt.plot(*poly.exterior.xy)
plt.scatter(*point.xy, color='r')
plt.show()
