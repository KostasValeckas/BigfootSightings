DROP TABLE IF EXISTS Locations CASCADE;

CREATE TABLE IF NOT EXISTS Locations(
    id SERIAL PRIMARY KEY,
    latitude_rounded Decimal(3,1),
    longitude_rounded Decimal(4,1),
    country text,
    state_name text, --state is a protected keyword
    city text
);