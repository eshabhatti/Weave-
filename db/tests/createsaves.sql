-- Dummy data file.
-- Creates a series of fake saved posts.
-- Run this after 'createusers.sql' and 'createposts.sql' to get the intended effect.

-- These queries should perform correctly.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

INSERT INTO SavedPost 
VALUES (
    "SneakySpy",
    001,
    "2020-09-10"
);

INSERT INTO SavedPost 
VALUES (
    "realuser2",
    001,
    "2020-09-10"
);

INSERT INTO SavedPost
VALUES (
    "realuser1",
    005,
    "2020-09-11"
);

INSERT INTO SavedPost
VALUES (
    "SneakySpy",
    003,
    "2020-09-11"
);

INSERT INTO SavedPost
VALUES (
    "realuser2",
    005,
    "2020-09-11"
);

INSERT INTO SavedPost
VALUES (
    "SneakySpy",
    004,
    "2020-09-11"
);

INSERT INTO SavedPost
VALUES (
    "SneakySpy",
    005,
    "2020-09-11"
);

INSERT INTO SavedPost
VALUES (
    "realuser3",
    006,
    "2020-09-12"
);

INSERT INTO SavedPost
VALUES (
    "realuser3",
    008,
    "2020-09-12"
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Querys the current database to make sure the data was correctly inserted into the tables.
SELECT *
FROM SavedPost
;
