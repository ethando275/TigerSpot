#-----------------------------------------------------------------------
# points.py
#-----------------------------------------------------------------------

import user_database
import daily_user_database
import math

#-----------------------------------------------------------------------

# Returns points based on distance from actual coordinates
def calculate_today_points(distance):
    if distance < 3:
        points = 1500
    elif distance < 6:
        points = 1250
    elif distance < 10:
        points = 1000
    else:
        distance -= 10
        points = max(0, 1 - distance / 100) * 1000
    return points

# Returns a player's updated cummulative points after their daily guess
def calculate_total_points(username, today_points):
    points = today_points + user_database.get_points(username)
    return points

#-----------------------------------------------------------------------

def test_point_distribution(distance):
    print(f"If distance is {distance}, then points is", calculate_today_points(distance))

#-----------------------------------------------------------------------

def main():
    
    test_point_distribution(0) # 1500
    test_point_distribution(3) # 1250
    test_point_distribution(6) # 1000
    test_point_distribution(10) # ~1000
    test_point_distribution(100) # ~100
    test_point_distribution(110) # 0

    cummulative_points = calculate_total_points('wn4759', 0)
    print(cummulative_points)
    cummulative_points = calculate_total_points('wn4759', 1000)
    print(cummulative_points)

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()
