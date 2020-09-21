-- This file holds example scripts that show how to properly insert data into the database.
-- Only the tables created for sprint one will be expalained here.
-- Note that 'createtables.sql' must be run for any data to be allowed into the database.

-- In general, to insert an entity into some table [TableName], write:
-- 		INSERT INTO [TableName] VALUES (attribute, attribute, attribute);
-- Note that spaces, newlines, and other whitespace should not matter. 

-- TO INSERT AN ENTITY THAT REPRESENTS A USER:
-- 		INSERT INTO UserAccount
-- 		VALUES (
-- 			username: a unique string corresponding to the chosen username; must be 20 characters or less
-- 			email: a unique string corresponding to the user's email; must be 50 characters or less
-- 			encrypted password: a string corresponding to the hash of the user's password; will likely be set at 64 characters
-- 			password salt: a string corresponding to the user's random salt; will likely be set at 16 characters
-- 			first name: a string representing the user's first name; can be NULL
-- 			last name: a string representing the user's last name; can be NULL
-- 			date joined: a date string representing when the user joined Weave IN THE FORMAT "YYYY-MM-DD"
-- 			user bio: a string that holds the user's personal bio; can be NULL; must be 250 characters or less
-- 			user pic: a string that holds the filepath to the user's profile picture; can be NULL; must be 100 characters or less
-- 			follower count: an integer that corresponds to how many others follow this user; always set this to 0 for now
-- 			moderation status: an integer that flags the mod status of the user; always set this to 0 for now
-- 		);
-- Assuming that the user can only set their name, bio, and profile pic after account creation,
-- an example of adding a new user account into the database would be:
INSERT INTO UserAccount
VALUES (
    "realuser1",                                                              -- username
    "exampleuser@gmail.com",                                                  -- email
    "ok3sKPXDGU7hZl6Ui3hgec2JpZu7gZ8K0giyQh5oInNSYj9vV7qM0g4mawZv6aGq",       -- encrypted_password
    "cdF2PK6FrPctt7Hn",                                                       -- password_salt
    NULL,                                                                     -- first_name
    NULL,                                                                     -- last_name
    "2020-9-20",                                                              -- date_joined
    NULL,                                                                     -- user_bio
    NULL,                                                                     -- user_pic
    0,                                                                        -- follower_count
    0                                                                         -- moderation_status
);

-- TO INSERT AN ENTITY THAT REPRESENTS A POST:
-- 		INSERT INTO Post
-- 		VALUES (
-- 			post_id: a unique integer that identifies the post
-- 			topic_name: a string that corresponds to the post's topic; 30 characters max; always set this to "general" for now
-- 			creator: a string that MUST correspond exactly to a username in the UserAccount table
-- 			date_created: a date string representing when the post was created IN THE FORMAT "YYYY-MM-DD"
-- 			post_type: an integer flag set to 1 if the post is text and set to 2 if the post is picture-caption
-- 			title: a string holding the text corresponding to the post's title; 75 characters max; CANNOT BE NULL
-- 			content: a string holding either a text post or the picture's caption; 750 characters max; can be NULL (picture but no caption)
-- 			pic_path: a string holding a filepath to the post's picture; 100 characters max; can be NULL
-- 			upvote_count: an integer representing the post's total upvotes; initialize this as 0
-- 			downvote_count: an integer representing the post's total downvotes; initialize this as 0
-- 			anon_flag: an integer flag that is set to 0 if the post is not anonymous and set to 1 if it is
-- 			moderation_status: an integer that flags the mod status of the user; always set this to 0 for now
-- 		);
-- A non-anonymous text post may be first inserted into the database like so:
INSERT INTO Post
VALUES (
    101,                                                   -- post_id
    "general",                                             -- topic_name
    "realuser1",                                           -- creator
    "2020-9-20",                                           -- date_created
    1,                                                     -- post_type
    "text post",                                           -- title
    "text content text content text content",              -- content
    NULL,                                                  -- pic_path
    0,                                                     -- upvote_count
    0,                                                     -- downvote_count
    0,                                                     -- anon_flag
    0                                                      -- moderation_status
);
-- While an anonymous picture-caption post may instead be inserted like so:
INSERT INTO Post
VALUES (
    202,                                                   -- post_id
    "general",                                             -- topic_name
    "realuser1",                                           -- creator
    "2020-9-21",                                           -- date_created
    2,                                                     -- post_type
    "picture-caption post",                                -- title
    "text content text content text content",              -- content
    "/picfilepath/image.jpeg",                             -- pic_path
    0,                                                     -- upvote_count
    0,                                                     -- downvote_count
    1,                                                     -- anon_flag
    0                                                      -- moderation_status
);
-- NOTE THAT POSTS MAY NOT BE INSERTED INTO THE DATABASE UNLESS THEY HAVE A VALID USER TO CONNECT TO

-- TO INSERT A RELATIONSHIP ENTITY THAT REPRESENTS A SAVED POST:
-- 		INSERT INTO SavedPost
-- 		VALUES (
-- 			username: a string that MUST correspond exactly to a username in the UserAccount table
-- 			post_id: an integer that MUST correspond exactly to a username in the Post table
-- 			date_saved: a date string representing when the post was saved IN THE FORMAT "YYYY-MM-DD"
-- 		);
-- So if "realuser1" wanted to save the post 101, you would run the following statement:
INSERT INTO SavedPost
VALUES (
	"realuser1",                      -- username
    101,                              -- post_id
    "2020-09-20"                      -- date_saved
);
-- NOTE THAT SAVED POSTS MAY NOT BE INSERTED INTO THE DATABASE UNLESS THEY HAVE A VALID USER AND A VALID POST TO CONNECT TO

-- TO INSERT A RELATIONSHIP ENTITY THAT REPRESENTS AN UPVOTE/DOWNVOTE:
-- 		INSERT INTO PostVote
-- 		VALUES (
-- 			username: a string that MUST correspond exactly to a username in the UserAccount table
-- 			post_id: an integer that MUST correspond exactly to a username in the Post table
-- 			score: an integer flag set to 1 if the vote is upvote and -1 if the vote is a downvote
-- 		);
-- So if "realuser1" wanted to upvote post 101, you would run the following statement:
INSERT INTO PostVote
VALUES (
    "realuser1",                      -- username
    101,                              -- post_id
    "1"                               -- score
);
-- NOTE THAT POST VOTES MAY NOT BE INSERTED INTO THE DATABASE UNLESS THEY HAVE A VALID USER AND A VALID POST TO CONNECT TO
-- IMPORTANT: When adding a new vote into the database, you also need to update the post table.
-- You would generally do this using the following format:
-- 		UPDATE [TableName] SET [attribute = new_attribute] WHERE [condition];
-- Assuming the same situation as above, you would update the Post table by running:
UPDATE Post 
SET upvote_count = upvote_count + 1
WHERE post_id = 101
;
-- If the user ever wants to CHANGE their vote, then:
-- 		> The PostVote table's score column needs to be updated.
-- 		> The previous upvote/downvote needs to be removed from the Post table
-- 		> The new upvote/downvote needs to be added to the Post table
-- Assuming the same situation as above, you would change the user's vote with the following queries:
UPDATE PostVote SET score = -1 WHERE username = "realuser1" AND post_id = 101;    -- CHANGE POSTVOTE SCORE
UPDATE Post SET upvote_count = upvote_count - 1 WHERE post_id = 101;              -- REMOVE OLD VOTE FROM POST
UPDATE Post SET downvote_count = downvote_count + 1 WHERE post_id = 101;          -- ADD NEW VOTE TO POST

-- To see information on deleting data from the database, see 'sprintone_datadeletion.sql'.
