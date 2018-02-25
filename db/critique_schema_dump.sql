PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT UNIQUE,
  regDate INTEGER NOT NULL,
  lastLoginDate INTEGER);

CREATE TABLE IF NOT EXISTS users_profile(
  user_id INTEGER PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname TEXT,
  email TEXT UNIQUE,
  mobile TEXT UNIQUE,
  gender TEXT,
  avatar TEXT,
  birthdate TEXT,
  bio TEXT,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS posts (
  post_id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  sender_id INTEGER NOT NULL,
  receiver_id INTEGER,
  reply_to INTEGER,
  post_text TEXT NOT NULL,
  rating INTEGER,
  anonymous INTEGER NOT NULL,
  public INTEGER NOT NULL,
  FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(reply_to) REFERENCES posts(post_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS ratings(
  ratings_id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  sender_id INTEGER NOT NULL,
  receiver_id INTEGER NOT NULL,
  rating INTEGER NOT NULL,
  FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE);

COMMIT;
PRAGMA foreign_keys=ON;
