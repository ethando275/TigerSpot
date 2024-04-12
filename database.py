import psycopg2
from geopy.distance import geodesic
import random
import cloudinary
import cloudinary.api
import cloud
import datetime

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'


def pic_of_day():
   day_of_year = datetime.datetime.now().timetuple().tm_yday
   picture_id = (day_of_year - 1) % 125 + 1
   return picture_id

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

def drop_daily_points_table():
   # query to create a database
   conn = psycopg2.connect(DATABASE_URL)
   cur = conn.cursor()
   cur.execute('''DROP TABLE usersDaily; ''')
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
        link varchar(255));''')

    cloudinary.config(
    cloud_name = 'dmiaxw4rr', 
    api_key = '678414952824331', 
    api_secret = 'wt-aWFLd0n-CelO5kN8h1NCYFzY'
    )

    folder_name = 'TigerSpot'

    resources = cloudinary.api.resources(
        type = 'upload',
        prefix = folder_name, 
        max_results = 500,
        context = True
    )

    pictureID = 0

    for resource in resources.get('resources', []):
        link, latitude, longitude = cloud.image_data(resource)
        coordinates = [latitude, longitude]
        pictureID += 1
        chosen = False
        cur.execute(''' INSERT INTO pictures (pictureID, coordinates, link) 
        VALUES (%s, %s, %s);
        ''', (pictureID, coordinates, link))
        # cur.execute(f'''INSERT INTO pictures (pictureID, coordinates, link, chosen) 
        # VALUES ({pictureID}, {coordinates}, '{link}', {chosen});''')
    conn.commit()
    cur.close()
    conn.close()

# already executed
def create_user_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    username varchar(255),
    points int);''')

        # cur.execute('''INSERT INTO users (userID, points) 
        #     VALUES ('1', '123');''')


    conn.commit()
    cur.close()
    conn.close()

# already executed
def create_daily_points_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS usersDaily (
    username varchar(255),
    points int,
    distance int,
    played boolean);''')

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
    #sql = """UPDATE pictures
    # SET coordinates = '{40.34805, -74.65570}'
    #WHERE pictureID = 1;"""
#    cur.execute(sql)
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

    # conn.commit()
    cur.close()
    conn.close()
    
def insert_player(username):

   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check if username exists
    cur.execute("SELECT points FROM users WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        cur.execute("INSERT INTO users (username, points) VALUES (%s, %s);", (username, 0,))

    # Commit change and disconnect
    conn.commit()
    conn.close()

def calculate_today_points(distance):
    if distance - 15 <= 0:
        points = 1000
    if distance - 15 <= 0:
        points = 1000
    elif distance - 25 <= 0:
        points = 750
    elif distance - 35 <= 0:
        points = 500
    elif distance - 45 <= 0:
        points = 250
    elif distance - 50 <= 0:
        points = 100
    else:
        points = 0
    
    return points 
    return points 

def calculate_total_points(username, today_points):
    
    points = today_points + get_points(username)

    return points

def update_player(username, points):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("UPDATE users SET points=%s WHERE username=%s;", (points, username))

    conn.commit()
    conn.close()

def player_played(username): 

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT played FROM usersDaily WHERE username=%s;", (username, ))
    result = cur.fetchall()[0][0]

    conn.commit()
    conn.close()

    return result

def reset_player(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("UPDATE usersDaily SET played=%s, points=%s WHERE username=%s;", (False, 0, username))

    conn.commit()
    conn.close()

def reset_players():

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()


    cur.execute("UPDATE usersDaily SET played=%s;", (False, ))

    conn.commit()
    conn.close()

def reset_picture(id):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    update("pictures", "chosen", False, "pictureID", id)

    conn.commit()
    conn.close()

def insert_player_daily(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT points FROM usersDaily WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        cur.execute("INSERT INTO usersDaily (username, points, distance, played) VALUES (%s, %s, %s, %s);", (username, 0, 0, False))

    conn.commit()
    conn.close()


def update_player_daily(username, points, distance):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT points FROM usersDaily WHERE username=%s;", (username,))
    result = cur.fetchone()

    if result is None:
        cur.execute("UPDATE usersDaily SET points=%s, distance=%s, played=%s WHERE username=%s;", (points, distance, True, username))

    conn.commit()
    conn.close()
    
def get_daily_points(username):

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT points FROM usersDaily WHERE username=%s;''', (username,))
    points = cur.fetchone()
    
    # Disconnect
    conn.close()
    
    if points is None:
        return 0
    
    return points[0]

def get_daily_distance(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute('''SELECT distance FROM usersDaily WHERE username=%s;''', (username,))
    distance = cur.fetchone()
    
    # Disconnect
    conn.close()
    
    if distance is None:
        return 0
    
    return distance[0]
    


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

    return points[0]

def get_rank(username):
    
   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    try: 
        cur.execute("SELECT username, points, DENSE_RANK() OVER (ORDER BY points DESC) as rank FROM users;")
        players = cur.fetchall()
        
        for player in players: 
            if player[0] == username:
                return player[2]
        return "Player not found"
    
    finally:
        conn.close()

    

def remove_from_user_table(username):
   # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()


    cur.execute("DELETE FROM users WHERE username=%s;", (username,))
    conn.commit()

    # Disconnect
    conn.close()

def create_challenge(challenger_id, challengee_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Check for existing challenge between the two users
        cur.execute("""
            SELECT id FROM challenges 
            WHERE 
                ((challenger_id = %s AND challengee_id = %s) OR 
                (challenger_id = %s AND challengee_id = %s)) 
                AND status IN ('pending', 'accepted')
            """, (challenger_id, challengee_id, challengee_id, challenger_id))

        existing_challenge = cur.fetchone()

        if existing_challenge:
            # An existing challenge was found
            return {'error': 'Challenge already exists', 'challenge_id': existing_challenge[0]}

        # No existing challenge found, proceed to create a new one
        cur.execute("""
            INSERT INTO challenges (challenger_id, challengee_id, status) 
            VALUES (%s, %s, 'pending') RETURNING id;
            """, (challenger_id, challengee_id))
        
        challenge_id = cur.fetchone()[0]
        conn.commit()

        return {'success': 'Challenge created successfully', 'challenge_id': challenge_id}

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return {'error': 'Database error occurred'}
    finally:
        if conn is not None:
            conn.close()

# Accept a challenge
def accept_challenge(challenge_id):
    status = "failed"  # Default status in case of error
    arr = [False, False, False, False, False]
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            UPDATE challenges 
            SET status = 'accepted', 
                versusList = %s,
                    challenger_bool = %s,
                    challengee_bool = %s
            WHERE id = %s;
        """, (create_random_versus(), arr, arr, challenge_id))
        conn.commit()
        cur.close()
        status = "accepted"  # Update status on success
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        # Optionally, handle different types of exceptions differently
    finally:
        if conn is not None:
            conn.close()
    return status

# Decline a challenge
def decline_challenge(challenge_id):
    status = "failed"  # Default status in case of error
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("UPDATE challenges SET status = 'declined' WHERE id = %s;", (challenge_id,))
        conn.commit()
        cur.close()
        status = "declined"  # Update status on success
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return status


# Complete a match
def complete_match(challenge_id, winner_id, challenger_score, challengee_score):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("UPDATE challenges SET status = 'completed' WHERE id = %s;", (challenge_id,))
        cur.execute("INSERT INTO matches (challenge_id, winner_id, challenger_score, challengee_score) VALUES (%s, %s, %s, %s) RETURNING id;", (challenge_id, winner_id, challenger_score, challengee_score))
        match_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(f"Match completed with ID: {match_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_players():
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Execute query to fetch user IDs
    cur.execute("SELECT username FROM users;")
    table = cur.fetchall()
    user_ids = [row[0] for row in table]
    # Disconnect
    conn.close()

    return user_ids

#dont run again
def create_challenges_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS challenges(
    id SERIAL PRIMARY KEY,
    challenger_id VARCHAR(255),
    challengee_id VARCHAR(255),
    status VARCHAR(50));''')
    conn.commit()
    cur.close()
    conn.close()

#dont run again
def create_matches_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    challenge_id INTEGER,
    winner_id VARCHAR(255),
    challenger_score INTEGER,
    challengee_score INTEGER);''')
    conn.commit()
    cur.close()
    conn.close()

def clear_challenges_table():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Deletes all records from the challenges table
        cur.execute("DELETE FROM challenges;")
        conn.commit()  # Commit the transaction to make changes permanent
        print("Challenges table cleared.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing challenges table: {error}")
    finally:
        if conn is not None:
            conn.close()

def clear_matches_table():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Deletes all records from the matches table
        cur.execute("DELETE FROM matches;")
        conn.commit()  # Commit the transaction to make changes permanent
        print("Matches table cleared.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing matches table: {error}")
    finally:
        if conn is not None:
            conn.close()

def reset_challenges_id_sequence():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Assuming the sequence name is 'challenges_id_seq'
        cur.execute("ALTER SEQUENCE challenges_id_seq RESTART WITH 1;")
        conn.commit()  # Commit the change to make it permanent
        print("Challenges id sequence reset.")
        cur.execute("ALTER SEQUENCE matches_id_seq RESTART WITH 1;")
        conn.commit()  # Commit the change to make it permanent
        print("Matches id sequence reset.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error resetting challenges id sequence: {error}")
    finally:
        if conn is not None:
            conn.close()


def get_user_challenges(user_id):
    conn = psycopg2.connect(DATABASE_URL)  # Ensure DATABASE_URL is properly configured
    cur = conn.cursor()
    # Query for both challenges initiated by the user and challenges where the user is the challengee,
    # including whether each side has finished the challenge.
    cur.execute("""
        SELECT challenges.id, challenger_id, challengee_id, status, challenger_finished, challengee_finished
        FROM challenges
        WHERE (challenges.challenger_id = %s OR challenges.challengee_id = %s);
        """, (user_id, user_id))
    challenges = cur.fetchall()
    cur.close()
    conn.close()
    
    # Initialize dictionaries to hold the two types of challenges
    user_challenges = {'initiated': [], 'received': []}
    
    # Iterate through the results and categorize each challenge
    for challenge in challenges:
        # Add challenger_finished and challengee_finished to the dictionary
        if get_winner(challenge[0]) is not None:
            challenge_dict = {
                "id": challenge[0], 
                "challenger_id": challenge[1], 
                "challengee_id": challenge[2], 
                "status": challenge[3],
                "challenger_finished": challenge[4],
                "challengee_finished": challenge[5],
                "winner_id": get_winner(challenge[0])
            }
        else:
            challenge_dict = {
                "id": challenge[0], 
                "challenger_id": challenge[1], 
                "challengee_id": challenge[2], 
                "status": challenge[3],
                "challenger_finished": challenge[4],
                "challengee_finished": challenge[5],
                "winner_id": None
            }
        if challenge[1] == user_id:  # User is the challenger
            user_challenges['initiated'].append(challenge_dict)
        else:  # User is the challengee
            user_challenges['received'].append(challenge_dict)
    
    return user_challenges

#Returns the number of rows from pictures table
def get_table_size():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM pictures;")
    result = cur.fetchone()

    pic_num = result[0]

    return pic_num

    conn.close()

#given an pictureID, check to see if it has already been chosen
def has_pic_been_chosen(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(f"SELECT chosen FROM pictures WHERE pictureID = {id};")
    result = cur.fetchone()

    chosen = result[0]

    return chosen

    conn.close()

#gets a random pictureID
def get_pic_id():
    chosen = True
    while(chosen):
        num = random.randint(1, get_table_size())
        chosen = has_pic_been_chosen(num)
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    update("pictures", "chosen", True, "pictureID", num)

    conn.commit()
    conn.close()

    return num

#For Admin: reset all pictures to False, meaning they haven't been chosen
def reset_pic():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    for i in range(get_table_size()+1):
        update("pictures", "chosen", False, "pictureID", i)

    conn.commit()
    cur.close()
    conn.close()

def update_finish_status(challenge_id, user_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id 
            FROM challenges 
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return
        
        challenger_id, challengee_id = result
        
        # Depending on whether the user is the challenger or the challengee,
        # update the corresponding finished column in the matches table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges 
                SET challenger_finished = TRUE 
                WHERE id = %s;
            ''', (challenge_id,))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_finished = TRUE 
                WHERE id = %s;
            ''', (challenge_id,))
        else:
            print("User is not part of this challenge.")
            return
        
        conn.commit()
        print("Finish status updated successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

def check_finish_status(challenge_id):
    conn = None
    status = {"status": "unfinished"}  # Default status
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Query to check the finish status for both challenger and challengee
        cur.execute('''
            SELECT challenger_finished, challengee_finished
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result:
            challenger_finished, challengee_finished = result
            if challenger_finished and challengee_finished:
                status = {"status": "finished"}
        else:
            print("No match found with the given challenge_id.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error checking finish status: {error}")
    finally:
        if conn is not None:
            conn.close()
    
    return status

def get_challenge_participants(challenge_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # SQL query to select challenger_id and challengee_id from the challenges table
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result:
            # Unpack the result
            challenger_id, challengee_id = result
            participants = {
                "challenger_id": challenger_id,
                "challengee_id": challengee_id
            }
            return participants
        else:
            print("No challenge found with the given ID.")
            return None
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error: {error}")
        return None
    finally:
        if conn is not None:
            conn.close()

def update_versus_points(challenge_id, user_id, additional_points):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # First, determine if the user is the challenger or the challengee for this challenge
        cur.execute('''
            SELECT challenger_id, challengee_id
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return
        
        challenger_id, challengee_id = result
        
        # Depending on whether the user is the challenger or the challengee,
        # increment the corresponding points column for that user in the challenges table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_points = COALESCE(challenger_points, 0) + %s
                WHERE id = %s;
            ''', (additional_points, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_points = COALESCE(challengee_points, 0) + %s
                WHERE id = %s;
            ''', (additional_points, challenge_id))
        else:
            print("User is not part of this challenge.")
            return
        
        conn.commit()
        print("User points incremented successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

def calculate_versus(distance):
    if distance - 3 <= 0:
        points = 100
    elif distance - 10 <= 0:
        points = 80
    elif distance - 25 <= 0:
        points = 50
    else:
        points = 0

    return points

def get_challenge_results(challenge_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Query to get challenger and challengee points for the given challenge ID
        cur.execute('''
            SELECT challenger_id, challengee_id, challenger_points, challengee_points
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return {"error": "Challenge not found"}

        challenger_id, challengee_id, challenger_points, challengee_points = result
        
        # Determine the winner or if it's a tie
        if challenger_points > challengee_points:
            winner = challenger_id
        elif challengee_points > challenger_points:
            winner = challengee_id
        else:
            winner = "Tie"
        
        # Return a dictionary with the results
        return {
            "winner": winner,
            "challenger_points": challenger_points,
            "challengee_points": challengee_points,
            "challenge_id": challenge_id
        }
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return {"error": str(error)}
    finally:
        if conn is not None:
            conn.close()

def create_random_versus():
    row_count = get_table_size()
    
    # Generate 5 unique pseudo-random integers from 1 to row_count
    random_indices = random.sample(range(1, row_count + 1), 5)
    
    return random_indices
        
def get_random_versus(challenge_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Query to get the versusList for the given challenge ID
        cur.execute('''
            SELECT versusList
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return {"error": "Challenge not found"}
        
        versusList = result[0]
        return versusList
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return {"error": str(error)}
    finally:
        if conn is not None:
            conn.close()

def insert_into_challenges():
    
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        random = create_random_versus()
        # Insert a new row into the challenges table
        cur.execute('''
            INSERT INTO challenges (challenger_id, challengee_id, status, versusList, challenger_bool, challengee_bool)
            VALUES (%s, %s, %s, %s);
        ''', ("ed8205", "jon", "accepted", random,))
        
        # Commit the changes to the database
        conn.commit()
        print("New challenge inserted successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        if conn is not None:
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
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        if conn is not None:
            conn.close()

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

def get_winner(challenge_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT winner_id FROM matches WHERE challenge_id = %s;", (challenge_id,))
        result = cur.fetchone()
        if result is None:
            return None
        else:
            return result[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

def main():
    # update()
    # create_pic_table()
    # create_user_table()
    #reset_players()
    #show_rows()
    #reset_players()
    #show_rows()
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
    create_pic_table()
    show_rows()
    create_pic_table()
    show_rows()
    # print(has_pic_been_chosen(4))
    # reset_pic()
    #insert_picture(4, [40.349020, -74.653282], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594813/IMG_8918_o7x9nv.jpg", False)
    #insert_picture(5, [40.35014, -74.65285], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594815/IMG_0010_a2xd92.jpg", False)
    #insert_picture(6, [40.34855, -74.65622], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594815/IMG_0011_epzjfx.jpg", False)
    #insert_picture(7, [40.34785, -74.65410], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594813/IMG_0016_pvpuan.jpg", False)
    #insert_picture(8, [40.34952, -74.65760], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594814/IMG_0012_gyeoc8.jpg", False)
    #insert_picture(9, [40.34661, -74.65605], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594814/IMG_0013_a2lgwj.jpg", False)
    #insert_picture(10, [40.35020, -74.65503], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594814/IMG_0014_mhbsia.jpg", False)
    #insert_picture(11, [40.34201, -74.65450], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594813/IMG_0018_jkycga.jpg", False)
    #insert_picture(12, [40.34789, -74.65794], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1712594813/IMG_0017_gp6byj.jpg", False)
    #insert_picture(13, [40.34597, -74.65759], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1710781259/TigerSpot/IMG_2992_saqtml.jpg", False)
    #insert_picture(13, [40.34868, -74.65508], "https://res.cloudinary.com/dmiaxw4rr/image/upload/v1710781260/TigerSpot/IMG_3007_pug42w.jpg", False)
    #update_picture_id_by_coordinates(14, [40.34902, -74.653282])
    #update_picture_id_by_coordinates(15, [40.35014, -74.65285])
    #update_picture_id_by_coordinates(16, [40.34868, -74.65508])
    #show_rows()
    #update_picture_coordinates()
    #print()
    #create_challenge("jon", "ed8205")
    #clear_challenges_table()
    #clear_matches_table()
    #reset_challenges_id_sequence()
    #drop_user_table()
    #create_user_table()
    #drop_daily_points_table()
    #create_daily_points_table()
    
    #reset_players()
    # Closing the connection
    
if __name__=="__main__":
    main()

    # print(query())

    
