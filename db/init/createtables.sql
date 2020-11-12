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
-- 'USER' is a keyword in SQL, which is the reason for the long table name.
-- ATTRIBUTE DESCRIPTIONS:
-- 		username: Plaintext username with a maximum of 20 characters
-- 		email: Plaintext email that the user's account is connected with
-- 		encrypted_password: User password hashed with bcrypt; bcrypt includes the salt along with the hash
-- 		first_name: Optional value that represents the user's first name
-- 		last_name: Optional value that represents the user's last name
-- 		date_joined: The date and time corresponding to when the user created their account
-- 		user_bio: The optional biography description attached to a user account
-- 		user_pic: The optional filepath to the user's profile picture
-- 		follower_count: An integer corresponding to the user's follower count
-- 		moderation_status: An integer flag corresponding to the user's moderation (deletion) status
CREATE TABLE UserAccount (
    username VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    encrypted_password CHAR(64) NOT NULL,
    first_name VARCHAR(15),
    last_name VARCHAR(15),
    date_joined DATETIME NOT NULL,
    user_bio VARCHAR(250),
    user_pic VARCHAR(100), 
    follower_count INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (username),
    UNIQUE (email)
);

-- Initializes the Topic Table
-- Topic descriptions aren't implemented for the time being, but they may be added later.
-- ATTRIBUTE DESCRIPTIONS:
-- 		topic_name: The UNIQUE name of the topic at 50 characters maximum
-- 		date_created: The date and time that the first post in this topic was created
-- 		follower_count: An integer that represents how many users follow this topic
-- 		moderation_status: An integer flag corresponding to topic moderation
-- 			NOTE: For now, this attribute will always be set to 0; it may be removed later. 
CREATE TABLE Topic (
	topic_name VARCHAR(50) NOT NULL,
    date_created DATETIME NOT NULL,
    follower_count INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (topic_name)
);

-- Initializes the Post Table
-- If album posts are ever allowed, this table will need to be modified
-- ATTRIBUTE DESCRIPTIONS:
-- 		post_id: Unique ID value assigned to a post upon creation
-- 		topic_name: The one topic that the post is assigned to; foreign key that applies to Topic
-- 		creator: The creator of the post's username; foreign key that applies to UserAccount
-- 		date_created: The date and time of the post's creation
-- 		post_type: A flag that states whether the post is pure text (1) or picture-caption (2) -- maybe not needed?
-- 		title: A string that holds the post's title
-- 		content: A string that completely holds a text post's content; in a picture-caption post, this holds the caption
-- 		pic_path: A filepath to the picture that is assigned to the post
-- 		upvote_count: The total number of upvotes the post has (initialized to 0)
-- 		downvote_count: The total number of downvotes the post has (initialized to 0)
-- 		anon_flag: A flag that marks whether (1) or not (0) the post is anonymous
-- 		moderation_status: an integer flag corresponding to the post's moderation status
-- 			NOTE: For now, this attribute will always be set to 0; it may be removed later. 
CREATE TABLE Post (
    post_id INT NOT NULL,
    topic_name VARCHAR(50) NOT NULL,
    creator VARCHAR(20) NOT NULL,
    date_created DATETIME NOT NULL,
    title VARCHAR(75) NOT NULL,
    content VARCHAR(750),
    pic_path VARCHAR(100), 
    upvote_count INT NOT NULL,
    downvote_count INT NOT NULL,
    anon_flag INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (creator) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (topic_name) REFERENCES Topic(topic_name)
);

-- Initializes the Comment table.
-- 'COMMENT' is also a keyword in SQL, which is the reason for the long table name.
-- ATTRIBUTE DESCRIPTIONS: 
-- 		comment_id: Unique ID assigned upon comment creation
-- 		post_parent: The ID of the post that the comment is attached to
-- 		user_parent: The username of the account that made the comment
-- 		comment_parent: The ID of the comment that this comment is a reply to 
-- 			NOTE: If the comment is not a reply, this attribute should be 0.
-- 		date_created: The date and time at which this comment was created
-- 		content: A string representing the body of the comment, with a maximum of 400 characters
-- 		upvote_count: An integer representing the total number of upvotes on this comment
-- 		downvote_count: An integer representing the total number of downvotes on this comment
-- 		moderation_status: an integer flag corresponding to the comment's moderation status
-- 			NOTE: For now, this attribute will always be set to 0; it may be removed later. 
CREATE TABLE PostComment (
	comment_id INT NOT NULL,
    post_parent INT NOT NULL,
    user_parent VARCHAR(20) NOT NULL,
    comment_parent INT NOT NULL,
    date_created DATETIME NOT NULL,
    content VARCHAR(400) NOT NULL,
    upvote_count INT NOT NULL,
    downvote_count INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_parent) REFERENCES Post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_parent) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Initializes the SavedPost table.
-- ATTRIBUTE DESCRIPTIONS: 
-- 		username: The user who saved the post
-- 		post_id: The post that the user saved
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair.
-- 		date_saved: The date and time that the post was saved
CREATE TABLE SavedPost (
    username VARCHAR(20) NOT NULL,
    post_id INT NOT NULL,
    date_saved DATETIME NOT NULL,
    PRIMARY KEY (username, post_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE, 
    FOREIGN KEY (post_id) REFERENCES Post(post_id) ON DELETE CASCADE
);

-- Initializes the PostVote table.
-- ATTRIBUTE DESCRIPTIONS:
-- 		username: The user who voted on the post
-- 		post_id: The post that the user voted on
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair.
-- 		score: A flag representing an upvote (1) or downvote (-1)
CREATE TABLE PostVote (
    username VARCHAR(20) NOT NULL,
    post_id INT NOT NULL,
    score INT NOT NULL,
    PRIMARY KEY (username, post_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(post_id) ON DELETE CASCADE
);

-- Initializes the PostVote table.
-- ATTRIBUTE DESCRIPTIONS:
-- 		username: The user who voted on the post
-- 		comment_id: The comment that the user saved
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair.
-- 		score: A flag representing an upvote (1) or downvote (-1)
CREATE TABLE CommentVote (
	username VARCHAR(20) NOT NULL,
    comment_id INT NOT NULL,
    score INT NOT NULL,
	PRIMARY KEY (username, comment_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES PostComment(comment_id) ON DELETE CASCADE
);

-- Initializes the FollowUser table.
-- Note that users can technically follow themselves, but the backend should be able to handle this.
-- ATTRIBUTE DESCRIPTIONS:
-- 		user_follower: The user who is following someone
-- 		user_followed: The user who is being followed by someone
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair.
CREATE TABLE FollowUser (
	user_follower VARCHAR(20) NOT NULL,
    user_followed VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_follower, user_followed),
    FOREIGN KEY (user_follower) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_followed) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Initializes the FollowTopic table.
-- ATTRIBUTE DESCRIPTIONS:
-- 		user_follower: The user who is following the topic
-- 		topic_followed: The topic that is being followed by the user
-- 			NOTE: The above two elements form the primary key; there cannot be a duplicate pair.
CREATE TABLE FollowTopic (
	user_follower VARCHAR(20) NOT NULL,
    topic_followed VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_follower, topic_followed),
    FOREIGN KEY (user_follower) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (topic_followed) REFERENCES Topic(topic_name)
);

-- Initializes the DirectMessage table.
-- Note that users can technically send messages to themselves, but the backend should be able to handle this.
-- When we modify account deletion, we may want to make sure that the correct usernames update to DELETED.
-- ATTRIBUTE DESCRIPTIONS:
-- 		message_id: A unique ID assigned to each direct message
-- 		sender: A username string corresponding to who sent the message
-- 		receiver: A username string corresponding to who should get the message
-- 		sender_status: A flag corresponding to whether or not the sender has deleted the message
-- 		receiver_status: A flag corresponding to whether or not the receiver has deleted the message
-- 			NOTE: For both of the flags above, a value of 0 means the message has been deleted.
-- 		content: A string representing the content of the message. 500 characters maximum.
-- 		date_created: A datetime field representing when the message was first sent. 
CREATE TABLE DirectMessage (
	message_id INT NOT NULL,
    sender VARCHAR(20) NOT NULL,
    receiver VARCHAR(20) NOT NULL,
    sender_status INT NOT NULL,
    receiver_status INT NOT NULL,
    content VARCHAR(500) NOT NULL,
    date_created DATETIME NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (sender) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (receiver) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Initializes the UserBlock table.
-- Note that users can technically block themselves. This would be problematic if the application allows it to happen.
-- ATTRIBUTE DESCRIPTIONS:
-- 		user_blocker: A username string corresponding to the blocking user in the relation (who pushed the button).
-- 		user_blocked: A username string corresponding to the blocked user in the relation (whose button was pushed).
CREATE TABLE UserBlock (
	user_blocker VARCHAR(20) NOT NULL,
    user_blocked VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_blocker, user_blocked),
	FOREIGN KEY (user_blocker) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_blocked) REFERENCES UserAccount(username) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Initializes the Blacklist table.
-- ATTRIBUTE DESCRIPTIONS:
-- 		token: The JWT token that needs to be blacklisted
CREATE TABLE Blacklist (
	token VARCHAR(256) NOT NULL,
    PRIMARY KEY (token)
);


-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- Adds the 'DELETED' user into the database to hold posts and comments of deleted users.
-- The password should not match anything and thus be inaccessible on the frontend.
INSERT INTO UserAccount
VALUES (
    "DELETED",
    "admin@weave.com",
    "XAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAXAX",
    "Deleted",
    "Graveyard",
    "2020-10-28 07:31:11",
    "This is a fake account that holds all posts and comments from users who have deleted their accounts", 
    NULL, 
    0, 
    0
);

-- Adds the 'general' topic to Weave into the database for visitor functionality.
-- Depending on how we set things up on the frontend, this may not be explicitly needed.
INSERT INTO Topic
VALUES (
    "general",
    "2020-11-12 01:28:30",
    0,
    0
);