# # # # # # # # # # # # # # # # # # # #
# # # # # # POST CURL TESTS # # # # # #
# # # # # # # # # # # # # # # # # # # #
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
def post_test(access_token):

    cursor = db.cursor()
    post_tests = []

    # Correct Post Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"hello hello hello hello\\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'post_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_post = True
    valid_post1 = ""
    while line:
        if failed_post and line and line.find('token') != -1:
            post_test1 = "PASSED: Check that a valid text post should always be posted."
            access_token = line[line.find('token') + 9:len(line) - 4]
            failed_post = False
            cursor.execute("SELECT post_id FROM Post ORDER BY post_id DESC LIMIT 0, 1;")
            valid_post1 = cursor.fetchall()[0][0]
            break
        line = test_output.readline()
    if failed_post:
        post_test1 = "FAILED: Check that a valid text post should always be posted."
    test_output.close()
    post_tests.append(post_test1)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Topic Creation Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    cursor.execute("SELECT * FROM Topic WHERE topic_name = \"general\";")
    post_test4 = "FAILED: Check that a valid text post creates a topic when created."
    for row in cursor:
        post_test4 = "PASSED: Check that a valid text post creates a topic when created."
    post_tests.append(post_test4)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Blank Topic Post Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"hello hello hello hello\\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'post_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_post = True
    valid_post2 = ""
    while line:
        if failed_post and line and line.find('token') != -1:
            post_test5 = "PASSED: Check that a text post without a topic should be created in general."
            access_token = line[line.find('token') + 9:len(line) - 4]
            failed_post = False
            cursor.execute("SELECT post_id FROM Post ORDER BY post_id DESC LIMIT 0, 1;")
            valid_post2 = cursor.fetchall()[0][0]
            break
        line = test_output.readline()
    if failed_post:
        post_test5 = "FAILED: Check that a text post without a topic should be created in general."
    test_output.close()
    post_tests.append(post_test5)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Blank Post Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"\\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'post_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_post = True
    while line:
        if failed_post and line and line.find('error') != -1:
            post_test2 = "PASSED: Check that blank posts can't be posted."
            failed_post = False
            break
        line = test_output.readline()
    if failed_post:
        post_test2 = "FAILED: Check that blank posts can't be posted."
    test_output.close()
    post_tests.append(post_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Invalid Post Length Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test \\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'post_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_post = True
    while line:
        if failed_post and line and line.find('error') != -1:
            post_test3 = "PASSED: Check that posts can't exceed 750 characters."
            failed_post = False
            break
        line = test_output.readline()
    if failed_post:
        post_test3 = "FAILED: Check that posts can't exceed 750 characters."
    test_output.close()
    post_tests.append(post_test3)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    post_tests.append(valid_post2)
    post_tests.append(valid_post1)
    post_tests.append(access_token)
    return post_tests