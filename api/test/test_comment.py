# # # # # # # # # # # # # # # # # # # #
# # # # # COMMENT CURL TESTS  # # # # # 
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
def comment_test(access_token):

    cursor = db.cursor()
    comment_tests = []

    # Correct Comment Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    comment_command = open('comment_test.cmd', 'w+')
    comment_command.seek(0)
    comment_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"content\\":\\"wow this is a cool comment\\",\\"post_id\\":\\"1\\"}" http://localhost:5000/createcomment/ > test_output.txt""")
    comment_command.truncate()
    comment_command.close()

    subprocess.call([r'comment_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_comment = True
    valid_comment = "0"
    while line:
        if failed_comment and line and line.find('token') != -1:
            comment_string = "PASSED: Check that a valid comment should always be posted."
            access_token = line[line.find('token') + 9:len(line) - 4]
            failed_comment = False
            valid_comment = "1"
            break
        line = test_output.readline()
    if failed_comment:
        comment_string = "FAILED: Check that a valid comment should always be posted."
    test_output.close()
    comment_tests.append(comment_string)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Empty Comment Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    comment_command = open('comment_test.cmd', 'w+')
    comment_command.seek(0)
    comment_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"content\\":\\"\\",\\"post_id\\":\\"1\\"}" http://localhost:5000/createcomment/ > test_output.txt""")
    comment_command.truncate()
    comment_command.close()

    subprocess.call([r'comment_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_comment = True
    while line:
        if failed_comment and line and line.find('Invalid Comment Body.') != -1:
            comment_string = "PASSED: Check that an empty comment should not be posted."
            failed_comment = False
            break
        line = test_output.readline()
    if failed_comment:
        comment_string = "FAILED: Check that an empty comment should not be posted."
    test_output.close()
    comment_tests.append(comment_string)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Large Comment (> 400) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    comment_command = open('comment_test.cmd', 'w+')
    comment_command.seek(0)
    comment_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"content\\":\\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa\\",\\"post_id\\":\\"1\\"}" http://localhost:5000/createcomment/ > test_output.txt""")
    comment_command.truncate()
    comment_command.close()

    subprocess.call([r'comment_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_comment = True
    while line:
        if failed_comment and line and line.find('Invalid Comment Body.') != -1:
            comment_string = "PASSED: Check that a large comment should not be posted."
            failed_comment = False
            break
        line = test_output.readline()
    if failed_comment:
        comment_string = "FAILED: Check that a large comment should not be posted."
    test_output.close()
    comment_tests.append(comment_string)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    comment_tests.append(valid_comment)
    comment_tests.append(access_token)
    return comment_tests
    