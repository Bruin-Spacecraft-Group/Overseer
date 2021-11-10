from prediction import *

# from google.colab import drive
# drive.mount('/content/drive')

import pandas as pd
from collections import defaultdict
from shapely.geometry import Point, Polygon

def createZones(): 
    PATH = "/content/drive/Shareddrives/Bruin Space/Projects/Overseer/2020-2021/Spring/Software/NewCoords"
    COORDS = "Polygon/outerBoundaryIs/LinearRing/coordinates"
    region_0 = pd.read_csv(f"{PATH}/Square 0.csv")[COORDS]
    region_1 = pd.read_csv(f"{PATH}/Square 1.csv")[COORDS]
    region_3 = pd.read_csv(f"{PATH}/Square 3.csv")[COORDS]
    region_4 = pd.read_csv(f"{PATH}/Square 4.csv")[COORDS]
    region_5 = pd.read_csv(f"{PATH}/Square 5.csv")[COORDS]
    region_8 = pd.read_csv(f"{PATH}/Square 8.csv")[COORDS]
    region_9 = pd.read_csv(f"{PATH}/Square 9.csv")[COORDS]
    regions = [region_0, region_1, region_3, region_4, region_5, region_8, region_9]

    zones = []
    for region in regions: 
        for i, coords in enumerate(region): 
            shape = []
            for s in coords.split():
                geo = s.split(",")
                shape.append(Point(float(geo[1]), float(geo[0])))
            zones[i] = Polygon(shape)
    return zones

def cutdown(): 
    print("CUTTING DOWN...")
    exit()

class Simulation():
  def __init__(self, latitude, longitude, altitude):
    self.latitude = latitude
    self.longitude = longitude
    self.altitude = altitude
    self.zones = createZones()

  def move(self):
    self.latitude -= 0.1
    self.longitude -= 0.2
    self.altitude += 1
  
def run_tests(x, y):
    pred = Predictor(40000, 17.5)
    sim = Simulation(35.3084, -118.57268, 30000)
    
    def check_within_red(current): #Check if the balloon is inside a red zone based upon above regions
        for shape in sim.zones:
            if current.within(sim.zones[shape]):
                return True
        return False

    def update_loc(c):
        pred.AddGPSPosition(c)
        return Point(pred.PreviousPosition['lat'], pred.PreviousPosition['lon'])

    stop = 0
    while True:
        while sim.altitude < pred.MaximumAltitude: #not yet at max altitude
            sim.move()
            continue
        while check_within_red(update_loc(pred)):
            sim.move()
            continue 
        while True: # the balloon is in a white zone and also above max altitude
            if check_within_red(update_loc(pred)):
                sim.move()
                cutdown()
                stop = 1
                break
        if stop:
            break

"""
What is happening?
# Case 1: In red zone & at max alt --> KEEP going until the balloon exits its current red zone --> cut down when it enters another red zone
# Case 2: In white zone & at max alt --> cut down when it enters a red zone

"""

run_tests(35.3084, -118.57268)

