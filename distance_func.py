#-----------------------------------------------------------------------
# distance_func.py
# This file contains functions relating distance calculation
#-----------------------------------------------------------------------
import psycopg2
from geopy.distance import geodesic

#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------

#Using the geopy library, we calculate the distance between two coordinates using the Haversine formula
#Measuring in meters
def calc_distance(lat1, lon1, coor2):
    coor1 = (lat1, lon1)
    distance = geodesic(coor1, coor2).meters
    return round(distance)

#-----------------------------------------------------------------------
def testing():
    #testing that calc_distance() calculates correct distance
    expected_distance = 751 #estimation using calculator
    calculated_distance = calc_distance(40.3487 , -74.6593, (40.3421, -74.6612))
    print("Expected distance:", expected_distance)
    print("Calculated distance:", calculated_distance)

    if(abs(expected_distance - calculated_distance) > 2):
        print("Error with distance calculation")

#-----------------------------------------------------------------------

def main():
    testing()
    
if __name__=="__main__":
    main()