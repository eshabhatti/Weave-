-- This is just a copy of 'createtables.sql' that will be used for testing.

CREATE DATABASE weave;
USE weave;

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

CREATE TABLE Topic (
	topic_name VARCHAR(50) NOT NULL,
    date_created DATETIME NOT NULL,
    follower_count INT NOT NULL,
    moderation_status INT NOT NULL,
    PRIMARY KEY (topic_name)
);

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
    FOREIGN KEY (creator) REFERENCES UserAccount(username) ON UPDATE CASCADE,
    FOREIGN KEY (topic_name) REFERENCES Topic(topic_name)
);

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
    FOREIGN KEY (post_parent) REFERENCES Post(post_id),
    FOREIGN KEY (user_parent) REFERENCES UserAccount(username) ON UPDATE CASCADE
);

CREATE TABLE SavedPost (
    username VARCHAR(20) NOT NULL,
    post_id INT NOT NULL,
    date_saved DATETIME NOT NULL,
    PRIMARY KEY (username, post_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username) ON UPDATE CASCADE, 
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);

CREATE TABLE PostVote (
    username VARCHAR(20) NOT NULL,
    post_id INT NOT NULL,
    score INT NOT NULL,
    PRIMARY KEY (username, post_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username) ON UPDATE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
);

CREATE TABLE CommentVote (
	username VARCHAR(20) NOT NULL,
    comment_id INT NOT NULL,
    score INT NOT NULL,
	PRIMARY KEY (username, comment_id),
    FOREIGN KEY (username) REFERENCES UserAccount(username) ON UPDATE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES PostComment(comment_id)
);

CREATE TABLE FollowUser (
	user_follower VARCHAR(20) NOT NULL,
    user_followed VARCHAR(20) NOT NULL,
    PRIMARY KEY (user_follower, user_followed),
    FOREIGN KEY (user_follower) REFERENCES UserAccount(username),
    FOREIGN KEY (user_followed) REFERENCES UserAccount(username)
);

CREATE TABLE FollowTopic (
	user_follower VARCHAR(20) NOT NULL,
    topic_followed VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_follower, topic_followed),
    FOREIGN KEY (user_follower) REFERENCES UserAccount(username),
    FOREIGN KEY (topic_followed) REFERENCES Topic(topic_name)
);

CREATE TABLE Blacklist (
	token VARCHAR(256) NOT NULL,
    PRIMARY KEY (token)
);