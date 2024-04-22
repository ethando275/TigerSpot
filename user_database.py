import psycopg2

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

def create_user_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    username varchar(255),
    points int);''')
    conn.commit()
    cur.close()
    conn.close()

def insert_player(username):

   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check if username exists
    cur.execute("SELECT points FROM users WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        cur.execute("INSERT INTO users (username, points) VALUES (%s, %s);", (username, 0,))

    # Commit change and disconnect
    conn.commit()
    conn.close()

def reset_player_total_points(username):

   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check if username exists
    cur.execute("SELECT points FROM users WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        return
    else:
        cur.execute("UPDATE users SET points=%s WHERE username=%s;", (0, username))
    # Commit change and disconnect
    conn.commit()
    print(f"Player {username} now has", get_points(username), "points")
    conn.close()

def update_player(username, points):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("UPDATE users SET points=%s WHERE username=%s;", (points, username))

    conn.commit()
    conn.close()


def get_points(username):

   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT points FROM users WHERE username=%s;''', (username,))
    points = cur.fetchone()

    # Disconnect
    conn.close()

    return points[0]


def get_rank(username):
    
   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    try: 
        cur.execute("SELECT username, points, DENSE_RANK() OVER (ORDER BY points DESC, username ASC) as rank FROM users;")
        players = cur.fetchall()
        
        for player in players:
            if player[0] == username:
                return player[2]
        return "Player not found"
    
    finally:
        conn.close()

    
def get_top_players():

    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    top_players = []
    cur.execute("SELECT username, points FROM users ORDER BY points DESC,  username ASC LIMIT 10;")
    table = cur.fetchall()
    for row in table:
        username, points = row
        player_stats = {'username': username, 'points': points}
        top_players.append(player_stats)

   # Disconnect
    conn.close()

    return top_players

    
def remove_from_user_table(username):
   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()


    cur.execute("DELETE FROM users WHERE username=%s;", (username,))
    conn.commit()

    # Disconnect
    conn.close()

def get_players():
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Execute query to fetch user IDs
    cur.execute("SELECT username FROM users;")
    table = cur.fetchall()
    user_ids = [row[0] for row in table]
    # Disconnect
    conn.close()

    return user_ids

def main():
    reset_player_total_points("cl7359")

if __name__=="__main__":
    main()