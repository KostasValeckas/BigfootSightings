DROP TABLE IF EXISTS Is_Close_To CASCADE;

CREATE TABLE IF NOT EXISTS Is_Close_To(
    lng Decimal(9,6),
    lat Decimal(8,6),
    cityName text,
	stateID text,

    PRIMARY KEYS (lng, lat, cityName, stateID)
    FOREIGN KEY lng REFERENCES Locations,
    FOREIGN KEY lat REFERENCES Locations,
    FOREIGN KEY cityName REFERENCES Cities,
    FOREIGN KEY stateID REFERENCES Cities
);

