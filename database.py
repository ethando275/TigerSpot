#-----------------------------------------------------------------------
# database.py
#-----------------------------------------------------------------------
import psycopg2
#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

# TABLE 1: pictures
# TABLE 2: users
# TABLE 3: usersDaily
#-----------------------------------------------------------------------
def drop_table(table):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"DROP TABLE {table}; ")

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

def update(table, col, value, id_type, id_num):
   conn = psycopg2.connect(DATABASE_URL)
   cur = conn.cursor()
   cur.execute(f"UPDATE {table} SET {col} = {value} WHERE {id_type} = {id_num};")
   conn.commit()
   cur.close()
   conn.close()

def query(col, table):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(f"SELECT {col} FROM {table}")

    rows = cur.fetchall()

    row = rows[0][0]
    return row
    cur.close()
    conn.close()

#Returns the number of rows from a table
def get_table_size(table):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {table};")
    result = cur.fetchone()

    pic_num = result[0]

    return pic_num

    conn.close()

#-----------------------------------------------------------------------

def show_rows():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("USERS TABLE")
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    print("DAILY USERS TABLE")
    cur.execute("SELECT * FROM usersDaily;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    print("PICTURES TABLE")
    cur.execute("SELECT * FROM pictures;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    print("CHALLENGES TABLE")
    cur.execute("SELECT * FROM challenges;")
    for row in cur.fetchall():
        print(row)

    print("MATCHES TABLE")
    cur.execute("SELECT * FROM matches;")
    for row in cur.fetchall():
        print(row)

    conn.commit()
    cur.close()
    conn.close()

def main():
    show_rows()
    # drop_table("pictures")
    
if __name__=="__main__":
    main()


    
