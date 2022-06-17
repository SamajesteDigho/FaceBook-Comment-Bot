DROP TABLE IF EXISTS features;

CREATE TABLE features (
    image TEXT PRIMARY KEY NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    name TEXT NOT NULL,
    price REAL DEFAULT 1.0,
    features TEXT NOT NULL
);
