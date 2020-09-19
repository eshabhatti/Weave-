-- Dummy data file.
-- Tries to create a series of fake users. None of these queries should succeed.
-- Make sure to run 'createusers.sql' and 'createposts.sql' and 'createsaves.sql' before running this file.
-- MySQL workbench should let you run queries individually if the script stops after the first error.

-- These queries should fail because of incorrect constraints.
-- Note that the backend should catch these errors before they ever hit the SQL database.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- User tries to save the same post twice
INSERT INTO SavedPost
VALUES (
    "SneakySpy",
	004,
    "2020-09-15"
);

-- Unknown user tries to save a post
INSERT INTO SavedPost
VALUES (
    "fakeuser1",
    004,
    "2020-09-15"
);

-- User tries to save unknown posts
INSERT INTO SavedPost
VALUES (
    "SneakySpy",
    404,
    "2020-09-15"
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
