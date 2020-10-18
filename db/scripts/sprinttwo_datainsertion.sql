-- For the second sprint, this script will serve both as a set of creation tests and as a dummy data set.
-- Data for tables in both sprint one and sprint two will be intialized here.
-- Note that 'createtables.sql' must be run for any data to be allowed into the database.

-- At this point in time, it is assumed that most know the general format of the INSERT statement.
-- It is also assumed that you know the general format of inserting data from sprint one.
-- If this is not the case, see "scripts/sprintone_datainsertion.sql".

-- First, a set of users must be initialized.
-- Note that these user entities have passwords shown as the first part of the email address.
-- Note the modification from DATE to DATETIME.
INSERT INTO UserAccount 
VALUES (
	'realuser1',
    'ABCabc777@password.org',
    '$2b$12$j2OssNGwu/nhjLapAt4cBeaO61iXaFqmly3PLnl1PfUHUV.fPHwES',
    NULL,
    NULL,
    '2020-10-15 22:22:22',
    NULL,
    NULL,
    '0',
    '0'
);

INSERT INTO UserAccount
VALUES (
	'realuser2',
    'abcABC88@password.org',
    '$2b$12$rANOHjCeAsGx61ctkQGV8OJeCAM/2bQ5Zji1dZFyjFnmYtcBuX1MG',
    NULL,
    NULL,
    '2020-10-15 11:11:11',
    NULL,
    NULL,
    '0', 
	'0'
);

-- Before, we could enter posts into the database at this point. 
-- However, at the end of this sprint, the database will be constrained such that topics must be created first.
-- TO INSERT AN ENTITY THAT REPRESENTS A TOPIC:
-- 		INSERT INTO Topic
-- 		VALUES (
-- 			topic_name: a unique string of 50 characters maximum that represents the topic's name
-- 			date_created: a date and time that the first post in the topic was made IN THE FORMAT 'YYYY-MM-DD HH:MI:SS'
-- 			follower_count: an integer that tracks how many users follow this topic; set this to 0 for now 
-- 			moderation_status: an integer that tracks the moderation status of a topic; set this to 0 for now
-- 		);
INSERT INTO Topic
VALUES (
	"GENERAL",                                      -- topic_name
    "2020-10-15 12:04:12",                          -- date_created
    0,                                              -- follower_count
    0                                               -- moderation_status
);

-- Once topics are initialized, posts can be added like normal.
-- Again, however, each post needs to be attached to a valid topic name by the end of the sprint (THIS IS NOT A CONSTRAINT YET)
-- It may be easiest to uppercase all topic names before pushing to the database, and lowercase them again when pulled.
-- NOTE: The attribute TYPE for the Post table no longer exists. DO NOT INCLUDE IT IN ANY INSERTION OR SELECTION STATEMENTS.
-- Also note the modification from DATE to DATETIME.
INSERT INTO Post 
VALUES (
	001,
    "GENERAL",
    "realuser1",
    "2020-10-9 01:01:11",
    "text post",
    "text content text content text content",
    NULL,
    0,
    0,
    0,
    0
);

INSERT INTO Post 
VALUES (
	002, 
    "GENERAL",
    "realuser2",
    "2020-10-10 01:01:11",
    "picture post",
    "picture caption picture caption picture caption",
    "0headshot.png.jpeg",
    0,
    0,
    0,
    0
);

-- Posts can also be saved like before.
-- Note the modification from DATE to DATETIME.
INSERT INTO SavedPost 
VALUES (
	"realuser1",
    002,
    "2020-10-12 11:11:11"
);

-- Posts can also be voted on like before.
INSERT INTO PostVote
VALUES (
	"realuser1",
    002,
    1
);
UPDATE Post SET upvote_count = upvote_count + 1 WHERE post_id = 002;

-- Users can now follow other users.
-- Technically, users can follow themselves right now. The backend should probably catch this, though?
-- TO INSERT AN ENTITY THAT REPRESENTS AN ACCOUNT-FOLLOW RELATIONSHIP:
-- 		INSERT INTO FollowUser
-- 		VALUES (
-- 			user_follower: a string representing the user who is FOLLOWING someone
-- 			user_followed: a string representing the user who is FOLLOWED by someone
-- 		);
-- Note that a FollowUser pair of ("username1", "username2") will be different than a pair of ("username2", "username1")
-- If realuser1 wants to follow realuser2, this would be represented by:
INSERT INTO FollowUser
VALUES (
	"realuser1",                -- user_follower
    "realuser2"                 -- user_followed
);

-- Users can also follow topics.
-- TO INSERT AN ENTITY THAT REPRESENTS AN TOPIC-FOLLOW RELATIONSHIP:
-- 		INSERT INTO FollowTopic
-- 		VALUES (
-- 			user_follower: a string representing the user who is FOLLOWING the topic
-- 			topic_followed: a string representing the topic that is FOLLOWED by the user
-- 		);
-- If realuser1 wants to follow the GENERAL topic, this would be represented by:
INSERT INTO FollowTopic
VALUES (
	"realuser1",                -- user_follower
    "GENERAL"                   -- topic_followed
);

-- Comments will also be implemented this sprint.
-- TO INSERT AN ENTITY THAT REPRESENTS A COMMENT:
-- 		INSERT INTO PostComment
-- 		VALUES (
-- 			comment_id: a unique integer ID assigned to the comment upon creation
-- 			post_parent: an integer corresponding to the post_id that the comment is attached to
-- 			user_parent: a string corresponding to the username of the comment's author
-- 			comment_parent: an integer corresponding to the comment_id that the comment is a reply to; set this to 0 if the comment is not a reply
-- 			date_created: a date and time that the first post in the topic was made IN THE FORMAT 'YYYY-MM-DD HH:MI:SS'
-- 			content: a string representing the text in the comment; 400 characters is the maximum
-- 			upvote_count: an integer representing the comment's total upvotes; initialize this as 0
-- 			downvote_count: an integer representing the comment's total downvotes; initialize this as 0
-- 			moderation_status: an integer that flags the mod status of the comment; always set this to 0 for now
-- 		);
-- If realuser1 posts a comment on post 002, this would be represented by:
INSERT INTO PostComment
VALUES (
	001,                                  -- comment_id
    002,                                  -- post_parent
    "realuser1",                          -- user_parent
    000,                                  -- comment_parent
    "2020-10-12 11:45:02",                -- date_created
    "Wow, that is a cool picture!",       -- content
    0,                                    -- upvote_count
    0,                                    -- downvote_count
    0                                     -- moderation_status
);

-- Comments can also be voted on.
-- Similiar UPDATE statements need to be made as in post voting.
-- TO INSERT AN ENTITY THAT REPRESENTS A COMMENT VOTE:
-- 		INSERT INTO CommentVote
-- 		VALUES (
-- 			username: a string corresponding to the user who voted on the comment
-- 			comment_id: an integer corresponding to the id of the comment that was voted on
-- 			score: an integer that represents the score; 1 for upvote and -1 for downvote
-- 		);
-- If realuser2 wants to vote on the comment with an ID of 1, this would be represented by:
INSERT INTO CommentVote
VALUES (
	"realuser1",
    001,
    1
);

-- Additionally, like post voting, the comment table will need to be updated as well:
UPDATE PostComment SET upvote_count = upvote_count + 1 WHERE comment_id = 1;
