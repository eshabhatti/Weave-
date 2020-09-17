-- If you're in MySQL workbench, you can ctrl + enter to run current query.
-- You can also do ctrl + shift + enter to run the whole query.
-- These options are avaliable under the query tab as well.
-- Somehow we need to host one server that everyone can access all the time.

-- Creates database and then selects it for use.
-- The create statement only can be run ONCE.
-- The use statement will need to be run for every use of the database.
CREATE DATABASE example;
USE example;

-- Shows all databases on your machine.
-- SHOW DATABASES;

-- Shows the current database in use.
-- SELECT database();

-- Creates a dummy table with some dummy attributes.
-- Note that each column will be separated by a comma.
-- VARCHAR is the standard string, but I don't think SQL allows it to be 100% dynamic.
-- DATE and INT and CHAR are other "data types" we can use. (There are others too.)
-- PRIMARY KEY determines the primary key (unique identifier) of the table.
-- NOT NULL states that the column cannot have a null value. CHECK can check other conidtions.
-- UNIQUE states that the value in the column must be unique, for email + username. 
CREATE TABLE Dummy (
	username VARCHAR(20) NOT NULL,
    realname VARCHAR(20) NOT NULL,
    description VARCHAR(150),
    date_of_birth DATE,
    PRIMARY KEY (username)
);

-- Loads a single instance into the table. This will probably be how the backend adds stuff.
-- We could also load from a filepath but I think that would mostly be backup files.
-- Note that DATE is in the format YYYY-MM-DD
-- Double quotes can be used interchangeably with single quotes. 
INSERT INTO Dummy 
VALUES ("Dummy1", "Joe Schmoe", "I am a guy.", "1912-12-12");

INSERT INTO Dummy
VALUES ("Dummy2", "Bob Jobs", "I am also a guy.", "2001-11-03");

INSERT INTO Dummy
VALUES ("Dummy3", "Killian Million", NULL, "1998-05-21");

-- SELECT * will select all information in the tables but that probably be used for debugging.
SELECT *
FROM Dummy
;

-- Basic query statement.
-- Follows the format SELECT [info] FROM [table] WHERE [conditon] ...
-- 		... ORDER BY [condition] GROUP BY [attribute] ;
-- The MySQL workbench puts a NULL value at the end of the table it shows you.
SELECT username 
FROM Dummy
WHERE description IS NOT NULL
ORDER BY realname
; 

-- Creates another table, but this time the tables will be linked with a foreign key.
-- The foreign key relates to a primary key in another table.
CREATE TABLE Post (
	post_id INT NOT NULL,
    content VARCHAR(750),
    creator_username VARCHAR(20),
    PRIMARY KEY (post_id),
    FOREIGN KEY (creator_username) REFERENCES Dummy(username) 
);

INSERT INTO Post
VALUES (1, "blah blah blah", "Dummy1");

INSERT INTO Post
VALUES (2, "blah blah blah blah", "Dummy1");

INSERT INTO Post
VALUES (3, "blah blah", "Dummy2");

INSERT INTO Post
VALUES (4, "blah", "Dummy3");

-- Joining tables in a select statement is done based on the foreign key, essentially. 
-- This will allow us to see who posts what and things like that.
-- Note that AS can be used to simplify names of things in the database for long WHERE statements.
SELECT D.realname, P.content
FROM Post AS P, Dummy AS D
WHERE P.creator_username = D.username AND D.username = "Dummy1"
;

-- Kills a specific table. We shouldn't have to do this much.
DROP TABLE Post;

-- Kills the database forever.
DROP DATABASE example;