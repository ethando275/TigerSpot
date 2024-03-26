import psycopg2


DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#already has been called dont need to call again
def create_pic_table():
    # query to create a database 
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE pictures (
        pictureID int,
        coordinates float[2],
        link varchar(255), 
        chosen boolean);''')

    conn.commit()
    conn.close()

#already has been called dont need to call again
def create_user_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()


    cur.execute('''CREATE TABLE users (
    userID int,
    points int);''')

    # cur.execute('''INSERT INTO users (userID, points) 
    #     VALUES ('1', '123');''')

    conn.commit()
    conn.close()

def insert():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    #this is alr inserted into table so change before executing so we dont have duplicates 
    # cur.execute('''INSERT INTO pictures (pictureID, coordinates, link, chosen) 
    # VALUES ('1', '{40.34805, 74.65570}', 
    # 'https://res.cloudinary.com/dmiaxw4rr/image/upload/c_pad,b_auto:predominant,fl_preserve_transparency/v1710781520/TigerSpot/IMG_9697_kf2cim.jpg?_s=public-apps', 
    # 'False');''')

    conn.commit()
    conn.close()

def query():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # create_pic_table(cur)
    # create_user_table(cur)

    cur.execute("SELECT link FROM pictures")

    rows = cur.fetchall()

    link = rows[0][0]
    return link
    conn.commit()
    conn.close()
    
# def calc_points():

    
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
    