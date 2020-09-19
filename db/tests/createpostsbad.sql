-- Dummy data file.
-- Tries to create a series of fake users. None of these queries should succeed.
-- Make sure to run 'createusers.sql' and 'createposts.sql' before running this file.
-- MySQL workbench should let you run queries individually if the script stops after the first error.

-- These queries should fail because of incorrect constraints.
-- Note that the backend should catch these errors before they ever hit the SQL database.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Repeated Post ID
INSERT INTO Post
VALUES (
    009,
    "general",
    "realuser1",
    "2020-09-13",
    1,
    "I also agree.",
    "/resources/postimages/agree.png",
    0,
    0,
    1,
    0
);

-- Post is not assigned to a real username
INSERT INTO Post
VALUES (
   010,
   "general",
   "fakeuser1",
   "2020-10-10",
   1,
   "I am not real. Can I still post?",
   NULL,
   0,
   0,
   0,
   0
);

-- There will need to be another test here that makes sure posts cannot be assigned to fake topics
-- (This means that the backend needs to create the topic before the post)

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
