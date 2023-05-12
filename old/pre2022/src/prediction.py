from enum import Enum
from math import pow, exp, sqrt

# Flight Modes
class FlightMode(Enum):
    fmIdle          = 0
    fmLaunched      = 1
    fmDescending    = 2
    fmLanded        = 3

# GPS Position Object
class Delta():
    def __init__(self, latitude, longitude):
        self.latitude = latitude 
        self.longitude = longitude
        
""" 
@param
int LandingAltitude
float DefaultCDA = 0.7

FAQ:
What is a slot?
A section of the max altitude (default: 60,000km) of height (slotSize).

"""
class Predictor(object):
    def __init__(self, LandingAltitude, DefaultCDA):

        # slots
        self.SlotSize = 100
        self.Deltas = []
        self.FlightMode = FlightMode.fmIdle
        self.PreviousPosition = {'time': '00:00:00', 'lat': 0.0, 'lon': 0.0, 'alt': 0, 'sats': 0, 'fixtype': 0}

        # altitude
        self.MinimumAltitude = 0
        self.MaximumAltitude = 0
        self.AscentRate = 0

        # landing
        self.LandingAltitude = LandingAltitude
        self.LandingLatitude = 0.0
        self.LandingLongitude = 0.0
        self.PollPeriod = 5
        self.Counter = 0
        self.CDA = DefaultCDA

        # initialize Deltas (lat:0, long:0)
        for _ in range(60000 // self.SlotSize):
            self.Deltas.append(Delta(0,0))


    """
    Fetch the current slot based on current balloon's altitude.
    """
    def GetSlot(self, Altitude):
        return max(0, min(int(Altitude // self.SlotSize), self.SlotSize-1))

    """
    Calculate air density based on altitude.
    Parameters (temperature, pressure) can be modified depending on current environment by altitude.
    """
    def CalculateAirDensity(self, Altitude):

        if Altitude < 11000.0:
            # Troposphere
            temperature = 15.04 - (0.00649 * Altitude)
            pressure = 101.29 * pow((temperature + 273.1) / 288.08, 5.256)

        elif Altitude < 25000.0:
            # lower Stratosphere
            temperature = -56.46
            pressure = 22.65 * exp(1.73 - ( 0.000157 * Altitude))

        else:
            # upper Stratosphere
            temperature = -131.21 + (0.00299 * Altitude)
            pressure = 2.488 * pow((temperature + 273.1) / 216.6, -11.388)

        return pressure / (0.2869 * (temperature + 273.1))

    """
    Calculate descent rate based on altitude.
    A positive descent rate suggest a falling trajectory.
    """
    def CalculateDescentRate(self, Weight, CDTimesArea, Altitude):
        Density = self.CalculateAirDensity(Altitude)
	
        return sqrt((Weight * 9.81)/(0.5 * Density * CDTimesArea))


    """
    Return CDA.
    Recalculate CDA if Descent Rate is positive (currently falling).
    """    
    def CalculateCDA(self, Weight, Altitude, DescentRate):
        if DescentRate > 0.0:
            Density = self.CalculateAirDensity(Altitude)

            return (Weight * 9.81)/(0.5 * Density * DescentRate * DescentRate)
        else:
            return self.CDA
            
    
    def CalculateLandingPosition(self, Latitude, Longitude, Altitude):

        # Estimation of time 
        TimeTillLanding = 0
	
        # Get current slot from altitude.
        Slot = self.GetSlot(Altitude)

        # Determine the current altitude's distance from the boundaries of its matching slot.        
        DistanceInSlot = Altitude + (1 - (Slot * self.SlotSize))
	
        
        while Altitude > self.LandingAltitude:

            # Refetch the next slot
            Slot = self.GetSlot(Altitude)
		
            # If the altitude is within the boundaries of the landing altitude slot, calculate the offset distance.
            if Slot == self.GetSlot(self.LandingAltitude):
                DistanceInSlot = Altitude - self.LandingAltitude
		
            # Approximate the time of descent to close that offset.
            DescentRate = self.CalculateDescentRate(1.0, self.CDA, Altitude)
            TimeInSlot = DistanceInSlot / DescentRate
            
            
            Latitude += self.Deltas[Slot].latitude * TimeInSlot
            Longitude += self.Deltas[Slot].longitude * TimeInSlot
            
            # Set parameters to the slot.
            TimeTillLanding += TimeInSlot
            Altitude -= DistanceInSlot
            DistanceInSlot = self.SlotSize
                    
        # Return prediction results once balloon reaches landing altitude (+ sync w/ cutdown).
        return {'pred_lat': Latitude, 'pred_lon': Longitude ,'TTL': TimeTillLanding}

    """
    Add current position.
    Record geolocational data to recalculate new landing approximation.
    """
    def AddGPSPosition(self, Position):
       
        Result = None
        
        # Default: set all Position['sats'] = 4
        if Position['sats'] >= 4:

            # Only recalculate within one poll period.
            self.Counter += 1

            if self.Counter >= self.PollPeriod:
                self.Counter = 0
                
                
                # Calculate ascent rate.
                if Position['alt'] <= 0:
                    self.AscentRate = 0
                else:
                    self.AscentRate = self.AscentRate * 0.7 + (Position['alt'] - self.PreviousPosition['alt']) * 0.3

                # Calculate minimum altitude based on altitude.
                if (Position['alt'] < self.MinimumAltitude) or (self.MinimumAltitude == 0):
                    self.MinimumAltitude = Position['alt']
                    
                # Calculate maximum altitude based on altitude.
                if Position['alt'] > self.MaximumAltitude:
                    self.MaximumAltitude = Position['alt']               

                """
                Balloon has launched if:
                * Ascent rate >= 1.0
                * Current altitude exceeds the minimum by 150 (can be changed).
                * The current mode is fmIdle (on start-up).
                """
                if (self.AscentRate >= 1.0) and (Position['alt'] > (self.MinimumAltitude+150)) and (self.FlightMode == FlightMode.fmIdle):
                    self.FlightMode = FlightMode.fmLaunched
                    print("*** [STATUS]: BALLOON LAUNCHED! ***")
            
                """
                Balloon has descended if:
                * Ascent rate < -10.0
                * The balloon's maximum altitude is greater than the minimum by 2,000 (can be changed).
                    * Why? We want to ensure that it has flown for an approximate height upwards (along its ascent, it could fluctuate in ascent rate).
                * The current mode is fmLaunched (it has already ascended).
                """
                if (self.AscentRate < -10.0) and (self.MaximumAltitude >= (self.MinimumAltitude+2000)) and (self.FlightMode == FlightMode.fmLaunched):
                    self.FlightMode = FlightMode.fmDescending
                    print("*** [STATUS]: BALLOON DESCENDING! ***")

                """
                Balloon has landed if:
                * Ascent rate >= -0.1 (stopped falling essentially).
                * The balloon's altitude is less than the landing altitude + 2000 (can be changed).
                    * We want to add the constant for "cushion" (dependent on poll period and environment).
                * The current mode is fmDescending (it has begun to descend/fall).
                """
                if (self.AscentRate >= -0.1) and (Position['alt'] <= self.LandingAltitude+2000) and (self.FlightMode == FlightMode.fmDescending):
                    self.FlightMode = FlightMode.fmLanded
                    print("*** [STATUS]: BALLOON LANDING ***")
                   



                """ 
                [PREDICTION TUNING]
                """  
                if self.FlightMode == FlightMode.fmLaunched:

                    # Get average slot of the two altitudes.
                    Slot = self.GetSlot(Position['alt']/2 + self.PreviousPosition['alt']/2)
                        
                    # Deltas are scaled to be speed per second.
                    self.Deltas[Slot].latitude = (Position['lat'] - self.PreviousPosition['lat']) / self.PollPeriod
                    self.Deltas[Slot].longitude = (Position['lon'] - self.PreviousPosition['lon']) / self.PollPeriod
                    
                    print("Slot " + str(Slot) + " = " + str(Position['alt']) + "," + str(self.Deltas[Slot].latitude) + "," + str(self.Deltas[Slot].longitude))
               

                elif self.FlightMode == FlightMode.fmDescending:
                    self.CDA = (self.CDA * 4 + self.CalculateCDA(1.0, Position['alt']/2 + self.PreviousPosition['alt']/2, (self.PreviousPosition['alt'] - Position['alt']) / self.PollPeriod)) / 5
                
                
                # Calculate landing prediction on ascent & descent.
                if (self.FlightMode == FlightMode.fmLaunched) or (self.FlightMode == FlightMode.fmDescending):
                    Result = self.CalculateLandingPosition(Position['lat'], Position['lon'], Position['alt'])

                print('PREDICTOR: ' + str(Position['time']) + ', ' + "{:.5f}".format(Position['lat']) + ', ' + "{:.5f}".format(Position['lon']) + ', ' + str(Position['alt']) + ', ' + str(Position['sats']))

                self.PreviousPosition = Position.copy()
                
        return Result