-- This file holds example scripts that show how to properly select data from the database.
-- Only the tables created for sprint one will be expalained here.
-- Note that 'createtables.sql' must be run for any data to be allowed into the database.
-- If you want to run these queries yourself, you should also run 'sprintone_datainsertion.sql'.

-- In general, to select information from the database, use the format:
-- 		SELECT [data column(s) that you want displayed; use * for all columns]
-- 		FROM [table(s) that you want to pull the data from] 
-- 		WHERE [condition(s) that limit the columns shown]
-- 		ORDER BY [data column] [ASCENDING/DESCENDING]
-- 		LIMIT [range start (set as 0 if not specified),] [range end]
-- 		;

-- Many of the database's actions may simply pull a single specific entity:
SELECT *
FROM UserAccount
WHERE username = "realuser1"
;

-- Some actions may need to pull the most recent number of all of a type of entity.
-- This query would return the 10 most recent posts on the entire database:
SELECT *
FROM Post
ORDER BY date_created DESC
LIMIT 10
;

-- Other actions may need to pull the most recent number of a more specific set of entities.
-- This query would return the 10 most recent saved posts of the user "realuser1":
SELECT *
FROM SavedPost
WHERE username = "realuser1"
ORDER BY date_saved DESC
LIMIT 10
;

-- Returning user verification is one instance where data will need to be pulled from one table.
-- Assuming the user "realuser1" is logging in with their username and password only, the needed query would be:
SELECT username, encrypted_password, password_salt
FROM UserAccount
WHERE username = "realuser1"
;

-- More complicated queries may need to join tables together. 
-- These queries oftentimes occur while relating the data of two entities in one query only.
-- You can join tables either with the JOIN keyword or by having a WHERE condition that equates a relevant shared key.
-- Note that the AS keyword can be used to temporairly rename tables for queries, which will make typing easier.
-- For instance, to find the join date of the user who posted Post 202, you would write:
SELECT U.date_joined
FROM UserAccount AS U, Post AS P
WHERE U.username = P.creator AND P.post_id = 202
;

-- Queries can also return calculations in their own columns.
-- This will likely be used in things like calculating a post's score, among other things.
-- To perform the total score calculation for posts (upvote - downvote), you would write:
SELECT post_id, (upvote_count - downvote_count) AS total_score
FROM Post
ORDER BY total_score DESC
;