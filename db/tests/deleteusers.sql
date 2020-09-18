-- Dummy data file.
-- Deletes all data in the UserAccount table that 'createusers.sql' will create.
DELETE FROM UserAccount WHERE username = "realuser1";
DELETE FROM UserAccount WHERE username = "realuser2";
DELETE FROM UserAccount WHERE username = "realuser3";
DELETE FROM UserAccount WHERE username = "SneakySpy";

-- Deletes all data in the UserAccount table that 'createusersbad.sql' will create
--     if the 'createusers.sql' is not run first. 
DELETE FROM UserAccount WHERE username = "fakeuser1";

-- Selects all the data from the UserAccount table to make sure deletion was a success.
SELECT *
FROM UserAccount
;

-- Alternatively, you could turn off safe update mode and simply run:
-- DELETE FROM UserAccount;
