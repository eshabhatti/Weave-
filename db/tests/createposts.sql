-- Dummy data file.
-- Creates a series of fake users to make sure that the UserAccount Table was intialized correctly.
-- Run this after 'createusers.sql' to get the intended effect.

-- These queries should perform correctly.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
INSERT INTO Post
VALUES (
    001,
    "general",
    "realuser1",
    "2020-09-10",
    1,
    "Hello World",
    "Hello everyone, this is the first post on Weave. Isn't it so cool? I think it is pretty cool. That is why I have used cool twice in two sentences. Now thrice in three sentences!",
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
    002,
    "general",
    "realuser2",
    "2020-09-10",
    1,
    "You Suck",
    "Actually, I don't think it is that cool to be the first post on Weave. You are not even real, realuser1.",
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
   003,
   "general",
   "realuser1",
   "2020-09-11",
   1,
   "Rude!",
   "Wow, you are so rude realuser2. I bet you are not even real yourself.",
   NULL,
   0,
   0,
   0,
   0
);

INSERT INTO Post
VALUES (
    004,
    "general",
    "realuser1",
    "2020-09-11",
    1,
    "I agree with my husband.",
    "Yes I agree with realuser1, you are very rude realuser2",
    NULL,
    0,
    0,
    1,
    0
);

INSERT INTO Post
VALUES (
    005,
    "general",
    "realuser3",
    "2020-09-12",
    2,
    "Wow Look At This",
    "Wow guys you can put pictures here on Weave as well, isn't that cool?",
    "/resources/postimages/coolimg.png",
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
    006,
    "general",
    "realuser2",
    "2020-09-12",
    1,
    "Shut Up",
    "Shut up realuser3 no one likes your pictures either",
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
    007,
    "general",
    "realuser3",
    "2020-09-12",
    2,
    "You Make Me Sad",
    NULL,
    "/resources/postimages/crying.png",
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
   008,
   "general",
   "realuser1",
   "2020-09-13",
   1,
   "You are so MEAN",
   "Wow you are so mean realuser2, you should be smited off this website.",
   NULL,
   0,
   0,
   0,
   0
);

INSERT INTO Post
VALUES (
    009,
    "general",
    "realuser1",
    "2020-09-13",
    1,
    "AGREE",
    "I agree.",
    "/resources/postimages/agree.png",
    0,
    0,
    1,
    0
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Querys the current database to make sure the data was correctly inserted into the tables.
SELECT *
FROM Post
;
