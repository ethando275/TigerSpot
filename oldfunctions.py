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

#given an pictureID, check to see if it has already been chosen
def has_pic_been_chosen(id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(f"SELECT chosen FROM pictures WHERE pictureID = {id};")
    result = cur.fetchone()

    chosen = result[0]

    return chosen

    conn.close()