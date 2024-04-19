import user_database
import daily_user_database

def calculate_today_points(distance):
    if distance - 15 <= 0:
        points = 1000
    elif distance - 25 <= 0:
        points = 750
    elif distance - 35 <= 0:
        points = 500
    elif distance - 45 <= 0:
        points = 250
    elif distance - 50 <= 0:
        points = 100
    else:
        points = 0

    return points

#-----------------------------------------------------------------------

def calculate_total_points(username, today_points):
    
    points = today_points + user_database.get_points(username)

    return points
