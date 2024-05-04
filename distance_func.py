#-----------------------------------------------------------------------
# distance_func.py
# This file contains functions relating distance calculation
#-----------------------------------------------------------------------
import psycopg2
from geopy.distance import geodesic

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'
#-----------------------------------------------------------------------

#Using the geopy library, we calculate the distance between two coordinates using the Haversine formula
def calc_distance(lat1, lon1, coor2):
    coor1 = (lat1, lon1)
    distance = geodesic(coor1, coor2).meters
    return distance