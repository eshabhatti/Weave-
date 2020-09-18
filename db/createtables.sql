-- This will be the general constructor for Weave's database.
-- All tables needed for the database will be created, along with the database itself.
-- Format is:
-- 		CREATE TABLE TableName (
-- 			column_attribute TYPE OTHER_CONDITIONS,
-- 			column_attribute TYPE OTHER_CONDITIONS,
-- 			... ,
-- 			PRIMARY KEY (column_attribute),
-- 			FOREIGN KEY (column_attribute) REFERENCES ReferenceTable(reference_attribute)
-- 		);

-- Initializes the database.
CREATE DATABASE weave;
USE weave;

-- Initializes the user table.
-- 'USER' is a keyword in SQL which is the reason for the long table name.
-- ATTRIBUTE DESCRIPTIONS:
-- 		username: plaintext username with a maximum of 20 characters
-- 		email: plaintext email that the user's account is connected with
-- 		encrypted_password: user password hashed with scrypt (output will be locked at 64 bytes?)
-- 		password_salt: (cyprtographically) random value to be appended to password before hash (locked at 16 bytes?)
-- 		first_name: optional value that represents the user's first name
-- 		last_name: optional value that represents the user's last name
-- 			NOTE: These names are separated to make injection attacks harder.
-- 		date_joined: the date corresponding to when the user created their account
-- 		user_bio: the optional biography description attached to a user account
-- 		user_pic: the optional filepath to the user's profile picture (length may be too long?)
-- 		follower_count: an integer corresponding to the user's follower count
-- 		moderation_status: an integer flag corresponding to the user's moderation status
-- 			NOTE: For now, the above two attributes will always be set to 0
CREATE TABLE UserAccount (
    username VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    encrypted_password CHAR(64) NOT NULL,
    password_salt CHAR(16) NOT NULL,
    first_name VARCHAR(15),
    last_name VARCHAR(15),
    date_joined DATE NOT NULL,
    user_bio VARCHAR(250),
    user_pic VARCHAR(100), 
    follower_count INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (username),
    UNIQUE (email)
);
