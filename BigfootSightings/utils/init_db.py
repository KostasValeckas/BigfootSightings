import psycopg2
import os

from dotenv import load_dotenv
from choices import sightingsFile, citiesFile

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
        # Run cities.sql
        with open('cities.sql') as db_file:
            cur.execute(db_file.read())
            print("Cities file opened")

        # Import all sightings from the dataset
        all_sightings = list(
            map(lambda x: tuple(x),
                sightingsFile[['number', 'title', 'latitude', 'longitude']].to_records(index=False))
        )
        sightingArgs_str = ','.join(cur.mogrify("(%s, %s, %s, %s)", i).decode('utf-8') for i in all_sightings)
        cur.execute("INSERT INTO Sightings (nr, title, latitude, longitude) VALUES " + sightingArgs_str)

        # Import all cities from the dataset
        all_cities = list(
            map(lambda x: tuple(x),
                citiesFile[['cityName', 'stateID', 'stateName', 'country']].to_records(index=False))
        )
        cityArgs_str = ','.join(cur.mogrify("(%s, %s, %s, %s)", i).decode('utf-8') for i in all_cities)
        cur.execute("INSERT INTO Cities (cityName, stateID, stateName, country) VALUES " + cityArgs_str)

        conn.commit()

    conn.close()
