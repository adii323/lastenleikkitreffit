CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE invitations (
    id INTEGER PRIMARY KEY,
    title TEXT,
    name TEXT,
    location TEXT,
    day DATE,
    time TEXT,
    age INTEGER,
    childs_name TEXT,
    user_id INTEGER REFERENCES users
);
