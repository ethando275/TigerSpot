#-----------------------------------------------------------------------
# daily_user_database.py
#-----------------------------------------------------------------------

import psycopg2
import database

#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------

def create_daily_user_table():
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS usersDaily (
                                username varchar(255),
                                points int,
                                distance int,
                                played boolean,
                                last_played date,
                                current_streak int);''')
                conn.commit()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def insert_player_daily(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:

                cur.execute("SELECT points FROM usersDaily WHERE username=%s;", (username,))
                result = cur.fetchone()

                if result is None:
                    cur.execute("INSERT INTO usersDaily (username, points, distance, played, last_played, current_streak) VALUES (%s, %s, %s, %s, NULL, %s);", (username, 0, 0, False, 0))

                conn.commit()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

    
#-----------------------------------------------------------------------

def update_player_daily(username, points, distance):
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:

                cur.execute("SET TIME ZONE 'America/New_York';")

                cur.execute('''UPDATE usersDaily
                                SET 
                                    points=%s,
                                    distance=%s,
                                    played=%s,
                                    current_streak = CASE
                                        WHEN last_played IS NULL THEN 1 
                                        WHEN last_played::date = (CURRENT_DATE - INTERVAL '1 day')::date THEN current_streak + 1 
                                        ELSE 1
                                    END,                        
                                    last_played= CURRENT_DATE
                                WHERE username=%s;''', (points, distance, True, username))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def player_played(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:

                cur.execute("SELECT played FROM usersDaily WHERE username=%s;", (username, ))
                result = cur.fetchall()[0][0]

        return result

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"


#-----------------------------------------------------------------------

#resets the user's daily points
def reset_player(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE usersDaily SET played=%s, points=%s, distance=%s WHERE username=%s;", (False, 0, 0, username))
                print(f"Player {username} has been reset for the daily round")
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

# server wide player reset
def reset_players():

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE usersDaily SET played=%s, points=%s, distance=%s, last_played=NULL, current_streak = %s;", (False, 0, 0, 0))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_last_played_date(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT last_played FROM usersDaily WHERE username=%s;''', (username,))
                date = cur.fetchone()

        if date is None:
            return 0
    
        return date[0]
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_streak(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT current_streak FROM usersDaily WHERE username=%s;''', (username,))
                streak = cur.fetchone()

        if streak is None:
            return 0

        return streak[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_daily_points(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT points FROM usersDaily WHERE username=%s;''', (username,))
                points = cur.fetchone()

        if points is None:
            return 0

        return points[0]
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_daily_distance(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT distance FROM usersDaily WHERE username=%s;''', (username,))
                distance = cur.fetchone()

        if distance is None:
            return 0

        return distance[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_daily_top_players():

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                daily_top_players = []
                cur.execute("SET TIME ZONE 'America/New_York';")
                cur.execute("SELECT username, points FROM usersDaily WHERE last_played = CURRENT_DATE ORDER BY points DESC, username ASC LIMIT 10;")
                table = cur.fetchall()
                for row in table:
                    username, points = row
                    player_stats = {'username': username, 'points': points}
                    daily_top_players.append(player_stats)

        return daily_top_players

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_daily_rank(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SET TIME ZONE 'America/New_York';")
                cur.execute("SELECT username, points, DENSE_RANK() OVER (ORDER BY points DESC, username ASC) as rank FROM usersDaily WHERE last_played = CURRENT_DATE;")
                players = cur.fetchall()

        for player in players:
            if player[0] == username:
                return player[2]
        return "Play Today's Game!"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def remove_daily_user(username):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:

                cur.execute("DELETE FROM usersDaily WHERE username=%s;", (username,))
                conn.commit()
  
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def main():
    # update_player_daily('wn4759', 100, 30)
    #reset_player('cl7359')
    #reset_player('jy3107')
    #reset_player('fl9971')
    #print(get_last_played_date('fl9971'))
    #reset_player('wn4759')
    #reset_player('ed8205')
    # remove_daily_user('fl9971')
    #reset_player('jy1365')
    #create_daily_user_table()
    date = get_last_played_date('fl9971')
    print(date)
    streak = get_streak('fl9971')
    print(streak)
    date1 = get_last_played_date('cl7359')
    print(date1)

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()
