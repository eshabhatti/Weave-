-- This will be the general destructor for Weave's database.
-- All tables within the database will be dropped. The database itself may also be dropped.
-- Format is:
-- 		DROP TABLE TableName ;

-- Drops the Post table.
DROP TABLE Post;

-- Drops the UserAccount table
DROP TABLE UserAccount;

-- Terminates the entire database. This will also drop the tables above.
-- The DROP statements will be kept nonetheless in case the database needs to be cleared, not removed.
DROP DATABASE weave; 
