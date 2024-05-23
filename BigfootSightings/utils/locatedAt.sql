DROP TABLE IF EXISTS Located_At CASCADE;

CREATE TABLE IF NOT EXISTS Located_At(
    cityName text,
	stateID text,
    lng Decimal(9,6),
    lat Decimal(8,6),

    PRIMARY KEYS (cityName, stateID, lng, lat)
    FOREIGN KEY cityName REFERENCES Cities,
    FOREIGN KEY stateID REFERENCES Cities,
    FOREIGN KEY lng REFERENCES Locations,
    FOREIGN KEY lat REFERENCES Locations
);

