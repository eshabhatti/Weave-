-- This file holds test scripts that show how the cascading update (added 09-28-2020) will work.
-- These scripts assume that you have run 'createtables.sql' and 'createusers.sql' and 'createposts.sql'.

-- As before, users can be deleted if nothing depends on them.
-- For instance, since SneakySpy has made no posts or votes or saves, they can be deleted from the database without issue.
DELETE FROM UserAccount WHERE username = "SneakySpy";
SELECT * FROM UserAccount;
SELECT * FROM Post;

-- However, as before, if a user has dependent posts or votes, they cannot be deleted from the database.
DELETE FROM UserAccount WHERE username = "realuser1";
SELECT * FROM UserAccount;
SELECT * FROM Post;

-- With cascading upvote, however, data can be updated for users without first changing information in their dependents.
-- The script below would not run without cascading on update. 
-- With cascading, however, it should update all usernames of dependent posts when the user account's username changes.
UPDATE UserAccount SET username = "newrealuser1" WHERE username = "realuser1";
SELECT * FROM UserAccount;
SELECT * FROM Post;
