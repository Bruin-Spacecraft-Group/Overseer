
#Cd = 1.75
predictor = Predictor(40000, 17.5)
# CalculateLandingPosition(Latitude, Longitude, Altitude)
lat = 35.0 #current latitude
longi = -117.15
alt = 60000
time = 0
for i in range(1, 30):
  d = {'time': str(time) + str(i), 'lat': lat, 'lon': longi, 'alt': alt, 'sats': 5, 'fixtype': 0}
  lat += 1
  longi += 1
  alt += 100 #increasing altitude means ascending
  print(predictor.AddGPSPosition(d))

print("Predicting latitude: ", pred_x, "Predicting longitude: ", pred_y , "Time to descent: ", descent_time)
