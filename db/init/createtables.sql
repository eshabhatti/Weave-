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
-- 		encrypted_password: user password hashed with bcrypt; bcrypt includes the salt along with the hash
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

-- NOTE: When topics are added, their table needs to be initialized here.

-- Initializes the Post Table
-- If album posts are allowed, this table will need to be modified
-- ATTRIBUTE DESCRIPTIONS:
-- 		post_id: Unique ID value assigned to a post upon creation
-- 		topic_name: The one topic that the post is assigned to; foreign key that applies to Topic
-- 			NOTE: For now, just assign this value as "null" or "general"
-- 		creator: The creator of the post's username; foreign key that applies to UserAccount
-- 		date_created: The date of the post's creation
-- 		post_type: A flag that states whether the post is pure text (1) or picture-caption (2) -- maybe not needed?
-- 		title: A string that holds the post's title
-- 		content: A string that completely holds a text post's content; in a picture-caption post, this holds the caption
-- 		pic_path: A filepath to the picture that is assigned to the post
-- 		upvote_count: The total number of upvotes the post has (initialized to 0)
-- 		downvote_count: The total number of downvotes the post has (initialized to 0)
-- 		anon_flag: A flag that marks whether (1) or not (0) the post is anonymous
-- 		moderation_status: an integer flag corresponding to the post's moderation status
-- 			NOTE: For now, this attribute will always be set to 0
CREATE TABLE Post (
    post_id INT NOT NULL,
    topic_name VARCHAR(30) NOT NULL,
    creator VARCHAR(20) NOT NULL,
    date_created DATE NOT NULL,
    post_type INT NOT NULL,
    title VARCHAR(75) NOT NULL,
    content VARCHAR(750),
    pic_path VARCHAR(100), 
    upvote_count INT NOT NULL,
    downvote_count INT NOT NULL,
    anon_flag INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (creator) REFERENCES UserAccount(username)    
);

-- Initializes the SavedPost table.
-- Note that users can save their own posts on a database level. This can be prevented by the backend.
-- ATTRIBUTE DESCRIPTIONS: 
-- 		username: The user who saved the post
-- 		post_id: The post that the user saved
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair
-- 		date_saved: The date that the post was saved
CREATE TABLE SavedPost (
    username VARCHAR(20) NOT NULL,
    post_id INT NOT NULL,
    date_saved DATE NOT NULL,
    PRIMARY KEY (username, post_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username),
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);

-- Initializes the PostVote table.
-- ATTRIBUTE DESCRIPTIONS:
-- 		username: The user who voted on the post
-- 		post_id: The post that the user saved
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair
-- 		score: A flag representing an upvote (1) or downvote (-1)
CREATE TABLE PostVote (
    username VARCHAR(20) NOT NULL,
    post_id INT NOT NULL,
    score INT NOT NULL,
    PRIMARY KEY (username, post_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username),
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);
