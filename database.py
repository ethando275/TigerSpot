import psycopg2
from geopy.distance import geodesic


DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'


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
        link = file.readline().strip()
        coordinates = {file.readline().strip, file.readline().strip}
        pictureID += 1
        chosen = False
        cur.execute('''INSERT INTO pictures (pictureID, coordinates, link, chosen) 
        VALUES (?, ?, ?, ? );''',
        (pictureID, link, coordinates, chosen))
    conn.commit()
    cur.close()
    conn.close()
# def update_user_table(userID, distance, cur):
#         if distance - 3 >= 0:
#             points = 100
#         elif distance - 10 >= 0:
#             points = 80
#         elif distance - 25 >= 0:
#             points = 50
#         else
#             points = 0
#         cur.execute('''UPDATE users
#             SET points = %d
#             WHERE userID = %s);
#             ''', (points, userID))
def create_user_table():
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE users (
        userID int,
        points int);''')

        cur.execute('''INSERT INTO users (userID, points) 
            VALUES ('1', '123');''')

def query(cur):
    create_pic_table(cur)
    # create_user_table(cur)

    cur.execute("SELECT link FROM pictures")

    rows = cur.fetchall()

    link = rows[0][0]
    return link
    conn.commit()
    cur.close()
    conn.close()

def get_distance():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT coordinates FROM pictures")
    rows = cur.fetchall()

    coor = rows[0][0]
    return coor
    conn.commit()
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

    cur.execute("SELECT * FROM pictures")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    conn.commit()
    cur.close()
    conn.close()
    
def main():
    # update()
    show_rows()
    # connection establishment
    # Creating a cursor object
    # return query(cur)
    # create_user_table()
    # create_pic_table()
    # link = query()
    # return link

    # Closing the connection
if __name__=="__main__": 
    main()

    # print(query())

    