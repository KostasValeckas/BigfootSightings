DROP TABLE IF EXISTS Sightings CASCADE;

CREATE TABLE IF NOT EXISTS Sightings(
    nr int,
    title text,
    latitude float,
    longitude float,

    PRIMARY KEY (nr)
);

DELETE FROM Sightings;

