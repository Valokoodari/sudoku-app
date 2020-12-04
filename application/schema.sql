CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    display_name TEXT,
    permission_level INTEGER
);

CREATE TABLE sudokus (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users,
    name TEXT,
    cells TEXT[9][9],
    instructions TEXT,
    display INTEGER
);

CREATE TABLE shares (
    sudoku_id INTEGER REFERENCES sudokus,
    user_id INTEGER REFERENCES users
);