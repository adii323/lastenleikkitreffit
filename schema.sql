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
    info TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    invitation_id INTEGER REFERENCES invitations,
    title TEXT,
    value TEXT
);

CREATE TABLE invitation_classes (
    id INTEGER PRIMARY KEY,
    invitation_id INTEGER REFERENCES invitations,
    title TEXT,
    value TEXT
);

CREATE TABLE answers (
    id INTEGER PRIMARY KEY,
    invitation_id INTEGER REFERENCES invitations,
    user_id INTEGER REFERENCES users,
    childs_name TEXT,
    age INTEGER,
    message TEXT
);