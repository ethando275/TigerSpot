#-----------------------------------------------------------------------
# user_database.py
#-----------------------------------------------------------------------

import psycopg2

#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------

def create_user_table():

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS users (
                username varchar(255),
                points int);''')
                conn.commit()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"
    
#-----------------------------------------------------------------------

def insert_player(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Check if username exists
                cur.execute("SELECT points FROM users WHERE username=%s;", (username,))
                result = cur.fetchone()

                if result is None:
                    cur.execute("INSERT INTO users (username, points) VALUES (%s, %s);", (username, 0,))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def reset_player_total_points(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Check if username exists
                cur.execute("SELECT points FROM users WHERE username=%s;", (username,))
                result = cur.fetchone()

                if result is None:
                    return
                else:
                    cur.execute("UPDATE users SET points=%s WHERE username=%s;", (0, username))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"


#-----------------------------------------------------------------------

def update_player(username, points):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET points=%s WHERE username=%s;", (points, username))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_points(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT points FROM users WHERE username=%s;''', (username,))
                points = cur.fetchone()

        return points[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_rank(username):
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, points, DENSE_RANK() OVER (ORDER BY points DESC, username ASC) as rank FROM users;")
                players = cur.fetchall()
        
        for player in players:
            if player[0] == username:
                return player[2]
        return "Player not found"
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_top_players():

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:

                top_players = []
                cur.execute("SELECT username, points FROM users ORDER BY points DESC,  username ASC LIMIT 10;")
                table = cur.fetchall()
                for row in table:
                    username, points = row
                    player_stats = {'username': username, 'points': points}
                    top_players.append(player_stats)

        return top_players

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------
    
def remove_from_user_table(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE username=%s;", (username,))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def get_players():

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users;")
                table = cur.fetchall()
                user_ids = [row[0] for row in table]
        return user_ids
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def main():
    print(get_top_players())

if __name__=="__main__":
    main()
