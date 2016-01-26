CREATE TABLE IF NOT EXISTS entries (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  text  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS pages (
  id    INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  text  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email    TEXT NOT NULL,
  type     INTEGER
);
/*TODO: Check database, create safe database purge system and stuff*/
/*TODO: Database backup*/