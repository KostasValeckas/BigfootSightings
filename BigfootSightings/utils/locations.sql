DROP TABLE IF EXISTS Locations CASCADE;

CREATE TABLE IF NOT EXISTS Locations(
    lng Decimal(9,6),
    lat Decimal(8,6), 
    stateID text,
    country text,

    PRIMARY KEY (lng, lat)
);