DROP TABLE IF EXISTS Happens_At CASCADE;

CREATE TABLE IF NOT EXISTS Happens_At(
    nr int,
    lat Decimal(8,6),
    lng Decimal(9,6),

    PRIMARY KEY (nr, lng, lat),
    FOREIGN KEY (nr) REFERENCES Sightings(nr),
    FOREIGN KEY (lng, lat) REFERENCES Locations(lng, lat)
);

