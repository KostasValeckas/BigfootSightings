DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE IF NOT EXISTS Users(
    username text,
	password text,
    PRIMARY KEY (username)
);

