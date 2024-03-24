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
        longitude float,
        latitude float,
        link varchar(255), 
        chosen boolean);''')

    cur.execute('''INSERT INTO pictures (pictureID, longitude, latitude, link, chosen) 
    VALUES ('1', '40.34661', '74.65605', 'https://png.pngtree.com/png-vector/20191121/ourmid/pngtree-blue-bird-vector-or-color-illustration-png-image_2013004.jpg', 'False');''')

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