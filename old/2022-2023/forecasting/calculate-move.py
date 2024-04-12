"""

does the calculations based on data collected in previous step
*assumes we get altitude, latitude, and longitude from sensors

"""

from datetime import datetime, timedelta

#placeholders!!
alt = 1001
lat = 34.285714
lng = -115.4
time = datetime.utcnow()+timedelta(hours=-7)

#round to nearest table value
alt = 1000*round(alt/1000) + 5
lat = round(0.142857*round((lat-33)/0.142857) + 33, 5)
lng = round(0.357143*round((lng+120)/0.357143) -120, 5)
time = (time - timedelta(minutes=time.minute % 10, seconds=time.second)).strftime("%Y-%m-%dT%H:%M:%SZ")

#note that data is ordered, so instead of doing search it'd be more efficient to calculate index
#first layer varies by altitude
  #then we want data
    #then we have to check the parameter (for speed or dir)
    #then in coordinates
      #lat
      #lng
      #then in dates
        #date
        #then finally value
"""
[round(alt/1000)]['data']['coordinates'][round((lat-33)/0.142857)*15 + round((lng+120)/0.357143)]['dates'][something w time]
"""
#I should've just used a csv lmao



#gets wind speed and direction from wind.json
with open('wind.json') as file:
    data = json.load(file)
wspeed = data[0]['data']
print(wspeed)

#puts in terms of x/y direction

#does some calculations to find force

#predicts next location
