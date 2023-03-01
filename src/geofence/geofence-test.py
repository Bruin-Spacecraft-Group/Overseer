import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import wkt

reds = pd.read_csv('~/Overseer/src/geofence/reds.csv')
reds['shape'] = reds['shape'].apply(wkt.loads)

# feed gps coords here
lon,lat = -121.397, 38.682
point = Point(lon, lat)

for i,x in enumerate(reds['shape']):
  if x.contains(point):
    print("In Red:", reds['name'][i], 'at (lon, lat):', lon,',',lat)
