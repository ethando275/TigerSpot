import psycopg2
import datetime
import cloudinary
import cloudinary.api
import cloud
import database

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

def create_pic_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pictures (
        pictureID int,
        coordinates float[2],
        link varchar(255));''')

    # connects to TigerSpot folder in cloudinary
    cloudinary.config(
    cloud_name = 'dmiaxw4rr', 
    api_key = '678414952824331', 
    api_secret = 'wt-aWFLd0n-CelO5kN8h1NCYFzY'
    )

    folder_name = 'TigerSpot/Checked'

    resources = cloudinary.api.resources(
        type = 'upload',
        prefix = folder_name, 
        max_results = 500,
        context = True
    )

    pictureID = 0

    # loops through folder and retrieves image url, coordinates and sets pictureid per resource
    for resource in resources.get('resources', []):
        link, latitude, longitude = cloud.image_data(resource)
        coordinates = [latitude, longitude]
        cur.execute("SELECT * FROM pictures WHERE link = %s", (link,))
        exists = cur.fetchone()
        if not exists:
            pictureID += 1
            cur.execute(''' INSERT INTO pictures (pictureID, coordinates, link) 
            VALUES (%s, %s, %s);
            ''', (pictureID, coordinates, link))
    conn.commit()
    cur.close()
    conn.close()

# Checks the current date and returns associated picture id
def pic_of_day():
   day_of_year = datetime.datetime.now().timetuple().tm_yday
   picture_id = (day_of_year - 1) % database.get_table_size("pictures") + 1
   return picture_id

def get_pic_info(col, id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(f"SELECT {col} FROM pictures WHERE pictureID = {id}")
    rows = cur.fetchall()

    row = rows[0][0]
    return row
    # conn.commit()
    cur.close()
    conn.close()

def update_picture_coordinates():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)  # Make sure DATABASE_URL is properly configured
        cur = conn.cursor()
        
        # SQL command to update the coordinates of the picture with the specified pictureID
        cur.execute('''
            UPDATE pictures
            SET coordinates = %s
            WHERE pictureID = %s;
        ''', ([40.34642, -74.65609], 1))
        
        # Commit the changes to the database
        conn.commit()
        print(f"Coordinates updated successfully for pictureID {1}.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"An error occurred: {error}")
    finally:
        # Ensure the database connection is closed
        if conn is not None:
            conn.close()
            
#-----------------------------------------------------------------------

def insert_picture(pictureID, coordinates, link):
    conn = None
    try:
        # Creating a cursor object using the connection object
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # SQL statement for inserting data
        insert_sql = '''INSERT INTO pictures (pictureID, coordinates, link) 
                        VALUES (%s, %s, %s)'''
        # Executing the SQL statement with the provided values
        cur.execute(insert_sql, (pictureID, coordinates, link))
        # Committing the transaction
        conn.commit()
        print("Row inserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error in insert operation: {error}")
    finally:
        # Closing the cursor
        if cur is not None:
            cur.close()
    
#-----------------------------------------------------------------------

def update_picture_id_by_coordinates(new_pictureID, coordinates):
    conn = None
    try:
        # Creating a cursor object using the connection object
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # SQL statement for updating the pictureID
        update_sql = '''UPDATE pictures SET pictureID = %s WHERE coordinates = ARRAY[%s, %s]::float[]'''
        # Executing the SQL statement with the provided values
        cur.execute(update_sql, (new_pictureID, coordinates[0], coordinates[1]))
        # Committing the transaction
        conn.commit()
        # Check if the update was successful
        if cur.rowcount == 0:
            print("No rows were updated.")
        else:
            print(f"{cur.rowcount} row(s) updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error in update operation: {error}")
    finally:
        # Closing the cursor
        if cur is not None:
            cur.close()
            
#-----------------------------------------------------------------------