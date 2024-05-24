DROP TABLE IF EXISTS Located_At CASCADE;

CREATE TABLE IF NOT EXISTS Located_At(
    cityName text,
	stateID text,
    lat Decimal(8,6),
    lng Decimal(9,6),

    PRIMARY KEY (cityName, stateID, lng, lat),
    FOREIGN KEY (cityName, stateID) REFERENCES Cities(cityName, stateID),
    FOREIGN KEY (lng, lat) REFERENCES Locations(lng, lat)
);

