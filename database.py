import psycopg2


DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'
# connection establishment

def create(cur):
    # conn = psycopg2.connect(DATABASE_URL)

    # Creating a cursor object
    # cur = conn.cursor()
    # query to create a database 
    cur.execute('''CREATE TABLE pictures (
        pictureID int,
        coordinates float[2],
        link varchar(255), 
        chosen boolean);''')

    cur.execute('''INSERT INTO pictures (pictureID, longitude, latitude, link, chosen) 
    VALUES ('1', ['40.34805', '74.65570'], 'https://asset.cloudinary.com/dmiaxw4rr/35bd4c9df9bb361b5c8c905f6c25e540', 'False');''')

    # Closing the connection
    # conn.close()
    #{40.34661,74.65605}
    #"https://tinyurl.com/mvetxvex"
def query():
    conn = psycopg2.connect(DATABASE_URL)

    # Creating a cursor object
    
    cur = conn.cursor()
    create(cur)

    cur.execute("SELECT link FROM pictures")

    rows = cur.fetchall()

    link = rows[0][0]
    return link
    conn.close()
    
def main():
    print(query())
    

if __name__ == '__main__':
    main()