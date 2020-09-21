-- Dummy data file.
-- Creates a series of fake users to make sure that the UserAccount Table was intialized correctly.
-- Run this before running any other user test files.

-- These queries should perform correctly.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
INSERT INTO UserAccount
VALUES (
    "realuser1",
    "exampleuser@gmail.com",
    "ok3sKPXDGU7hZl6Ui3hgec2JpZu7gZ8K0giyQh5oInNSYj9vV7qM0g4mawZv6aGq",
    "Real",
    "User",
    "1998-12-12",
    NULL, 
    NULL, 
    0, 
    0
);
    
INSERT INTO UserAccount
VALUES (
    "realuser2",
    "exampleuser2@aol.com",
    "VzRtsKzMP84NkoWbwFJDU6kl6He5BXUaDgq3ohNVkH84PMrKZSztseuJ6DMVEZqp",
    "Joe",
    "Schmoe",
    "2002-02-04",
    "Holy smokes I have an actual description this time, but I don't have a filepath for the caption because IDK.",
    NULL, 
    0, 
    0
);

INSERT INTO UserAccount
VALUES (
    "realuser3",
    "exampleuser@hotmail.com",
    "eo6683V5PAHmTsqLHL2qGTiYs7tFB64FICL31jIWPzjz7UPvs1mfmzXiSTXgvLvg",
    NULL, 
    NULL,
    "2000-08-22",
    "Hahaha I do not have a name but I do have a description and a profile picture. Strange, isn't it?",
    "\resources\profiles\example.png",
    0, 
    0
);

INSERT INTO UserAccount
VALUES (
    "SneakySpy",
    "sneakyuser@gmail.com",
    "bUulldwxu6c61jGsnGCFJXnwQkVQfUiqhahimhuSm7Gx48iBh9gLwWL64gLxYcZK",
    NULL,
    NULL,
    "1999-09-17",
    NULL,
    NULL,
    0,
    0
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Querys the current database to make sure the data was correctly inserted into the tables.
SELECT *
FROM UserAccount
;
