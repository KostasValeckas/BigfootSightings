import psycopg2
import os

from dotenv import load_dotenv
from choices import sightingsFile, happensAtFile, locationsFile
load_dotenv()

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )
    with conn.cursor() as cur:
        # Run users.sql
        with open('users.sql') as db_file:
            cur.execute(db_file.read())
            print("Users file opened")
        # Run sightings.sql
        with open('sightings.sql') as db_file:
            cur.execute(db_file.read())
            print("Sightings file opened")
        # Run locatedAt.sql
        with open('happensAt.sql') as db_file:
            cur.execute(db_file.read())
            print("HappensAt file opened")
        # Run locations.sql
        with open('locations.sql') as db_file:
            cur.execute(db_file.read())
            print("Locations file opened")

        # Import all sightings from the dataset
        all_sightings = list(
            map(lambda x: tuple(x),
                sightingsFile[['number', 'title', 'timestamp']].to_records(index=False))
        )
        sightingArgs_str = ','.join(cur.mogrify("(%s, %s, %s)", i).decode('utf-8') for i in all_sightings)
        cur.execute("INSERT INTO Sightings (nr, title, t_stamp) VALUES " + sightingArgs_str)

        # Import all locations from the dataset
        all_locations = list(
            map(lambda x: tuple(x),
                locationsFile[['lat', 'lng', 'stateName', 'country']].to_records(index=False))
        )
        locationArgs_str = ','.join(cur.mogrify("(%s, %s, %s, %s)", i).decode('utf-8') for i in all_locations)
        cur.execute("INSERT INTO Locations (lat, lng, stateName, country) VALUES " + locationArgs_str)

        # Import all happensAts from the dataset
        all_happensAts = list(
            map(lambda x: tuple(x),
                happensAtFile[['number', 'lat', 'lng']].to_records(index=False))
        )
        happensAtArgs_str = ','.join(cur.mogrify("(%s, %s, %s)", i).decode('utf-8') for i in all_happensAts)
        cur.execute("INSERT INTO Happens_At (nr, lat, lng) VALUES " + happensAtArgs_str)

        conn.commit()

    conn.close()
