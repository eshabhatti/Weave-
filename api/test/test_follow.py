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
def follow_test(access_token, valid_post):

    cursor = db.cursor()
    follow_tests = []

    # Adds information to the database needed to run all further tests.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    follow_command = open('follow_test.cmd', 'w+')
    follow_command.seek(0)
    follow_command.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"followtest1\\",\\"password\\":\\"Gudpasswurd22\\",\\"email\\":\\"follower1@test.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    follow_command.truncate()
    follow_command.close()
    subprocess.call([r'follow_command.cmd'])
    test_output = open("test_output.txt", "r")
    line = test_output.readline()
    while line:
        if line and line.find('token') != -1:
            access_token_1 = line[line.find('token') + 9:len(line) - 4]
            break
        line = test_output.readline()
    test_output.close()

    follow_command = open('follow_test.cmd', 'w+')
    follow_command.seek(0)
    follow_command.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"followtest2\\",\\"password\\":\\"Gudpasswurd22\\",\\"email\\":\\"follower2@test.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    follow_command.truncate()
    follow_command.close()
    subprocess.call([r'follow_command.cmd'])
    test_output = open("test_output.txt", "r")
    line = test_output.readline()
    while line:
        if line and line.find('token') != -1:
            access_token_2 = line[line.find('token') + 9:len(line) - 4]
            break
        line = test_output.readline()
    test_output.close()


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
