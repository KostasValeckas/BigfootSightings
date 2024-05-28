from BigfootSightings import db_cursor, conn
from BigfootSightings.models import Sighting, User
import re

# MAX QUERY
def max_report_nr():
    sql = """
    SELECT MAX(nr) FROM Sightings
    """
    db_cursor.execute(sql)
    row = db_cursor.fetchone()
    print(row)
    if row:
        max = row['max']
        print("The maximum is:", max)
    else:
        print("Did not find a maximum")
    if max is None:
        max = 0    
    return max


# INSERT QUERIES
def insert_sighting(sighting: Sighting):
    sql = """
    INSERT INTO Sightings(nr, title, longitude, latitude)
    VALUES (%s, %s, %s, %s)
    """
    next_report_number = max_report_nr() + 1
    db_cursor.execute(sql, (next_report_number, sighting.title,  sighting.latitude, sighting.longitude))
    conn.commit()

def insert_user(user: User):
    sql = """
    INSERT INTO Users(username, password)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (user.username, user.password))
    conn.commit()

# SELECT QUERIES
def get_user_by_user_name(username):
    sql = """
    SELECT * FROM Users
    WHERE username = %s
    """
    db_cursor.execute(sql, (username,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    print("fetched used: ", user)
    return user

def get_all_sightings():
    sql = """
    SELECT * FROM Sightings
    """
    db_cursor.execute(sql)
    sightings = db_cursor.fetchall()
    return sightings

def search_sightings(search_text):

    # Validate the search_text for acceptable characters
    if not re.match("^[a-zA-Z0-9_ ]*$", search_text):
        print("Invalid search text")
        return []
    
    sql = """
    SELECT * FROM Sightings
    WHERE title ~*%s
    """
    db_cursor.execute(sql, (search_text,))
    sightings = db_cursor.fetchall()
    return sightings


