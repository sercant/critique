INSERT INTO "users" VALUES(1, 'Scott', 1519557738, 1519557799);
INSERT INTO "users" VALUES(2, 'Kim', 1518557738, 1519554738);
INSERT INTO "users" VALUES(3, 'Stephen', 1517557738, 1519537738);
INSERT INTO "users" VALUES(4, 'Young', 1509557738, 1519557138);
INSERT INTO "users" VALUES(5, 'Knives', 1515557738, 1519457738);

INSERT INTO "users_profile" VALUES(1, 'Scott', 'Pilgrim', 'scott@outlook.com', NULL, 'male', 'photo1.jpg', '1998-01-22', 'Best bass in town. Ramona <3');
INSERT INTO "users_profile" VALUES(2, 'Kim', 'Pine', 'kim@hotmail.com', NULL, 'female', 'photo3.png', '2000-11-11', 'Drums! Dont irritate me...');
INSERT INTO "users_profile" VALUES(3, 'Stephen', 'Stills', 'stephen@gmail.com', '+358884567676', 'male', 'photo4.png', '2001-03-28', 'Im the best!');
INSERT INTO "users_profile" VALUES(4, 'Young', 'Neil', 'young@yahoo.com', '+902345448679', 'male', 'photo_5.jpg', '1981-07-30', 'Im good at gameboy');
INSERT INTO "users_profile" VALUES(5, 'Knives', 'Chau', 'knives@naver.com', NULL, 'female', 'photo8.png', '1981-12-22', 'Love you Scott!!');

INSERT INTO "posts" VALUES(0, 1362017481, 1, 2, NULL, 'She is scary and used to love me in highscool.', 6, 0, 1);
INSERT INTO "posts" VALUES(1, 1362012481, 1, 3, NULL, 'You are such a cool actor. Can we get a photo?', 10, 0, 1);
INSERT INTO "posts" VALUES(2, 1362017281, 1, 4, NULL, 'This dude is good at video games!', 8, 0, 1);
INSERT INTO "posts" VALUES(3, 1362017181, 1, 5, NULL, 'Ninja dancing like a boss.', 8, 0, 1);
INSERT INTO "posts" VALUES(4, 1362011481, 2, 1, NULL, 'Go and die scott!', 2, 1, 0);
INSERT INTO "posts" VALUES(5, 1362013381, 2, 5, NULL, 'She is creepy', 4, 1, 1);
INSERT INTO "posts" VALUES(6, 1362013881, 2, 3, NULL, 'Well he is a duche', 4, 1, 1);
INSERT INTO "posts" VALUES(7, 1362023481, 2, NULL, 6, 'No,  I am the best!', NULL, 0, 1);
INSERT INTO "posts" VALUES(8, 1362012381, 4, 1, NULL, 'Nice bass!', 8, 0, 1);
INSERT INTO "posts" VALUES(9, 1362012681, 4, 5, NULL, 'I love her', 8, 1, 1);
INSERT INTO "posts" VALUES(10, 1362020481, 5, NULL, 9, 'Scott is it you?? <3', NULL, 0, 1);
INSERT INTO "posts" VALUES(11, 1362021481, 5, 1, NULL, 'I love you scott!', 10, 0, 1);

INSERT INTO "ratings" VALUES(1, 1362022401, 1, 2, 6);
INSERT INTO "ratings" VALUES(2, 1362022411, 1, 3, 10);
INSERT INTO "ratings" VALUES(3, 1362022421, 1, 4, 8);
INSERT INTO "ratings" VALUES(4, 1362022431, 1, 5, 6);

INSERT INTO "ratings" VALUES(5, 1362022441, 2, 1, 8);
INSERT INTO "ratings" VALUES(6, 1362022451, 2, 3, 1);
INSERT INTO "ratings" VALUES(7, 1362022461, 2, 4, 8);
INSERT INTO "ratings" VALUES(8, 1362022471, 2, 5, 4);

INSERT INTO "ratings" VALUES(9, 1362022481, 3, 1, 6);
INSERT INTO "ratings" VALUES(10, 1362022491, 3, 2, 6);
INSERT INTO "ratings" VALUES(11, 1362022181, 3, 4, 6);
INSERT INTO "ratings" VALUES(12, 1362022281, 3, 5, 6);

INSERT INTO "ratings" VALUES(13, 1362022381, 4, 1, 8);
INSERT INTO "ratings" VALUES(14, 1362022481, 4, 2, 8);
INSERT INTO "ratings" VALUES(15, 1362022581, 4, 3, 8);
INSERT INTO "ratings" VALUES(16, 1362022681, 4, 5, 8);

INSERT INTO "ratings" VALUES(17, 1362022781, 5, 1, 10);
