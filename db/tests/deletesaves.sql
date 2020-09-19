-- Dummy data file.
-- Deletes all data in the UserAccount table that 'createposts.sql' will create.
DELETE FROM SavedPost WHERE username = "SneakySpy" AND post_id = 001;
DELETE FROM SavedPost WHERE username = "realuser2" AND post_id = 001;
DELETE FROM SavedPost WHERE username = "realuser1" AND post_id = 005;
DELETE FROM SavedPost WHERE username = "SneakySpy" AND post_id = 003;
DELETE FROM SavedPost WHERE username = "realuser2" AND post_id = 005;
DELETE FROM SavedPost WHERE username = "SneakySpy" AND post_id = 004;
DELETE FROM SavedPost WHERE username = "SneakySpy" AND post_id = 005;
DELETE FROM SavedPost WHERE username = "realuser3" AND post_id = 006;
DELETE FROM SavedPost WHERE username = "realuser3" AND post_id = 008;

-- Selects all the data from the Post table to make sure deletion was a success.
SELECT *
FROM SavedPost
;

-- Alternatively, you could turn off safe update mode and simply run:
-- DELETE FROM SavedPost;