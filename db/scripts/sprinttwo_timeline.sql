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

-- This can then be limited by adding in one more line:
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
LIMIT 0, 2
;

-- Note that as long as no tables are connected with JOIN, there should be no need for the DISTINCT keyword.
-- The above queries will all work properly only as long as there are no anonymous posts, however.
-- These anonymous posts should show when a user is following a topic, not when a user is following a user or when they made a post.
-- To illustrate this, there will be some more posts inserted:
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
INSERT INTO Post
VALUES (
	007,
    'ART',
    'followtest2',
    '2020-10-17 23:22:22',
    'Visible Post 6',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    1,
    0
);

INSERT INTO Post
VALUES (
	008,
    'GENERAL',
    'followtest3',
    '2020-10-17 23:22:22',
    'Invisible Post 2',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    1,
    0
);

INSERT INTO Post
VALUES (
    009,
    'GENERAL',
    'followtest1',
    '2020-10-17 22:22:22',
    'Invisible Post 3',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    1,
    0
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

-- If the above query is run, it will show anonymous posts where they aren't supposed to be.
-- Therefore the internal queries need to be modified, as anonymous posts are treated differently per category.
-- The easiest thing to do is likely going to be returning an explicit list of post_id attributes for each subquery.
-- The follow-user subquery, for instance, may look something like this:
SELECT post_id
FROM Post AS P, FollowUser AS F
WHERE F.user_followed = P.creator 
    AND P.anon_flag = 0 AND F.user_follower = 'followtest1'
;

-- While the user's own query may look something like this:
SELECT post_id
FROM Post
WHERE creator = 'followtest1' AND anon_flag = 0 
;

-- And the topic query may look like this:
SELECT post_id
FROM Post AS P, FollowTopic AS T
WHERE T.topic_followed = P.topic_name
    AND T.user_follower = 'followtest1'
;

-- The whole query, then, will look like this:
SELECT *
FROM Post
WHERE post_id IN
    ( SELECT post_id
      FROM Post
      WHERE creator = 'followtest1' AND anon_flag = 0 )
OR post_id IN 
    ( SELECT post_id
      FROM Post AS P, FollowTopic AS T
      WHERE T.topic_followed = P.topic_name AND T.user_follower = 'followtest1' )
OR post_id IN
    ( SELECT post_id
	  FROM Post AS P, FollowUser AS F
      WHERE F.user_followed = P.creator AND P.anon_flag = 0 AND F.user_follower = 'followtest1')
ORDER BY date_created DESC
;

-- And, of course, the limit statement can be added on afterwards.