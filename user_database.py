#-----------------------------------------------------------------------
# user_database.py
#-----------------------------------------------------------------------

import psycopg2

#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------

# Creates users table with columns username and points.

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

# Inserts username into users table.

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
                
        return "success"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

# Resets username's total points to 0.

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
                
        return "success"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"


#-----------------------------------------------------------------------

# Updates username's total points with points.

def update_player(username, points):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET points=%s WHERE username=%s;", (points, username))
                conn.commit()
                
        return "success"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

# Returns username's points.

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

# Returns username's total rank among all players.

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

# Returns a dictionary of the usernames and points of the the top 10
# scoring players.

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

# Removes username from the users table.

def remove_from_user_table(username):

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE username=%s;", (username,))
                conn.commit()
                
        return "success"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

# Returns all players in users table.

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

# Returns number one player's username and points

def get_top_player():

    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                
                cur.execute("SELECT username, points FROM users ORDER BY points DESC,  username ASC LIMIT 1;")
                table = cur.fetchall()
                for row in table:
                    username, points = row
                    player_stats = {'username': username, 'points': points}

        return player_stats

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

def main():
    print(get_top_players())
    print(get_top_player())
    print(get_players())
    print(insert_player('test'))
    print(update_player('test', 30000))
    print(get_points('test'))
    print(get_rank('test'))
    print(get_top_players())
    print(reset_player_total_points('test'))
    print(get_points('test'))
    print(get_rank('test'))
    print(remove_from_user_table('test'))
    print(get_players())

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()