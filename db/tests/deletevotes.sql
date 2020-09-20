-- Dummy data file.
-- Deletes all data in the UserAccount table that 'createvotes.sql' will create.
DELETE FROM PostVote WHERE username = "realuser1" AND post_id = 001;
DELETE FROM PostVote WHERE username = "SneakySpy" AND post_id = 001;
DELETE FROM PostVote WHERE username = "realuser1" AND post_id = 002;
DELETE FROM PostVote WHERE username = "realuser2" AND post_id = 002;
DELETE FROM PostVote WHERE username = "realuser3" AND post_id = 002;
DELETE FROM PostVote WHERE username = "SneakySpy" AND post_id = 002;
DELETE FROM PostVote WHERE username = "realuser1" AND post_id = 005;
DELETE FROM PostVote WHERE username = "realuser2" AND post_id = 005;
DELETE FROM PostVote WHERE username = "realuser3" AND post_id = 005;
DELETE FROM PostVote WHERE username = "SneakySpy" AND post_id = 005;
DELETE FROM PostVote WHERE username = "realuser1" AND post_id = 006;
DELETE FROM PostVote WHERE username = "realuser3" AND post_id = 006;
DELETE FROM PostVote WHERE username = "realuser2" AND post_id = 006;
DELETE FROM PostVote WHERE username = "SneakySpy" AND post_id = 006;

-- Shows the PostVote table to make sure that all data was updated correctly.
SELECT *
FROM PostVote
;

-- Alternatively, you could turn off safe update mode and simply run:
-- DELETE FROM PostVote;

-- Clears the updates done to the Post table.
UPDATE Post SET upvote_count = 0, downvote_count = 0 WHERE post_id = 1;
UPDATE Post SET upvote_count = 0, downvote_count = 0 WHERE post_id = 2;
UPDATE Post SET upvote_count = 0, downvote_count = 0 WHERE post_id = 5;
UPDATE Post SET upvote_count = 0, downvote_count = 0 WHERE post_id = 6;

-- Shows the Post table to make sure that all data was updated correctly.
SELECT *
FROM Post
;

-- Alternatively, you could turn off safe update mode and simply run:
-- UPDATE Post SET upvote_count = 0, downvote_count = 0;
