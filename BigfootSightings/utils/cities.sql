DROP TABLE IF EXISTS Cities CASCADE;

CREATE TABLE IF NOT EXISTS Cities(
    cityName text,
    stateID text,
    stateName text,
    country text,

    PRIMARY KEY (cityName, stateID)
);