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
    display TEXT
);

CREATE TABLE shares (
    sudoku_id INTEGER REFERENCES sudokus,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    uesr_id INTEGER REFERENCES users,
    sudoku_id INTEGER REFERENCES sudokus,
    rating INTEGER,
    content TEXT
);