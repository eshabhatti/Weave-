-- Dummy data file.
-- Deletes all data in the UserAccount table that 'createposts.sql' will create.
DELETE FROM Post WHERE post_id = 001;
DELETE FROM Post WHERE post_id = 002;
DELETE FROM Post WHERE post_id = 003;
DELETE FROM Post WHERE post_id = 004;
DELETE FROM Post WHERE post_id = 005;
DELETE FROM Post WHERE post_id = 006;
DELETE FROM Post WHERE post_id = 007;
DELETE FROM Post WHERE post_id = 008;
DELETE FROM Post WHERE post_id = 009;
DELETE FROM Post WHERE post_id = 010;

-- Selects all the data from the Post table to make sure deletion was a success.
SELECT *
FROM Post
;

-- Alternatively, you could turn off safe update mode and simply run:
-- DELETE FROM Post;
