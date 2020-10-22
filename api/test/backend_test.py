import subprocess
import sys
import mysql.connector
from test_registration import registration_test
from test_login import login_test
from test_profile import profile_test
from test_post import post_test
from test_anon import anon_test

# Tests (only) backend functionality with curl commands.
# Before running this script, start the Flask server for Weave.
# This script has a dependency of mysql-connector-python==8.0.22: run 'pip install mysql-connector-python' to install.

# Since the database can actually be damaged now, here is a confirm statement. 
confirm_test = input("THESE TESTS WILL ERASE THE CURRENT LOCAL WEAVE DATABASE.\nIS THIS OK? ENTER 'Y' TO PROCEED.\n")
if (confirm_test != "Y" and confirm_test != "y"):
	print("TESTS ABORTED")
	sys.exit()

# Initializes the cursor for database setup.
mysql_cred = open("../credentials/dbcredentials.txt", "r")
db_init = mysql.connector.connect(
	host="localhost", 
	user=mysql_cred.readline().strip("\n\r "), 
	password=mysql_cred.readline().strip("\n\r ")
)
mysql_cred.close()
init_cursor = db_init.cursor()

# DELETES THE WEAVE DATABASE
drop_file = open("../../db/tests/droptesttables.sql", "r")
droptables = drop_file.read()
drop_file.close()
drop_commands = droptables.split(";")
for query in drop_commands:
	init_cursor.execute(query)

# RE-CREATES THE WEAVE DATABASE
create_file = open("../../db/tests/createtesttables.sql", "r")
createtables = create_file.read()
create_file.close()
create_commands = createtables.split(";")
for query in create_commands:
	init_cursor.execute(query)
init_cursor.close()

# RUNS THE BACKEND TESTS
# See separate files for more information on each test.

reg_test = registration_test()                             # Registration tests.

login_tests = login_test()                                 # Login tests.
access_token = login_tests[len(login_tests) - 1]           # Access token needed for later tests.

pro_tests = profile_test(access_token)                     # Profile tests.
access_token = pro_tests[len(pro_tests) - 1]               # Access token needs to update for later tests.

post_tests = post_test(access_token)                       # Post tests.
access_token = post_tests[len(post_tests) - 1]             # Access token needs to update for later tests.
valid_post1 = post_tests[len(post_tests) - 2]              # Pulls first valid post's ID from the database.
valid_post2 = post_tests[len(post_tests) - 3]              # Pulls first valid post's ID from the database.

anon_tests = anon_test(access_token)                       # Anonymous post tests.
access_token = anon_tests[len(anon_tests) - 1]             # Access token needs to update for later tests.

            
# vote curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/

#new_post_test = open('vote_test.cmd', 'w+')
#new_post_test.seek(0)
#new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\":\\"testname\\",\\"type\\":\\"1\\",\\"id\\":\\"1\\",\\"vote\\":\\"1\\"}" http://localhost:5000/vote/ > test_output.txt""")
# new_post_test.truncate()
# new_post_test.close()

# subprocess.call([r'vote_test.cmd'])
# test_output = open("test_output.txt", "r")

# line = test_output.readline()
# failed_vote = True
# while line:	
# 	if failed_vote and line and line.find('token') != -1:
# 		vote_test = "PASSED: Vote Test"
# 		access_token = line[line.find('token') + 9:len(line) - 4]
# 		failed_vote = False
# 		break
# 	line = test_output.readline()
# if failed_vote:
# 	vote_test = "FAILED: Vote Test"
# test_output.close()


# Prints test output
print(" ")
print("Registration Tests")
for row in range(len(reg_test)):
	print(reg_test[row])

print(" ")
print("Login Tests")
for row in range(len(login_tests) - 1):
	print(login_tests[row])

print(" ")
print("Profile Changing Tests")
for row in range(len(pro_tests) - 1):
	print(pro_tests[row])

print(" ")
print("Posting Tests")
for row in range(len(post_tests) - 3):
	print(post_tests[row])

print(" ")
print("Anonymous Posting Tests")
for row in range(len(anon_tests) - 1):
	print(anon_tests[row])

#print(vote_test)
