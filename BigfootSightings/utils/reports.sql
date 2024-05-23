DROP TABLE IF EXISTS Reports CASCADE;

CREATE TABLE IF NOT EXISTS Reports(
    username text
    nr int,

    PRIMARY KEYS (username, nr)
    FOREIGN KEY username REFERENCES Users,
    FOREIGN KEY nr REFERENCES Sightings
);

