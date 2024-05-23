DROP TABLE IF EXISTS Happens_At CASCADE;

CREATE TABLE IF NOT EXISTS Happens_At(
    nr int,
    lng Decimal(9,6),
    lat Decimal(8,6),

    PRIMARY KEYS (nr, lng, lat)
    FOREIGN KEY nr REFERENCES Reports,
    FOREIGN KEY lng REFERENCES Locations,
    FOREIGN KEY lat REFERENCES Locations
);

