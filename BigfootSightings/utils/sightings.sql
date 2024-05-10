DROP TABLE IF EXISTS Sightings CASCADE;

-- TODO: For mnow dummy key as title
-- fix this later
CREATE TABLE IF NOT EXISTS Sightings(
    nr int,
    title text,
    latitude float,
    longitude float,

    PRIMARY KEY (title)
);

DELETE FROM Sightings;

