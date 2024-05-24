#-----------------------------------------------------------------------
# versus_database.py
#-----------------------------------------------------------------------

import psycopg2
from db_config import DATABASE_URL

#-----------------------------------------------------------------------

# Update cumulative points for a user in a given challenge
def update_versus_points(challenge_id, user_id, additional_points):
    try:
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
                    # Challenge not found
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
                    # User is not part of this challenge
                    return
                
                conn.commit()
                return "success"
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------
# Calculate the points for a versus challenge
def calculate_versus(distance, time):
    if time < 10 and distance < 10:
        return 1000
    else:
        if distance < 0:
            raise ValueError("Distance cannot be negative")
        dis_points = max(0, 1 - distance / 110) * 900
        if time < 0 or time > 120:
            raise ValueError("Time taken must be between 0 and the maximum allowed time")
        time_points = max(0, 1 - time / 120) * 100

        return dis_points + time_points

#-----------------------------------------------------------------------
# Return winner of a given challenge
def get_winner(challenge_id):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT winner_id FROM matches WHERE challenge_id = %s;", (challenge_id,))
                result = cur.fetchone()
                if result is None:
                    return None
                else:
                    return result[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Update the status of a versus challenge picture
def update_versus_pic_status(challenge_id, user_id, index):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                
                # First, determine if the user is the challenger or the challengee for this challenge
                cur.execute('''
                    SELECT challenger_id, challengee_id
                    FROM challenges
                    WHERE id = %s;
                ''', (challenge_id,))
                
                result = cur.fetchone()
                # Challenge not found.
                if result is None:
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
                    # User is not part of this challenge
                    return
                
                conn.commit()
                return "success"
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Get the status of a versus challenge picture
def get_versus_pic_status(challenge_id, user_id, index):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                
                # First, determine if the user is the challenger or the challengee for this challenge
                cur.execute('''
                    SELECT challenger_id, challengee_id
                    FROM challenges
                    WHERE id = %s;
                ''', (challenge_id,))
                
                result = cur.fetchone()
                # Challenge not found
                if result is None:
                    return
                
                challenger_id, challengee_id = result
                
                # Depending on whether the user is the challenger or the challengee,
                # get the corresponding finished column in the matches table
                if user_id == challenger_id:
                    cur.execute('''
                        SELECT challenger_bool[%s]
                        FROM challenges
                        WHERE id = %s;
                    ''', (index, challenge_id))
                elif user_id == challengee_id:
                    cur.execute('''
                        SELECT challengee_bool[%s]
                        FROM challenges
                        WHERE id = %s;
                    ''', (index, challenge_id))
                else:
                    # User is not part of this challenge
                    return
                
                result = cur.fetchone()
                if result is None: 
                    # Index not found
                    return
                else:
                    return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

#-----------------------------------------------------------------------

# Store the points for a versus challenge picture
def store_versus_pic_points(challenge_id, user_id, index, points):
    try:
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
                    # Challenge not found
                    return
                
                challenger_id, challengee_id = result
                
                # Depending on whether the user is the challenger or the challengee,
                # update the corresponding points column in the challenges table
                if user_id == challenger_id:
                    sql = '''
                        UPDATE challenges
                        SET challenger_pic_points[{0}] = %s
                        WHERE id = %s;
                    '''.format(index)
                    cur.execute(sql, (points, challenge_id))
                elif user_id == challengee_id:
                    sql = '''
                        UPDATE challenges
                        SET challengee_pic_points[{0}] = %s
                        WHERE id = %s;
                    '''.format(index)
                    cur.execute(sql, (points, challenge_id))
                else:
                    # User is not part of this challenge
                    return
                
                conn.commit()
                return "success"
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return "database error"

      
#-----------------------------------------------------------------------

def main():
    
    # Testing
    print('Testing')
    #print(update_versus_points('1', '123', 100))
    #print(calculate_versus(2, 1))
    #print(get_winner('1'))
    #print(update_versus_pic_status('1', '123', 2))
    #print(get_versus_pic_status('1', '123', 2))
    #print(store_versus_pic_points('1', '123', 2, 100))
    

#-----------------------------------------------------------------------
    
if __name__=="__main__":
    main()