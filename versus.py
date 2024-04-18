import psycopg2
import random

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
#-----------------------------------------------------------------------

def calculate_versus(distance):
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

def update_versus_pic_status(challenge_id, user_id, index):
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
                SET challenger_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
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
        
#-----------------------------------------------------------------------

def store_versus_pic_points(challenge_id, user_id, index, points):
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
                SET challenger_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        else:
            print("User is not part of this challenge.")
            return
        
        conn.commit()
        print("Points updated successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------

def store_versus_pic_points(challenge_id, user_id, index, points):
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
        # update the corresponding points column in the challenges table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_pic_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_pic_points[%s] = %s
                WHERE id = %s;
            ''', (index, points, challenge_id))
        else:
            print("User is not part of this challenge.")
            return

        conn.commit()
        print("Versus pic points updated successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------

def update_versus_pic_status(challenge_id, user_id, index):
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
        # update the corresponding boolean value in the challenges table
        if user_id == challenger_id:
            cur.execute('''
                UPDATE challenges
                SET challenger_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        elif user_id == challengee_id:
            cur.execute('''
                UPDATE challenges
                SET challengee_bool[%s] = TRUE
                WHERE id = %s;
            ''', (index, challenge_id))
        else:
            print("User is not part of this challenge.")
            return

        conn.commit()
        print("Versus pic status updated successfully.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

#-----------------------------------------------------------------------