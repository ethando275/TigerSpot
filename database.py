import psycopg2

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'
# connection establishment
conn = psycopg2.connect(DATABASE_URL)

# Creating a cursor object
cur = conn.cursor()

# query to create a database 
# cur.execute("CREATE DATABASE pictures")
cur.execute("SELECT * FROM pictures")

rows = cur.fetchall()
for row in rows:
    print(row)

# Closing the connection
conn.close()
