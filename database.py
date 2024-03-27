import psycopg2


DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

def create_pic_table(cur):
    # query to create a database 
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

def create_user_table(cur):
        cur.execute('''CREATE TABLE users (
        userID int,
        points int);''')
        cur.execute('''INSERT INTO users (userID, points) 
            VALUES ('1', '123');''')

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

def query(cur):
    create_pic_table(cur)
    # create_user_table(cur)

    cur.execute("SELECT link FROM pictures")

    rows = cur.fetchall()

    link = rows[0][0]
    return link
    
def main():
    # connection establishment
    conn = psycopg2.connect(DATABASE_URL)
    # Creating a cursor object
    cur = conn.cursor()
    return query(cur)

    # Closing the connection
    conn.close()

    # print(query())
    