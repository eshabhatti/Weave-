-- Dummy data file.
-- Deletes all data in the Post table that 'createposts.sql' will create.
DELETE from Post WHERE post_id = 001;
DELETE from Post WHERE post_id = 002;
DELETE from Post WHERE post_id = 003;
DELETE from Post WHERE post_id = 004;
DELETE from Post WHERE post_id = 005;
DELETE from Post WHERE post_id = 006;
DELETE from Post WHERE post_id = 007;
DELETE from Post WHERE post_id = 008;
DELETE from Post WHERE post_id = 009;
DELETE from Post WHERE post_id = 010;

-- Selects all the data from the Post table to make sure deletion was a success.
SELECT *
FROM Post
;

-- Alternatively, you could turn off safe update mode and simply run:
-- DELETE FROM Post;
