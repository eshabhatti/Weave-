-- Unlike the script made for the last sprint, this script will only show how to insert new types of data.
-- Since there have been no modifications to posts or comments, these entity types will not be discussed here.
-- Note that 'createtables.sql' must be run for any data to be allowed into the database.

-- At this point in time, it is assumed that most know the general format of the INSERT statement.
-- It is also assumed that you know the general format of inserting data from sprint one and sprint two.
-- If this is not the case, see "scripts/sprintone_datainsertion.sql" and "scripts/sprinttwo_datainsertion.sql".

-- To properly insert sprint three data into the database, we need to have two users.
-- Note that these user entities have passwords shown as the first part of the email address.
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

-- From here, we can examine the direct messages and blocking relationships.

-- FOR DIRECT MESSAGES:
-- Note that each direct message needs to have a valid (existing) recipient and a valid (existing) sender.
-- During entity creation, both sender_status and receiver_status should be set to 1.
-- TO INSERT AN ENTITY THAT REPRESENTS A DIRECT MESSAGE:
-- 		INSERT INTO DirectMessage
-- 		VALUES (
-- 			message_id: a unique integer ID that is assigned to the message upon creation
-- 			sender: a string representing the user who has sent the message
-- 			receiver: a string representing the user who should receive the message
-- 			sender_status: an integer flag that will be 0 if the message was deleted by the sender
-- 			receiever_status: an integer flag that will be 0 if the message was deleted by the receiver
-- 			content: a string holding the content of the message
-- 			date_created: the date and time when the message was created IN THE FORMAT 'YYYY-MM-DD HH:MI:SS'
-- 		);
-- If realuser1 wants to send realuser2 a message, the entity might look like this:
INSERT INTO DirectMessage
VALUES (
    001,
    "realuser1",
    "realuser2",
    1,
    1,
    "Hello, how are you?",
    "2020-11-12 04:05:06"
);

-- FOR BLOCKING RELATIONSHIPS:
-- Technically, users can block themselves right now. The backend should probably catch this, though.
-- TO INSERT AN ENTITY THAT REPRESENTS A BLOCKING RELATIONSHIP:
-- 		INSERT INTO UserBlock
-- 		VALUES (
-- 			user_blocker: a string representing the user WHO IS DOING THE BLOCKING
-- 			user_blocked: a string representing the user WHO IS BEING BLOCKED
-- 		);
-- If realuser2 wants to block realuser1, the entity might look like this:
INSERT INTO UserBlock
VALUES (
    "realuser2",
    "realuser1"
);
