import user_database
import daily_user_database
import math

def calculate_today_points(distance):
    # if distance - 15 <= 0:
    #     points = 1000
    # elif distance - 25 <= 0:
    #     points = 750
    # elif distance - 35 <= 0:
    #     points = 500
    # elif distance - 45 <= 0:
    #     points = 250
    # elif distance - 50 <= 0:
    #     points = 100
    # else:
    #     points = 0
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

#-----------------------------------------------------------------------

def calculate_total_points(username, today_points):
    
    points = today_points + user_database.get_points(username)

    return points

def test_point_distribution(distance):
    print(f"If distance is {distance}, then points is", calculate_today_points(distance))

def main():
    test_point_distribution(0)
    test_point_distribution(50)
    test_point_distribution(90)
    test_point_distribution(100)
    test_point_distribution(1000)

    
if __name__=="__main__":
    main()
