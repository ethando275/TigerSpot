import psycopg2
import random
import database
import versus_database

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------

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
#Clear the challenges table of all records
def clear_challenges_table():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # Deletes all records from the challenges table
        cur.execute("DELETE FROM challenges;")
        conn.commit()  # Commit the transaction to make changes permanent
        print("Challenges table cleared.")
        cur.execute("DELETE FROM matches;")
        conn.commit()  # Commit the transaction to make changes permanent
        print("Matches table cleared.")
        cur.execute("ALTER SEQUENCE challenges_id_seq RESTART WITH 1;")
        conn.commit()  # Commit the change to make it permanent
        print("Challenges id sequence reset.")
        cur.execute("ALTER SEQUENCE matches_id_seq RESTART WITH 1;")
        conn.commit()  # Commit the change to make it permanent
        print("Matches id sequence reset.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing challenges table: {error}")
        return "database error"
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------
        
#Clear challenge table of all records related to a users
def clear_user_challenges(user_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Query to find challenges related to the user_id
                cur.execute("""
                    SELECT id FROM challenges 
                    WHERE challenger_id = %s OR challengee_id = %s;
                """, (user_id, user_id))

                challenge_ids = [row[0] for row in cur.fetchall()]
                
                if challenge_ids:
                    # Delete matching entries from the matches table
                    cur.execute("""
                        DELETE FROM matches 
                        WHERE challenge_id IN %s;
                    """, (tuple(challenge_ids),))
                    
                    # Delete entries from the challenges table
                    cur.execute("""
                        DELETE FROM challenges 
                        WHERE id IN %s;
                    """, (tuple(challenge_ids),))

                conn.commit()  # Commit the transaction to make changes permanent
                print(f"Entries related to user_id {user_id} cleared from challenges and matches tables.")
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing entries for user_id {user_id}: {error}")
        return "database error"


#-----------------------------------------------------------------------

# Create a new challenge
def create_challenge(challenger_id, challengee_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
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
                
                # Get the ID of the newly created challenge
                challenge_id = cur.fetchone()[0]
                conn.commit()
                print(f"Challenge created with ID: {challenge_id}")
                return {'success': 'Challenge created successfully', 'challenge_id': challenge_id}

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

# Accept a challenge
def accept_challenge(challenge_id):
    status = "failed"  # Default status in case of error
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE challenges 
                    SET status = 'accepted', 
                        versusList = %s
                    WHERE id = %s;
                """, (create_random_versus(), challenge_id))
                conn.commit()
                status = "accepted"  # Update status on success
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"
    return status

#-----------------------------------------------------------------------

# Decline a challenge
def decline_challenge(challenge_id):
    status = "failed"  # Default status in case of error
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE challenges SET status = 'declined' WHERE id = %s;", (challenge_id,))
                conn.commit()
                status = "declined"  # Update status on success
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"
    return status

#-----------------------------------------------------------------------

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
        return "database error"
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------

def get_user_challenges(user_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Query for both challenges initiated by the user and challenges where the user is the challengee,
                # including whether each side has finished the challenge.
                cur.execute("""
                    SELECT challenges.id, challenger_id, challengee_id, status, challenger_finished, challengee_finished
                    FROM challenges
                    WHERE (challenges.challenger_id = %s OR challenges.challengee_id = %s);
                    """, (user_id, user_id))
                challenges = cur.fetchall()
                
                # Initialize dictionaries to hold the two types of challenges
                user_challenges = {'initiated': [], 'received': []}
                
                # Iterate through the results and categorize each challenge
                for challenge in challenges:
                    # Add challenger_finished and challengee_finished to the dictionary
                    winner_id = versus_database.get_winner(challenge[0])
                    challenge_dict = {
                        "id": challenge[0], 
                        "challenger_id": challenge[1], 
                        "challengee_id": challenge[2], 
                        "status": challenge[3],
                        "challenger_finished": challenge[4],
                        "challengee_finished": challenge[5],
                        "winner_id": winner_id
                    }
                    if challenge[1] == user_id:  # User is the challenger
                        user_challenges['initiated'].append(challenge_dict)
                    else:  # User is the challengee
                        user_challenges['received'].append(challenge_dict)

                return user_challenges
    except Exception as e:
        print(f"An error occurred: {e}")
        return "database error"

#-----------------------------------------------------------------------

# Update the finish status for a user in a given challenge
def update_finish_status(challenge_id, user_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
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
                return {"status": "success"}
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Check the finish status for a user in given challenge
def check_finish_status(challenge_id):
    status = {"status": "unfinished"}  # Default status
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
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
        return "database error"
    
    return status

#-----------------------------------------------------------------------

# Return all users in a given challenge
def get_challenge_participants(challenge_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
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
        return "database error"

#-----------------------------------------------------------------------

# Return all information pertaining to results to display of a given challenge
def get_challenge_results(challenge_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Query to get challenger and challengee points for the given challenge ID
                cur.execute('''
                    SELECT challenger_id, challengee_id, challenger_points, challengee_points, challenger_pic_points, challengee_pic_points
                    FROM challenges
                    WHERE id = %s;
                ''', (challenge_id,))
                
                result = cur.fetchone()
                if result is None:
                    print("Challenge not found.")
                    return 

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
        return "database error"

#-----------------------------------------------------------------------

# Create a list of 5 unique pseudo-random integers from 1 to the number of rows in the pictures table
def create_random_versus():
    row_count = database.get_table_size('pictures')
    
    # Generate 5 unique pseudo-random integers from 1 to row_count
    random_indices = random.sample(range(1, row_count + 1), 5)
    
    return random_indices

#-----------------------------------------------------------------------
        
# Return the versusList for a given challenge
def get_random_versus(challenge_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Query to get the versusList for the given challenge ID
                cur.execute('''
                    SELECT versusList
                    FROM challenges
                    WHERE id = %s;
                ''', (challenge_id,))
                
                result = cur.fetchone()
                if result is None:
                    print("Challenge not found.")
                    return 
                
                versusList = result[0]
                return versusList
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Update if user has started a given challenge
def update_playbutton_status(challenge_id, user_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
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
                        SET playger_button_status = TRUE
                        WHERE id = %s;
                    ''', (challenge_id,))
                elif user_id == challengee_id:
                    cur.execute('''
                        UPDATE challenges
                        SET playgee_button_status = TRUE
                        WHERE id = %s;
                    ''', (challenge_id,))
                else:
                    print("User is not part of this challenge.")
                    return
                
                conn.commit()
                print("Play button status updated successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Returns if player has started a given challenge yet
def get_playbutton_status(challenge_id, user_id):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
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
                        SELECT playger_button_status
                        FROM challenges
                        WHERE id = %s;
                    ''', (challenge_id,))
                elif user_id == challengee_id:
                    cur.execute('''
                        SELECT playgee_button_status
                        FROM challenges
                        WHERE id = %s;
                    ''', (challenge_id,))
                else:
                    print("User is not part of this challenge.")
                    return
                
                result = cur.fetchone()
                if result is not None:
                    return result[0]
                else:
                    print("No results found.")
                    return None
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------
def main():
    #clear_challenges_table()
    #reset_challenges_id_sequence()
    print()
    create_challenge('a', 'ed8205')
    
if __name__=="__main__":
    main()