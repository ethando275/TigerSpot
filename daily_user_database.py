import psycopg2
import database

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'


def create_daily_user_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS usersDaily (
    username varchar(255),
    points int,
    distance int,
    played boolean,
    last_played date,
    current_streak int);''')
    conn.commit()
    cur.close()
    conn.close()

def insert_player_daily(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT points FROM usersDaily WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        cur.execute("INSERT INTO usersDaily (username, points, distance, played, last_played, current_streak) VALUES (%s, %s, %s, %s, NULL, %s);", (username, 0, 0, False, 0))

    conn.commit()
    conn.close()

def update_player_daily(username, points, distance):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("SET TIME ZONE 'America/New_York';")

    cur.execute('''UPDATE usersDaily
                SET 
                points=%s,
                distance=%s,
                played=%s,
                last_played= CURRENT_DATE,
                current_streak = CASE
                    WHEN last_played IS NULL THEN 1 
                    WHEN last_played = CURRENT_DATE - INTERVAL '1 day' THEN current_streak + 1 
                    ELSE 1 
                END
                WHERE username=%s;''', (points, distance, True, username))
    print("EXECUTED DAILY UPDATE")
    conn.commit()
    conn.close()

#-----------------------------------------------------------------------

def player_played(username):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT played FROM usersDaily WHERE username=%s;", (username, ))
    result = cur.fetchall()[0][0]

    conn.close()

    return result

#-----------------------------------------------------------------------

#resets the user's daily points
def reset_player(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("UPDATE usersDaily SET played=%s, points=%s, distance=%s WHERE username=%s;", (False, 0, 0, username))

    conn.commit()
    conn.close()
#-----------------------------------------------------------------------

# server wide player reset
def reset_players():

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("UPDATE usersDaily SET played=%s;", (False, ))

    conn.commit()
    conn.close()

#-----------------------------------------------------------------------

def get_last_played_date(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT last_played FROM usersDaily WHERE username=%s;''', (username,))
    date = cur.fetchone()

    conn.close()

    if date is None:
        return 0

    return date[0]
    
#-----------------------------------------------------------------------

def get_streak(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT current_streak FROM usersDaily WHERE username=%s;''', (username,))
    streak = cur.fetchone()

    conn.close()

    if streak is None:
        return 0

    return streak[0]
#-----------------------------------------------------------------------
    
def get_daily_points(username):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT points FROM usersDaily WHERE username=%s;''', (username,))
    points = cur.fetchone()
    
    # Disconnect
    conn.close()
    
    if points is None:
        return 0
    
    return points[0]

#-----------------------------------------------------------------------

def get_daily_distance(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT distance FROM usersDaily WHERE username=%s;''', (username,))
    distance = cur.fetchone()
    
    # Disconnect
    conn.close()
    
    if distance is None:
        return 0
    
    return distance[0]

#-----------------------------------------------------------------------

def get_daily_top_players():

    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    daily_top_players = []
    cur.execute("SELECT username, points FROM usersDaily WHERE last_played = CURRENT_DATE ORDER BY points DESC, username ASC LIMIT 10;")
    table = cur.fetchall()
    for row in table:
        username, points = row
        player_stats = {'username': username, 'points': points}
        daily_top_players.append(player_stats)

   # Disconnect
    conn.close()

    return daily_top_players

#-----------------------------------------------------------------------

def get_daily_rank(username):
    
   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    try: 
        cur.execute("SELECT username, points, DENSE_RANK() OVER (ORDER BY points DESC, username ASC) as rank FROM usersDaily WHERE last_played = CURRENT_DATE;")
        players = cur.fetchall()
        
        for player in players:
            if player[0] == username:
                return player[2]
        return "Play Today's Game!"
    
    finally:
        conn.close()

#-----------------------------------------------------------------------

def remove_daily_user(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("DELETE FROM usersDaily WHERE username=%s;", (username,))

    conn.commit()
    conn.close()

def main():
    # update_player_daily('wn4759', 100, 30)
    #reset_player('cl7359')
    reset_player('wn4759')
    remove_daily_user('wn4759')
    ##reset_player('jy1365')
    #create_daily_user_table()
    # date = get_last_played_date('fl9971')
    # print(date)

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()
