-- Dummy data file.
-- Tries to create a series of fake users. None of these queries should succeed.
-- Make sure to run 'createusers.sql' before running this file.
-- MySQL workbench should let you run queries individually if the script stops after the first error.

-- These queries should fail because of incorrect attribute constraints.
-- Further tests probably don't need to have most of these. I just wanted to make sure I still understand SQL.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Incorrect column number.
INSERT INTO UserAccount
VALUES (
    "realuser3",
    "t8lBTZKRH7gECPa3CPBKWJXm5zDtuyREdMRszg6iSu2LLLgwLloFZgRWVJofcHSL",
    "Real",
    "Userman",
    "1990-10-10",
    "I do not like how this database works. >:(",
    NULL,
    0,
    0
);

-- NOT NULL value is set as NULL
INSERT INTO UserAccount
VALUES (
    "realuser3",
    "ohialmostforgotanemail@hotmail.com",
    "t8lBTZKRH7gECPa3CPBKWJXm5zDtuyREdMRszg6iSu2LLLgwLloFZgRWVJofcHSL",
    "Real",
    "Userman",
    NULL,
    "I do not like how this database works. >:(",
    NULL,
    0,
    0
);

-- Incorrect password length (too long).
-- NOTE: SQL does not check for strings that are too short. If this is expected to be set, the backend will have to handle it.
INSERT INTO UserAccount
VALUES (
    "realuser3",
    "ohialmostforgotanemail@hotmail.com",
    "t8lBTZKRH7gECPa3CPBKWJXm5zDtuSu2LLLgwLloFZgRWVJofcHSLt8lBTZKRH7gECPa3CPBKWJXm5zDtuSu2LLLgwLloFZgRWVJofcHSL",
    "Real",
    "Userman",
    "1990-10-10",
    "I do not like how this database works. >:(",
    NULL,
    0,
    0
);

-- Incorrect date format
INSERT INTO UserAccount
VALUES (
    "realuser3",
    "ohialmostforgotanemail@hotmail.com",
    "t8lBTZKRH7gECPa3CPBKWJXm5zDtuyREdMRszg6iSu2LLLgwLloFZgRWVJofcHSL",
    "Real",
    "Userman",
    "1900-20-10",
    "I do not like how this database works. >:(",
    NULL,
    0,
    0
);

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- These queries should fail because of incorrect constraints.
-- These are the important tests that probably every table should have.
-- Note that the backend should catch these errors before they ever hit the SQL database.
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Repeated username
INSERT INTO UserAccount
VALUES (
    "realuser3",
    "ohialmostforgotanemail@hotmail.com",
    "t8lBTZKRH7gECPa3CPBKWJXm5zDtuyREdMRszg6iSu2LLLgwLloFZgRWVJofcHSL",
    "Real",
    "Userman",
    "1900-02-10",
    "I do not like how this database works. >:(",
    NULL,
    0,
    0
);

-- Repeated email
INSERT INTO UserAccount
VALUES (
    "fakeuser1",
    "exampleuser@gmail.com",
    "t8lBTZKRH7gECPa3CPBKWJXm5zDtuyREdMRszg6iSu2LLLgwLloFZgRWVJofcHSL",
    "Real",
    "Userman",
    "1900-02-10",
    "I do not like how this database works. >:(",
    NULL,
    0,
    0
);
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
