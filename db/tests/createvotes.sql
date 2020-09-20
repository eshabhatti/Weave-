-- Dummy data file.
-- Creates a series of fake votes.
-- Also updates the post table accordingly.
-- Run this after 'createusers.sql' and 'createposts.sql' and to get the intended effect.

-- These queries should perform correctly.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

INSERT INTO PostVote
VALUES (
    "realuser1",
    001,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 1
;

INSERT INTO PostVote
VALUES (
     "SneakySpy",
     001,
     1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 1
;

INSERT INTO PostVote
VALUES (
     "realuser1",
     002,
     -1
);
UPDATE Post
SET downvote_count = downvote_count + 1
WHERE post_id = 2
;

INSERT INTO PostVote
VALUES (
    "realuser2",
    002,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 2
;

INSERT INTO PostVote
VALUES (
    "realuser3",
    002,
    -1
);
UPDATE Post
SET downvote_count = downvote_count + 1
WHERE post_id = 2
;

INSERT INTO PostVote
VALUES (
    "Sneakyspy",
    002,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 2
;

INSERT INTO PostVote
VALUES (
    "realuser1",
    005,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 5
;

INSERT INTO PostVote
VALUES (
    "realuser2",
    005,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 5
;

INSERT INTO PostVote
VALUES (
    "realuser3",
    005,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 5
;

INSERT INTO PostVote
VALUES (
    "SneakySpy",
    005,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 5
;

INSERT INTO PostVote
VALUES (
    "realuser1",
    006,
    -1
);
UPDATE Post
SET downvote_count = downvote_count + 1
WHERE post_id = 6
;

INSERT INTO PostVote
VALUES (
    "realuser3",
    006,
    -1
);
UPDATE Post
SET downvote_count = downvote_count + 1
WHERE post_id = 6
;

INSERT INTO PostVote
VALUES (
    "SneakySpy",
    006,
    -1
);
UPDATE Post
SET downvote_count = downvote_count + 1
WHERE post_id = 6
;

INSERT INTO PostVote
VALUES (
    "realuser2",
    006,
    1
);
UPDATE Post
SET upvote_count = upvote_count + 1
WHERE post_id = 6
;

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Querys the current database to make sure the data was correctly inserted into the tables.
SELECT *
FROM PostVote
;

-- Also querys the post database to make sure the data was updated there.
SELECT *
FROM Post
;