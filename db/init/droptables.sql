-- This will be the general destructor for Weave's database.
-- All tables within the database will be dropped. The database itself may also be dropped.
-- Format is:
-- 		DROP TABLE TableName ;

-- Selects the database to be deleted.
USE weave;

-- Drops the Blacklist table.
DROP TABLE Blacklist;

-- Drops the DirectMessage table.
DROP TABLE DirectMessage;

-- Drops the UserBlock table.
DROP TABLE UserBlock;

-- Drops the TopicFollow table.
DROP TABLE FollowTopic;

-- Drops the UserFollow table.
DROP TABLE FollowUser;

-- Drops the CommentVote table.
DROP TABLE CommentVote;

-- Drops the PostVote table.
DROP TABLE PostVote;

-- Drops the SavedPost table.
DROP TABLE SavedPost;

-- Drops the Comment table.
DROP TABLE PostComment;

-- Drops the Post table.
DROP TABLE Post;

-- Drops the Topic table.
DROP TABLE Topic;

-- Drops the UserAccount table
DROP TABLE UserAccount;

-- Terminates the entire database. This will also drop the tables above.
-- The DROP statements will be kept nonetheless in case the database needs to be cleared, not removed.
DROP DATABASE weave;