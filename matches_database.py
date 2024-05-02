import psycopg2

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'


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

#--------------------------------------------------------------
def clear_matches_table():
    conn = None
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Deletes all records from the matches table
                cur.execute("DELETE FROM matches;")
                conn.commit()  # Commit the transaction to make changes permanent
                print("Matches table cleared.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error clearing matches table: {error}")
   
#--------------------------------------------------------------
            
# Complete a match
def complete_match(challenge_id, winner_id, challenger_score, challengee_score):
    try:
        # Establish connection and create cursor using 'with' statement
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                # Update the status of the challenge to 'completed'
                cur.execute("UPDATE challenges SET status = 'completed' WHERE id = %s;", (challenge_id,))
                # Insert the match into the matches table
                cur.execute("INSERT INTO matches (challenge_id, winner_id, challenger_score, challengee_score) VALUES (%s, %s, %s, %s) RETURNING id;", (challenge_id, winner_id, challenger_score, challengee_score))
                match_id = cur.fetchone()[0]
                conn.commit()
                print(f"Match completed with ID: {match_id}")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#--------------------------------------------------------------

def main():
    #clear_matches_table()
    print()
    
if __name__=="__main__":
    main()