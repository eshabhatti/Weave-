-- This file holds a script that tests the statements that must be used to pull timeline posts.
-- Timeline posts include the posts that the user makes as well as posts from the accounts and topics that the user follows.
-- Ideally, there shuold be only one final statement that pulls all timeline posts.

-- First we create some dummy users.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
INSERT INTO UserAccount 
VALUES (
	'followtest1', 
    'AAAaaa111@password.org', 
    '$2b$12$EZTltQzTCIaoQbFaJV0ELes/0vJpwptkvfijuWaZFpgu2OKlqatUS',
    NULL,
    NULL,
    '2020-10-16 20:13:11',
    NULL,
    NULL,
    '0',
    '0'
);

INSERT INTO UserAccount
VALUES (
	'followtest2',
    'ABCabc777@password.com',
    '$2b$12$3.iOc2fUVKz2f7gjLu2pi.ZQP87RxBWSXmcGmeTKGZf9DEuIMCDwi',
    NULL,
    NULL,
    '2020-10-16 13:22:31',
    NULL,
    NULL,
    '0',
    '0'
);

INSERT INTO UserAccount
VALUES (
	'followtest3', 
    'BCAbac1@password.org',
    '$2b$12$rK4RleKHCA3qjOd7WoQPfe36Seu3CJegVG5kIyw3f23kXiEYrhlpK',
    NULL,
    NULL,
    '2020-10-16 11:20:22',
    NULL,
    NULL,
    '0',
    '0'
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- Next we create some dummy topics.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
INSERT INTO Topic
VALUES (
	'GENERAL',
    '2020-10-16 12:04:12',
    0,
    0
);

INSERT INTO Topic
VALUES (
	'ART',
    '2020-10-16 14:02:11',
    0,
    0
);

INSERT INTO Topic
VALUES (
	'CATS',
    '2020-10-16 23:23:23',
    0,
    0
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- Next we enter some dummy posts.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
INSERT INTO Post
VALUES (
    001,
    'GENERAL',
    'followtest1',
    '2020-10-17 22:22:22',
    'Visible Post 1',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	002,
    'GENERAL',
    'followtest2',
    '2020-10-17 21:22:22',
    'Invisible Post 1',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	003,
    'ART',
    'followtest2',
    '2020-10-17 21:22:22',
    'Visible Post 2',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	004,
    'CATS',
    'followtest2',
    '2020-10-17 12:21:34',
    'Visible Post 3',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	005,
    'GENERAL',
    'followtest3',
    '2020-10-17 20:22:22',
    'Visible Post 4',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	006,
    'ART',
    'followtest3',
    '2020-10-17 23:22:22',
    'Visible Post 5',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- Finally, we add the dummy follow conditions.
-- For this test, the user 'followtest1' will follow topics 'ART' and 'CATS'.
-- User 'followtest1' will also follow the user 'followtest3'.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
INSERT INTO FollowTopic
VALUES (
	'followtest1',
    'ART'
);

INSERT INTO FollowTopic
VALUES (
	'followtest1',
    'CATS'
);

INSERT INTO FollowUser
VALUES (
	'followtest1',
    'followtest3'
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- Now that the data has been inserted, we need to pull all posts that meet the above criteria.
-- Pulling posts that the user has made just requires a simple select statement.
SELECT *
FROM Post
WHERE creator = 'followtest1'
ORDER BY date_created DESC
;

-- Pulling posts from followed topics and accounts is not as clear.
-- This is because there may be more than one topic that the user follows.
-- The backend could handle this by first pulling all the topics that the user follows:
SELECT topic_followed
FROM FollowTopic
WHERE user_follower = 'followtest1'
;

-- Before writing a dynamic query to the database like this:
SELECT *
FROM Post
WHERE topic_name = 'ART' OR topic_name = 'CATS'
ORDER BY date_created DESC
;

-- It will probably be more effective, however, to write an embedded query to do both these things at once:
SELECT *
FROM Post
WHERE topic_name IN 
	( SELECT topic_followed AS topic_name
	  FROM FollowTopic
      WHERE user_follower = 'followtest1' )
ORDER BY date_created DESC
;

-- The two timeline elements can then be combined into the following query:
SELECT *
FROM Post
WHERE creator = 'followtest1'
OR topic_name IN 
	( SELECT topic_followed AS topic_name
	  FROM FollowTopic
      WHERE user_follower = 'followtest1' )
ORDER BY date_created DESC
;

-- The final timeline element should be retrieved in a similiar way:
SELECT *
FROM Post
WHERE creator IN
	( SELECT user_followed AS creator
      FROM FollowUser
      WHERE user_follower = 'followtest1' )
ORDER BY date_created DESC
;

-- Therefore, the final list of timeline posts should be retrieved with the following query:
SELECT *
FROM Post
WHERE creator = 'followtest1'
OR topic_name IN 
	( SELECT topic_followed AS topic_name
	  FROM FollowTopic
      WHERE user_follower = 'followtest1' )
OR creator IN
	( SELECT user_followed AS creator
      FROM FollowUser
      WHERE user_follower = 'followtest1' )
ORDER BY date_created DESC
;

-- Note that as long as no tables are connected with JOIN, there should be no need for the DISTINCT keyword.
