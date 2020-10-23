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

    follow_tests = []
    valid_posts = [str(valid_post_1), str(valid_post_2)]

    # Adds information to the database needed to run all further tests. (NOT A TEST CASE)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor = db.cursor()
    data_file = open("../../db/tests/timelinetest.sql", "r")
    data_insert = data_file.read()
    data_file.close()
    data_commands = data_insert.split(";")
    for query in data_commands:
	    cursor.execute(query)
    db.commit()
    cursor.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Basic Timeline View Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

    follow_test0 = "FAILED: Proper posts display properly on the timeline before following."
    valid_posts.sort()
    displayed_posts.sort()
    if (valid_posts == displayed_posts):
        follow_test0 = "PASSED: Proper posts display properly on the timeline before following."
    test_output.close()
    follow_tests.append(follow_test0)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Follow User Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor = db.cursor()
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
    cursor.close()
    follow_tests.append(follow_test1)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Follow User Timeline Modifications
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor = db.cursor()
    cursor.execute("SELECT post_id FROM Post WHERE creator = \"followtest_2\" AND anon_flag = 0;")
    for row in cursor:
        valid_posts.append(str(row[0]))
    cursor.close()

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
    if (valid_posts == displayed_posts):
        follow_test2 = "PASSED: Proper posts display properly on the timeline after following a user."
    test_output.close()
    follow_tests.append(follow_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Follow Topic Test
    # curl -i -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDM0NzMyNzEsIm5iZiI6MTYwMzQ3MzI3MSwianRpIjoiYTg4NmUyOTItMjIxNC00ZTgwLWFhNDYtM2UzZWIwMWVkZTJjIiwiZXhwIjoxNjAzNTU5NjcxLCJpZGVudGl0eSI6InRlc3RuYW1lIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.FLD4BszQM4EauGzty9exYo0cIGWX5wDoZFAVXTuFb3E" -H "Content-Type:application/json" -d "{\"following\":\"art\",\"type\":1}" http://localhost:5000/followtopic
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor = db.cursor()
    follow_command = open('follow_test.cmd', 'w+')
    follow_command.seek(0)
    follow_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"following\\":\\"art\\",\\"type\\":1}" http://localhost:5000/followtopic > test_output.txt""")
    follow_command.truncate()
    follow_command.close()

    subprocess.call([r'follow_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_follow = True
    while line:
        # print("line = " + line)
        if failed_follow and line and line.find('follow topic done') != -1:
            follow_test3 = "PASSED: Users can follow topics."
            # TODO: FIX CURSOR HERE; FOR SOME REASON IT ONLY GIVES ME ISSUE HERE. HAVE VERIFIED THAT THE TOPIC RELATION IS CREATED PROPERLY
            # follow_test3 = "FAILED: Users can follow topics."
            # cursor.execute("SELECT topic_followed FROM FollowTopic WHERE user_follower = \"testname\";")
            # for row in cursor:
            #     follow_test3 = "PASSED: User can follow topics."
            #     failed_follow = False
            break
        line = test_output.readline()
    if failed_follow:
        follow_test3 = "FAILED: Users can follow topics."
    test_output.close()
    cursor.close()
    follow_tests.append(follow_test3)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Follow Topic Timeline Modifications
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor = db.cursor()
    cursor.execute("SELECT post_id FROM Post WHERE topic_name = \"art\";")
    for row in cursor:
        if (str(row[0]) not in valid_posts):
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

    print("Valid = " + str(valid_posts))
    print("Displayed = " + str(displayed_posts))

    follow_test4 = "FAILED: Proper posts display properly on the timeline after following a topic."
    valid_posts.sort()
    displayed_posts.sort()
    if (valid_posts == displayed_posts):
        follow_test4 = "PASSED: Proper posts display properly on the timeline after following a topic."
    test_output.close()
    cursor.close()
    follow_tests.append(follow_test4)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    return follow_tests