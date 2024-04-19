import psycopg2
import random
import database

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

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
    
#-----------------------------------------------------------------------

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
        
        
#-----------------------------------------------------------------------

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
        print(f"Challenge created with ID: {challenge_id}")
        return {'success': 'Challenge created successfully', 'challenge_id': challenge_id}

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return {'error': 'Database error occurred'}
    finally:
        if conn is not None:
            conn.close()
            
#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

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

#-----------------------------------------------------------------------

def get_challenge_results(challenge_id):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Query to get challenger and challengee points for the given challenge ID
        cur.execute('''
            SELECT challenger_id, challengee_id, challenger_points, challengee_points, challenger_pic_points, challengee_pic_points
            FROM challenges
            WHERE id = %s;
        ''', (challenge_id,))
        
        result = cur.fetchone()
        if result is None:
            print("Challenge not found.")
            return {"error": "Challenge not found"}

        challenger_id, challengee_id, challenger_points, challengee_points, challenger_pic_points, challengee_pic_points = result
        
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
            "challenger_id": challenger_id,
            "challengee_id": challengee_id,
            "challenger_points": challenger_points,
            "challengee_points": challengee_points,
            "challenge_id": challenge_id,
            "challenger_pic_points": challenger_pic_points,
            "challengee_pic_points": challengee_pic_points,
        }
        
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
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', ("ed8205", "jon", "completed", random, [True, True, True, True, True], [True, True, True, True, True]))
        
        # Commit the changes to the database
        conn.commit()
        print("New challenge inserted successfully.")
        
        cur.execute('''
                    INSERT INTO matches (challenge_id, winner_id, challenger_score, challengee_score)
                    VALUES (%s, %s, %s, %s);
                    ''', (1, "ed8205", 5, 3))
        conn.commit()
        print("New match inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
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
