import psycopg2

#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------

def drop_pic_table():
    # query to create a database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''DROP TABLE pictures; ''')

    conn.commit()
    conn.close()
    
def drop_user_table():
    # query to create a database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''DROP TABLE users; ''')

    conn.commit()
    conn.close()

#already has been called dont need to call again
def create_pic_table():
    # query to create a database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pictures (
        pictureID int,
        coordinates float[2],
        link varchar(255), 
        chosen boolean);''')

    conn.commit()
    conn.close()
    
#-----------------------------------------------------------------------

#already has been called dont need to call again
def create_user_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()


    cur.execute('''CREATE TABLE users (
    username varchar(255),
    points int);''')

    conn.commit()
    conn.close()

#-----------------------------------------------------------------------

def insert_or_update_player(username, points):

    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Check if username exists
    cur.execute('''SELECT points FROM users WHERE username=%s;''', (username,))
    result = cur.fetchone

    if result is None:
        cur.execute('''INSERT INTO users (username, points) VALUES (%s, %s);''', (username, 0))
    else:
        cur.execute('''UPDATE users SET points=%s WHERE username=%s;''', (points, username))

    # Commit change and disconnect
    conn.commit()
    conn.close()

#-----------------------------------------------------------------------

def get_top_players():

    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    top_players = []
    cur.execute('''SELECT username, points FROM users ORDER BY points DESC LIMIT 10;''')
    table = cur.fetchall
    for row in table:
        username, points = row
        player_stats = {'username': username, 'points': points}
        top_players.append(player_stats)

    # Disconnect
    conn.close()

    return top_players

#-----------------------------------------------------------------------

def get_points(username):

    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT points FROM users WHERE username=%s;''', (username,))
    points = cur.fetchone

    # Disconnect
    conn.close()

    return points

#-----------------------------------------------------------------------

def query():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # create_pic_table(cur)
    # create_user_table(cur)

    cur.execute('''SELECT link FROM pictures;''')

    rows = cur.fetchall()

    link = rows[0][0]
    return link
    conn.commit()
    conn.close()

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

# def main():
    # connection establishment
    # Creating a cursor object
    # return query(cur)
    # create_user_table()
    # create_pic_table()
    # link = query()
    # return link

    # Closing the connection
    

    # print(query())
    