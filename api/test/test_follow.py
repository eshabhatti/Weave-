# # # # # # # # # # # # # # # # # # # 
# # # # # FOLLOW CURL TESTS # # # # # 
# # # # # # # # # # # # # # # # # # # 
import subprocess
import mysql.connector

# Initializes the database instance.
mysql_cred = open("../credentials/dbcredentials.txt", "r")
db = mysql.connector.connect(
	host="localhost", 
	user=mysql_cred.readline().strip("\n\r "), 
	password=mysql_cred.readline().strip("\n\r "),
    database="weave"
)
mysql_cred.close()


# Runs test cases.
def follow_test(access_token, valid_post_1, valid_post_2):

    cursor = db.cursor()
    follow_tests = []

    # Adds information to the database needed to run all further tests. (NOT A TEST CASE)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    data_file = open("../../db/tests/timelinetest.sql", "r")
    data_insert = data_file.read()
    data_file.close()
    data_commands = data_insert.split(";")
    for query in data_commands:
	    cursor.execute(query)
    db.commit()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Follow User Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    follow_command = open('follow_test.cmd', 'w+')
    follow_command.seek(0)
    follow_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"following\\":\\"followtest_2\\",\\"type\\":1}" http://localhost:5000/followuser > test_output.txt""")
    follow_command.truncate()
    follow_command.close()

    subprocess.call([r'follow_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_follow = True
    while line:
        if failed_follow and line and line.find('follow user done') != -1:
            follow_test1 = "FAILED: Users can follow other users."
            cursor.execute("SELECT user_followed FROM FollowUser WHERE user_follower = \"testname\" LIMIT 0, 1;")
            for row in cursor:
                follow_test1 = "PASSED: User can follow other users."
                failed_follow = False
            break
        line = test_output.readline()
    if failed_follow:
        follow_test1 = "FAILED: Users can follow other users."
    test_output.close()
    follow_tests.append(follow_test1)

    return follow_tests