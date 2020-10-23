INSERT INTO UserAccount
VALUES (
	'followtest_1',
    'ABCabc777@password.com',
    '$2b$12$3.iOc2fUVKz2f7gjLu2pi.ZQP87RxBWSXmcGmeTKGZf9DEuIMCDwi',
    NULL,
    NULL,
    '2020-10-16 13:22:31',
    NULL,
    NULL,
    '0',
    '0'
);

INSERT INTO UserAccount
VALUES (
	'followtest_2', 
    'BCAbac1@password.org',
    '$2b$12$rK4RleKHCA3qjOd7WoQPfe36Seu3CJegVG5kIyw3f23kXiEYrhlpK',
    NULL,
    NULL,
    '2020-10-16 11:20:22',
    NULL,
    NULL,
    '0',
    '0'
);

INSERT INTO Topic
VALUES (
	'art',
    '2020-10-16 14:02:11',
    0,
    0
);

INSERT INTO Topic
VALUES (
	'cats',
    '2020-10-16 23:23:23',
    0,
    0
);

INSERT INTO Post
VALUES (
	004,
    'general',
    'followtest_1',
    '2020-10-17 21:22:22',
    'Invisible Post 1',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	005,
    'art',
    'followtest_1',
    '2020-10-17 21:22:22',
    'Visible Post 2',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	006,
    'cats',
    'followtest_1',
    '2020-10-17 12:21:34',
    'Invisible Post 4',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	007,
    'general',
    'followtest_2',
    '2020-10-17 20:22:22',
    'Visible Post 4',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	008,
    'art',
    'followtest_2',
    '2020-10-17 23:22:22',
    'Visible Post 5',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post
VALUES (
	009,
    'art',
    'followtest_1',
    '2020-10-17 23:22:22',
    'Visible Post 6',
    'This post should show in the final select statement',
    NULL,
    0,
    0,
    1,
    0
);

INSERT INTO Post
VALUES (
	010,
    'general',
    'followtest_2',
    '2020-10-17 23:22:22',
    'Invisible Post 2',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    1,
    0
);

INSERT INTO Post
VALUES (
    011,
    'general',
    'testname',
    '2020-10-17 22:22:22',
    'Invisible Post 3',
    'This post should not show in the final select statement',
    NULL,
    0,
    0,
    1,
    0
);