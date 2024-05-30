DROP TABLE IF EXISTS Sightings CASCADE;

CREATE TABLE IF NOT EXISTS Sightings(
    nr int,
    username text,
    title text,
    t_stamp timestamp,

    PRIMARY KEY (nr)
);

DELETE FROM Sightings;

