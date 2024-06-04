import psycopg2
import os
import pandas as pd
import sys
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Add the parent directory to the system path (needed for some imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


import tqdm


# THIS IS THE PATH YOU HAVE TO SET MANUALLY FOR YOUR LOCAL SETUP
LOCAL_PATH = "~/Documents/DIS/BigfootSightings"

# IF YOU DON'T CHANGE THE LAYOUT OF THE REPOSITORY, THIS PATH SHOULD WORK
SIGHTINGS_PATH = LOCAL_PATH + "/dataset/archive/bfro_locations.csv"
LOCATIONS_PATH = LOCAL_PATH + "/dataset/archive/locations.csv"


sightingsFile = pd.read_csv(SIGHTINGS_PATH, sep=",", dtype=str)

print("Sightings database loaded:\n", sightingsFile)

locationsFile = pd.read_csv(LOCATIONS_PATH, sep=",", dtype=str)

# convert Nan's to None's
locationsFile["city"] = locationsFile["city"].fillna("None")
locationsFile["state_name"] = locationsFile["state_name"].fillna("None")

print("Location cache loaded:\n", locationsFile)


# Remove the 'Report (number): ' prefix from the title
sightingsFile["title"] = sightingsFile["title"].str.replace(
    r"^Report \d+: ", "", regex=True
)


load_dotenv()

if __name__ == "__main__":

    # Load environment variables from .env file
    load_dotenv()

    conn = psycopg2.connect(
        host="localhost",
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
    )
    with conn.cursor() as cur:
        # Run users.sql
        with open("users.sql") as db_file:
            cur.execute(db_file.read())
            print("Users schema created")
        # Run sightings.sql
        with open("sightings.sql") as db_file:
            cur.execute(db_file.read())
            print("Sightings schema created")
        with open("locations.sql") as db_file:
            cur.execute(db_file.read())
            print("Locations schema created")

        # Import all sightings from the dataset
        all_sightings = list(
            map(
                lambda x: tuple(x),
                sightingsFile[
                    ["title", "timestamp", "latitude", "longitude"]
                ].to_records(index=False),
            )
        )

        # Import all locations from the dataset
        all_locations = list(
            map(
                lambda x: tuple(x),
                locationsFile[
                    ["latitude_rounded", "longitude_rounded", "country", "state_name", "city"]
                ].to_records(index=False),
            )
        )

        print("Using cached locations from locations.csv file.")
        locationArgs_str = ",".join(
            cur.mogrify("(%s, %s, %s, %s, %s)", i).decode("utf-8") for i in all_locations
        )
        cur.execute(
            "INSERT INTO Locations(latitude_rounded, longitude_rounded, country, state_name, city) VALUES "
            + locationArgs_str
        )

        db_cursor = conn.cursor(cursor_factory=RealDictCursor)

        # internal import to avoid circular imports
        from queries import insert_sighting

        # insert_sighting also insert locations (weak entities) if they don't exist,
        # so this loop takes some time. For the current set, we provide a pre-cooked
        # cache of locations in locations.csv that corresponds to initial sightings 
        # database.
        for record in tqdm.tqdm(all_sightings, desc="Initiating sightings databse"):
            # skip bad coordinate reads
            if (
                float(record[2]) < -90
                or float(record[2]) > 90
                or float(record[3]) < -180
                or float(record[3]) > 180
            ):
                continue
            sighting_data = dict(
                title=record[0], latitude=record[2], longitude=record[3]
            )
            insert_sighting(
                "timothyrenner (https://data.world/timothyrenner/bfro-sightings-data)",
                sighting_data,
                now=False,
                time=record[1],
                db_cursor=db_cursor,
                conn=conn,
            )

        # easter egg

        insert_sighting(
            "Anonymous",
            {"title": "Bigfoot seen crying over segfaulting C script", "latitude": 55.7017805, "longitude": 12.56108},
            now=True,
            db_cursor=db_cursor,
            conn=conn,
        )

        # add a user for the initial databse timothyrenner from:
        # https://data.world/timothyrenner/bfro-sightings-data
        cur.execute(
            "INSERT INTO Users(username, password) VALUES ('timothyrenner (https://data.world/timothyrenner/bfro-sightings-data)', '123')"
        )

        conn.commit()

    conn.close()

    print("\n---------\nDatabase initiated.\n---------\n")
