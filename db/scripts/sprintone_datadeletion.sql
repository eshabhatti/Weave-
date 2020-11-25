-- This file holds example scripts that show how to properly remove data from the database.
-- Only the tables created for sprint one will be expalained here.
-- Note that 'createtables.sql' must be run for any data to be allowed into the database.

-- In general, to remove an entity from some table [TableName], write:
-- 		DELETE FROM [TableName] WHERE [condition];
-- Note that spaces, newlines, and other whitespace should not matter. 
-- Also note that THE CONDITION MUST INVOLVE THE PRIMARY KEY FOR SAFE DELETION.
-- MySQL may also refuse to delete an entity if other entities still hold foriegn key constraints.
-- This may make deleting large accounts difficult in the future, but there may be cascading delete options available to help us here.

-- For now, all PostVote and SavedPosts entities corresponding to a user/post must be deleted before the user/post can be deleted.
-- To remove these entities, use the following statements but substitute the appropriate keys: 
DELETE FROM PostVote WHERE username = "realuser1" AND post_id = 101;
DELETE FROM SavedPost WHERE username = "realuser1" AND post_id = 101;

-- For proper removal of votes, the Post table must also be updated.
UPDATE Post SET downvote_count = downvote_count - 1 WHERE post_id = 101;

-- Once all dependent entities are removed, users and posts can be removed.
-- Note that posts ARE dependent upon users, so they must be removed before users are.
-- To remove these entities, use the following statements but substitute the appropriate keys: 
DELETE from Post WHERE post_id = 101;
DELETE from Post WHERE post_id = 202;
DELETE FROM UserAccount WHERE username = "realuser1";

-- For information about inserting data, see 'sprintone_datainsertion.sql'.
