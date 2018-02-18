PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT UNIQUE,
  regDate INTEGER NOT NULL,
  lastLogin INTEGER);

CREATE TABLE IF NOT EXISTS users_profile(
  user_id INTEGER PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname TEXT,
  bio TEXT,
  email TEXT UNIQUE,
  mobile TEXT UNIQUE,
  birthdate TEXT,
  gender TEXT,
  avatar TEXT,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS posts (
  post_id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  public INTEGER NOT NULL,
  sender_id INTEGER NOT NULL,
  anonymous INTEGER NOT NULL,
  receiver_id INTEGER NOT NULL,
  reply_to TEXT,
  post_text TEXT NOT NULL,
  rating INTEGER,
  FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(reply_to) REFERENCES posts(post_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS ratings(
  ratings_id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp INTEGER NOT NULL,
  rating INTEGER NOT NULL,
  sender_id INTEGER NOT NULL,
  receiver_id INTEGER NOT NULL,
  FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE);

COMMIT;
PRAGMA foreign_keys=ON;
