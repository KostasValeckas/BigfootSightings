DROP TABLE IF EXISTS Sightings CASCADE;

CREATE TABLE IF NOT EXISTS Sightings(
    nr SERIAL PRIMARY KEY,
    username text,
    title text,
    report_time TIMESTAMPTZ,
    latitude float,
    longitude float,
    location_id int
);

DELETE FROM Sightings;

