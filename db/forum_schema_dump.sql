PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS users(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  nickname TEXT UNIQUE,
  regDate INTEGER,
  lastLogin INTEGER);

CREATE TABLE IF NOT EXISTS users_profile(
  user_id INTEGER PRIMARY KEY,
  firstname TEXT,
  lastname TEXT,
  bio TEXT,
  email TEXT UNIQUE,
  mobile TEXT UNIQUE,
  birthdate TEXT,
  gender TEXT,
  avatar TEXT,
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS posts (
  post_id INTEGER,
  timestamp INTEGER,
  public INTEGER,
  sender_id INTEGER,
  receiver_id INTEGER,
  reply_to TEXT,
  post_text TEXT,
  rating INTEGER,
  PRIMARY KEY(post_id),
  FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (receiver_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(reply_to) REFERENCES posts(post_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS ratings(
  ratings_id INTEGER PRIMARY KEY,
  timestamp INTEGER,
  rating INTEGER,
  sender_id INTEGER,
  receiver_id INTEGER,
  PRIMARY KEY(ratings_id),
  FOREIGN KEY(sender_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(receiver_id) REFERENCES users(user_id) ON DELETE CASCADE);

COMMIT;
PRAGMA foreign_keys=ON;
