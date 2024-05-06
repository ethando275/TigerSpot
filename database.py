#-----------------------------------------------------------------------
# database.py
# This file is for general actions with tables
# Tables in Tiger Spot: pictures, users, usersDaily, challenges, matches
#-----------------------------------------------------------------------
import psycopg2
#-----------------------------------------------------------------------

DATABASE_URL = 'postgres://tigerspot_user:9WtP1U9PRdh1VLlP4VdwnT0BFSdbrPWk@dpg-cnrjs7q1hbls73e04390-a.ohio-postgres.render.com/tigerspot'

#-----------------------------------------------------------------------
#drops a specified table
def drop_table(table):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE %s;" % (table))
                conn.commit()
                print(f"{table} has been dropped")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

#updates a specific row in a table
#id_type can be pictureID or challenge_id for example
def update(table, col, value, id_type, id_num):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE %s SET %s = %s WHERE %s = %s;" % (table, col, value, id_type, id_num))
                print(f"Updated with value as {value}")
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

#returns all the values from a specified column in a table in the form of an array of tuples
def query(column, table):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT %s FROM %s" % (column, table))
                rows = cur.fetchall()
                print(f"Returning values in column '{column}' from table '{table}'")
                return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

#Returns the number of rows in a table
def get_table_size(table):
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM %s;" % (table))
                print(f"Returning number of rows in table '{table}'")
                result = cur.fetchone()
                pic_num = result[0]
                return pic_num
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return "database error"

#-----------------------------------------------------------------------

#prints out all rows in the users, usersDaily, pictures, challenges, and matches tables
def show_rows():
    print("Showing all rows in users, usersDaily, pictures, challenges, and matches tables")
    print()
    print("USERS TABLE")
    print(query("*", "users"))
    print()
    print("DAILY USERS TABLE")
    print(query("*", "usersDaily"))
    print()
    print("PICTURES TABLE")
    print(query("*", "pictures"))
    print()
    print("CHALLENGES TABLE")
    print(query("*", "challenges"))
    print()
    print("MATCHES TABLE")
    print(query("*", "matches"))
    print()

#-----------------------------------------------------------------------
#tests the above functions that do not commit changes to the tables
def testing():
    #drop_table('pictures')
    #update('pictures', 'place', 'Princeton', 'pictureID', '1')
    print('-----Testing query()-----')
    print(query('pictureID', 'pictures'))
    print(query('place', 'pictures'))
    print()
    print('-----Testing get_table_size()-----')
    print(get_table_size('pictures'))
    print(get_table_size('users'))
    print(get_table_size('usersDaily'))
    print(get_table_size('challenges'))
    print(get_table_size('matches'))
    print()
    print('-----Testing show_rows()-----')
    show_rows()

#-----------------------------------------------------------------------

def main():
    print()
    testing()

#-----------------------------------------------------------------------

if __name__=="__main__":
    main()



    
