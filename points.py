#-----------------------------------------------------------------------
# points.py
#-----------------------------------------------------------------------

import user_database

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
        points = max(0, 1 - (distance / 100)) * 1000
    # rounding due to Python's floating point arithmetic precision error
    # https://python.plainenglish.io/floating-point-arithmetic-precision-error-in-python-decimal-comes-for-rescue-8803d1290601 
    # due to the nature of our point system, we found that it would be easier to round rather than use the Decimal library as that could cause type errors
    return round(points)

# Returns a player's updated cummulative points after their daily guess
def calculate_total_points(username, today_points):
    points = today_points + user_database.get_points(username)
    return round(points)

#-----------------------------------------------------------------------

def test_point_distribution(distance):
    print(f"If distance is {distance}, then points is", calculate_today_points(distance))

#-----------------------------------------------------------------------

def testing():
    # [0,3) meters
    assert calculate_today_points(0) == 1500 
    assert calculate_today_points(2) == 1500 
    assert calculate_today_points(2.999999999999) == 1500 
    # [3,6) meters
    assert calculate_today_points(3) == 1250 
    assert calculate_today_points(3.0) == 1250 
    assert calculate_today_points(3.00000000001) == 1250 
    assert calculate_today_points(5.999999999) == 1250
    # [6, 10) meters
    assert calculate_today_points(6) == 1000 
    assert calculate_today_points(6.00000000001) == 1000 
    assert calculate_today_points(9.9999999999999) == 1000 
    # >= 10 meters, points will linearly decrease with distance
    assert calculate_today_points(10) == 1000
    assert calculate_today_points(100) == 100 
    #technically this is within 110 meters but since we round to the nearest integer for both distance and rounding calculations
    #this would become 110 meters and result in 0 points
    assert calculate_today_points(109.9999999) == 0 
    assert calculate_today_points(110) == 0 

    # testing calculation for adding points to a user 
    cummulative_points = calculate_total_points('wn4759', 0)
    print("Cummulative points before adding daily points:", cummulative_points)
    cummulative_points = calculate_total_points('wn4759', 1000)
    print("Cummulative points after adding 1000 points:", cummulative_points)


def main():
    testing()

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()
