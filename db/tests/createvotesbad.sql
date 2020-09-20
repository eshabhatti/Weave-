-- Dummy data file.
-- Tries to create a series of fake votes. None of these queries should succeed.
-- Make sure to run 'createusers.sql' and 'createposts.sql' and 'createvotes.sql' before running this file.
-- MySQL workbench should let you run queries individually if the script stops after the first error.

-- These queries should fail because of incorrect constraints.
-- Note that the backend should catch these errors before they ever hit the SQL database.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- User tries to vote on the same post twice
-- This means that the database will need to UPDATE the vote rather than make a new one if the user wants to switch
INSERT INTO PostVote
VALUES (
    "realuser2",
	006,
    -1
);

-- Unknown user tries to vote on a post
INSERT INTO PostVote
VALUES (
    "fakeuser1",
    006,
    -1
);

-- User tries to vote on unknown posts
INSERT INTO PostVote
VALUES (
    "SneakySpy",
    404,
    1
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
