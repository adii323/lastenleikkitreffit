CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE invitations (
    id INTEGER PRIMARY KEY,
    title TEXT,
    location TEXT,
    time DATE,
    age INTEGER,
    user_id INETEGR REFERENCES users
);
