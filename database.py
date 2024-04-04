import datetime
import psycopg2
from geopy.distance import geodesic


DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

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

    pictureID = 0

    with open('picturedata.txt', 'r') as file:
        while True:
            link = file.readline().strip()

            if not link:
                break 
            coordinates = [float(file.readline().strip()), float(file.readline().strip())]
            pictureID += 1
            chosen = False
            cur.execute(''' INSERT INTO pictures (pictureID, coordinates, link, chosen) 
            VALUES (%s, %s, %s, %s);
            ''', (pictureID, coordinates, link, chosen))
        # cur.execute(f'''INSERT INTO pictures (pictureID, coordinates, link, chosen) 
        # VALUES ({pictureID}, {coordinates}, '{link}', {chosen});''')
    conn.commit()
    cur.close()
    conn.close()

def create_user_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    username varchar(255),
    points int,
    played boolean);''')

        # cur.execute('''INSERT INTO users (userID, points) 
        #     VALUES ('1', '123');''')


    conn.commit()
    cur.close()
    conn.close()

def insert():
   conn = psycopg2.connect(DATABASE_URL)
   cur = conn.cursor()

   #this is alr inserted into table so change before executing so we dont have duplicates
#    cur.execute('''INSERT INTO pictures (pictureID, coordinates, link, chosen)
#    VALUES ('1', '{40.34805, -74.65570}',
#    'https://res.cloudinary.com/dmiaxw4rr/image/upload/c_pad,b_auto:predominant,fl_preserve_transparency/v1710781520/TigerSpot/IMG_9697_kf2cim.jpg?_s=public-apps',
#    'False');''')

   conn.commit()
   cur.close()
   conn.close()

def update():
   conn = psycopg2.connect(DATABASE_URL)
   cur = conn.cursor()
   # cur.execute("UPDATE pictures SET coordinates = [40.34805, -74.65570] WHERE pictureID = 1;")
    #sql = """UPDATE pictures
    # SET coordinates = '{40.34805, -74.65570}'
    #WHERE pictureID = 1;"""
   cur.execute(sql)
   # cur.execute('''UPDATE pictures
   # SET coordinates = {40.34805, -74.65570}
   # WHERE pictureID = 1;''')

   conn.commit()
   cur.close()
   conn.close()

def query(col, table):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # create_pic_table()
    # create_user_table()

    cur.execute(f"SELECT {col} FROM {table}")

    rows = cur.fetchall()

    row = rows[0][0]
    return row
    # conn.commit()
    cur.close()
    conn.close()

def get_pic_info(col, id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # create_pic_table()
    # create_user_table()

    cur.execute(f"SELECT {col} FROM pictures WHERE pictureID = {id}")

    rows = cur.fetchall()

    row = rows[0][0]
    return row
    # conn.commit()
    cur.close()
    conn.close()


def get_distance():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT coordinates FROM pictures")
    rows = cur.fetchall()

    coor = rows[0][0]
    return coor
    # conn.commit()
    cur.close()
    conn.close()

def calc_distance(lat1, lon1, coor2):
    coor1 = (lat1, lon1)
    distance = geodesic(coor1, coor2).meters
    return distance
    
# def calc_points():
def show_rows():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    cur.execute("SELECT * FROM pictures;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # conn.commit()
    cur.close()
    conn.close()
    
def insert_player(username, points):

   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check if username exists
    cur.execute("SELECT points FROM users WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        cur.execute("INSERT INTO users (username, points, played) VALUES (%s, %s, %s);", (username, 0, False))

    # Commit change and disconnect
    conn.commit()
    conn.close()

def calculate_points(username, distance):
    if distance - 3 <= 0:
        points = 100
    elif distance - 10 <= 0:
        points = 80
    elif distance - 25 <= 0:
        points = 50
    else:
        points = 0

    return points

def update_player(username, points):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    points = points + get_points(username)[0]

    cur.execute("UPDATE users SET points=%s, played=%s WHERE username=%s;", (points, True, username))

    conn.commit()
    conn.close()

def reset_players():

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("UPDATE users SET played=%s;", (False, ))

    conn.commit()
    conn.close()

   
def get_top_players():

    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    top_players = []
    cur.execute("SELECT username, points FROM users ORDER BY points DESC LIMIT 10;")
    table = cur.fetchall()
    for row in table:
        username, points = row
        player_stats = {'username': username, 'points': points}
        top_players.append(player_stats)

   # Disconnect
    conn.close()

    return top_players

def get_points(username):

   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT points FROM users WHERE username=%s;''', (username,))
    points = cur.fetchone()

    # Disconnect
    conn.close()

    return points

def remove_from_user_table(username):
   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()


    cur.execute("DELETE FROM users WHERE username=%s;", (username,))
    conn.commit()

    # Disconnect
    conn.close()

    
def main():
    # update()
    # create_pic_table()
    # create_user_table()
    # show_rows()
    # insert()
    # connection establishment
    # Creating a cursor object
    # return query(cur)
    # create_user_table()
    # create_pic_table()
    # link = query()
    # return link
    #print(get_points('fl9971'))
    #drop_pic_table()
    #create_pic_table()
    #drop_user_table()
    #create_user_table()
    # insert_player('wn4759', 0)
    # insert_player('ed8205', 0)
    # insert_player('fl9971', 0)
    # insert_player('cl7359', 0)
    # insert_player('ys6592', 0)
    # insert_player('jy3107', 0)

    show_rows()
    

    # Closing the connection
if __name__=="__main__":
    main()

    # print(query())

    