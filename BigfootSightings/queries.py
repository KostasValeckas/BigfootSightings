import os
import sys


from BigfootSightings import db_cursor, conn


import re

from BigfootSightings.utils.geolocator import get_location_descriptor
from BigfootSightings.models import User, Location
import datetime


# INSERT QUERIES


def insert_location(lat, long, db_cursor=db_cursor, conn=conn):

    """
    Custom db_cursor and conn parameters are used for initiating database.
    """

    # get location descriptors (if exists):
    country, state, city = get_location_descriptor(lat, long)

    # Round latitude and longitude to one decimal if necessary
    lat = round(float(lat), 1)
    long = round(float(long), 1)

    sql = """
    INSERT INTO Locations(latitude_rounded, longitude_rounded, country, state_name, city)
    VALUES (%s, %s, %s, %s, %s)
    """
    db_cursor.execute(sql, (lat, long, country, state, city))
    conn.commit()


def insert_sighting(
    username: str, sighting, now: bool = True, time=None, db_cursor=db_cursor, conn=conn
):
    """
    algorithm:

    1. Check if the location exists in the database
    2. If it does, get the location_id, else create location (weak entity)
    3. Insert the sighting into the database

    The "now" bool is used to control whether to timestamp with current time

    Custom db_cursor and conn parameters are used for initiating database.
    """

    if db_cursor is None or conn is None:
        raise ValueError("db_cursor and conn parameters are required")

    location_id = get_location_id(
        sighting["latitude"], sighting["longitude"], db_cursor=db_cursor
    )

    if not location_id:
        insert_location(
            sighting["latitude"], sighting["longitude"], db_cursor=db_cursor, conn=conn
        )
        location_id = get_location_id(
            sighting["latitude"], sighting["longitude"], db_cursor=db_cursor
        )
        assert location_id is not None  # location should exist now

    time = "NOW()" if now else time

    sql = """
    INSERT INTO Sightings(username, title, report_time, longitude, latitude, location_id)
    VALUES (%s, %s, %s, %s,%s, %s)
    """

    db_cursor.execute(
        sql,
        (
            username,
            sighting["title"],
            time,
            sighting["latitude"],
            sighting["longitude"],
            location_id,
        ),
    )
    conn.commit()


def insert_user(user):
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
    return user


def get_all_sightings():

    sql = """
    SELECT * FROM Sightings
    JOIN Locations ON Sightings.location_id = Locations.id
    """
    db_cursor.execute(sql)
    sightings = db_cursor.fetchall()
    return sightings


def search_sightings(
    search_text=None,
    username=None,
    lat=None,
    long=None,
    location_id=None,
    time=None,
    country=None,
    state = None,
    city=None,
):
    if not any([search_text, username, lat, long, location_id, time, country, state, city]):
        return None

    sql = """
    SELECT * FROM Sightings
    JOIN Locations ON Sightings.location_id = Locations.id
    WHERE 1=1
    """
    params = []

    if search_text:
        # Validate the search_text for acceptable characters
        if not re.match("^[a-zA-Z0-9_ ]*$", search_text):
            return []

        sql += " AND Sightings.title ~* %s"
        params.append(search_text)

    if username:
        sql += " AND Sightings.username = %s"
        params.append(username)

    if lat:
        if not lat.lstrip("-").isdigit():
            return []  # Invalid format
        lat = round(float(lat))
        sql += " AND ROUND(CAST(Sightings.latitude AS numeric), 0) = %s"
        params.append(lat)

    if long:
        if not long.lstrip("-").isdigit():
            return []
        long = round(float(long))
        sql += " AND ROUND(CAST(Sightings.longitude AS numeric), 0) = %s"
        params.append(long)

    if location_id:
        try:
            location_id = int(location_id)
        except ValueError:
            return []  # Invalid location_id format
        sql += " AND Sightings.location_id = %s"
        params.append(location_id)

    if time:
        try:
            datetime.datetime.strptime(time, "%Y-%m-%d")
        except ValueError:
            return []  # Invalid date format
        sql += " AND DATE(Sightings.report_time) = %s"
        params.append(time)

    if country:
        sql += " AND Locations.country ~* %s"
        params.append(f".*{country}.*")

    if state:
        sql += " AND Locations.state_name ~* %s"
        params.append(f".*{state}.*")


    if city:
        sql += " AND Locations.city ~* %s"
        params.append(f".*{city}.*")


    db_cursor.execute(sql, tuple(params))
    sightings = db_cursor.fetchall()
    return sightings


def show_timezone():
    sql = """
    SHOW TIMEZONE
    """
    db_cursor.execute(sql)
    timezone = db_cursor.fetchone()
    if timezone:
        return timezone["TimeZone"]
    else:
        return "Timezone unknown"


def get_location_id(latitude, longitude, db_cursor=db_cursor):
    """
    Custom db_cursor parameter is used for initiating database.
    """
    sql = """
    SELECT id FROM Locations
    WHERE latitude_rounded = %s AND longitude_rounded = %s
    """

    latitude = round(float(latitude), 1)
    longitude = round(float(longitude), 1)
    db_cursor.execute(sql, (latitude, longitude))
    location = db_cursor.fetchone()

    if location:
        return location["id"]
    else:
        return None


def get_location_by_id(location_id):
    sql = """
    SELECT * FROM Locations
    WHERE id = %s
    """
    db_cursor.execute(sql, (location_id,))
    location = Location(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return location
