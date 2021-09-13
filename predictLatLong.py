import math

#constants
r_earth = 6378100  #[m]
pi = 3.14
g = 9.18  #[m/s^2]
landing_alt = 2000  #[meters]
descent_rate = 4.56  # [m/s], not really constant but we will estimate it to be


# calcuate the new latitude using current latitude, y velocity and descent time
def calcLatitude(currLatitude, y_velocity, descent_time):
	y_distance = y_velocity * descent_time  #[m] calculate change in y-distance
	new_latitude = currLatitude + (y_distance / r_earth) * (
	    180 / pi)  #[degrees]calculate new latitude
	return new_latitude


# calculate the new longitude using current latiude and longitude, x_velocity and descent time
def calcLongitude(currLatitude, currLongitude, x_velocity, descent_time):
	x_distance = x_velocity * descent_time  # [m] calculate change in y-distance
	new_longitude = currLongitude + (x_distance / r_earth) * (
	    180 / pi) / math.cos(
	        currLatitude * pi / 180)  # [degree] calculate new longitude
	return new_longitude


#variables
curr_alt = 30480  #[meters], current altitude of the balloon
curr_lat = 35.04  #current latitude of the balloon
curr_long = -117.15  #current longitude of the balloon

#calculate the time to descent in the z direction, v=dx/dt -> dt=dx/v
descent_time = (curr_alt - landing_alt) / descent_rate

#calculate the intial velocity in the x and y direction
#v_x = difference in latitude/difference in time, between the last two packets
#v_y = difference in longitude/difference in time, between the last two packets
#just use arbitrary values for now
v_x = 2  #[m/s]
v_y = 2  #[m/s]

#calculate the landing position, x=x0+v0t+1/2at^2
pred_long_x = calcLongitude(curr_lat, curr_long, v_x, descent_time)
pred_lat_y = calcLatitude(curr_lat, v_y, descent_time)

print("Predicting latitude: ", pred_lat_y, "Predicting longitude: ",
      pred_long_x, "Time to descent: ", descent_time)
