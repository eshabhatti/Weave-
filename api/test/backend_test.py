import subprocess
import sys
import mysql.connector

from test_registration import registration_test
from test_login import login_test
from test_profile import profile_test
from test_post import post_test
from test_anon import anon_test
from test_follow import follow_test
from test_postvote import post_vote_test
from test_comment import comment_test
from test_commentvote import comment_vote_test

# Tests (only) backend functionality with curl commands.
# Before running this script, start the Flask server for Weave.
# This script has a dependency of mysql-connector-python==8.0.22: run 'pip install mysql-connector-python' to install.
# IF THE TEST SUITE HANGS ON STARTUP, TRY RESTARTING YOUR LOCAL MYSQL SERVER.




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

post_tests = post_test(access_token)                       # Post and topic tests.
access_token = post_tests[len(post_tests) - 1]             # Access token needs to update for later tests.
vp_1 = post_tests[len(post_tests) - 2]                     # Pulls first valid post's ID (001).
vp_2 = post_tests[len(post_tests) - 3]                     # Pulls first valid post's ID (002).

anon_tests = anon_test(access_token)                       # Anonymous post tests.
access_token = anon_tests[len(anon_tests) - 1]             # Access token needs to update for later tests.

postvote_tests = post_vote_test(access_token)              # Post vote tests.

follow_tests = follow_test(access_token, vp_1, vp_2)       # Following and timeline tests.

comment_tests = comment_test(access_token)                 # Comment tests.
access_token = comment_tests[len(comment_tests) - 1]       # Access token needs to update for later tests.
vc_1 = comment_tests[len(comment_tests) - 2]               # Pulls the valid comment ID (001).

commentvote_tests = comment_vote_test(access_token)        # Comment vote tests.






# PRINTS TEST OUTPUT
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

print(" ")
print("Post Voting Tests")
for row in range(len(postvote_tests)):
	print(postvote_tests[row])

print(" ")
print("Timeline and Following Tests")
for row in range(len(follow_tests)):
	print(follow_tests[row])

print (" ")
print("Comment Tests")
for row in range(len(comment_tests) - 2):
	print(comment_tests[row])

print (" ")
print("Comment Vote Tests")
for row in range(len(commentvote_tests)):
	print(commentvote_tests[row])
