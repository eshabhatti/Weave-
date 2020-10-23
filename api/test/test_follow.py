# # # # # # # # # # # # # # # # # # # 
# # # # # FOLLOW CURL TESTS # # # # # 
# # # # # # # # # # # # # # # # # # # 
import re
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
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Follow User Timeline Modifications
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor.execute("SELECT post_id FROM Post WHERE creator = \"followtest_2\" AND anon_flag = 0")
    valid_posts = [str(valid_post_1), str(valid_post_2)]
    for row in cursor:
        valid_posts.append(str(row[0]))

    follow_command = open('follow_test.cmd', 'w+')
    follow_command.seek(0)
    follow_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"start\\":0,\\"end\\":5}" http://localhost:5000/timeline > test_output.txt""")
    follow_command.truncate()
    follow_command.close()

    subprocess.call([r'follow_test.cmd'])
    test_output = open("test_output.txt", "r")
    
    displayed_posts = []
    line = test_output.readline()
    follow_search = False
    while line:
        if line and follow_search == False and re.search("\[", line) != None:
            follow_search = True
        if line and follow_search == True and re.search("[0-9]+", line) != None:
            displayed_posts.append(line.strip("\n\t ,"))
        line = test_output.readline()

    follow_test2 = "FAILED: Proper posts display properly on the timeline after following a user."
    valid_posts.sort()
    displayed_posts.sort()
    # print("Valid = " + str(valid_posts))
    # print("Displayed = " + str(displayed_posts))
    if (valid_posts == displayed_posts):
        follow_test2 = "PASSED: Proper posts display properly on the timeline after following a user."
    test_output.close()
    follow_tests.append(follow_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    return follow_tests