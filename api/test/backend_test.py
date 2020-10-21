import subprocess
from test_registration import registration_test
from test_login import login_test
from test_profile import profile_test
from test_post import post_test
from test_anon import anon_test

# Tests (only) backend functionality with curl commands.
# Before running this script, start the Flask server for Weave.
# MAY WANT TO FEED THE DATABASE DROPTABLES AND THEN CREATETABLES SO THAT REGISTRATION ALWAYS WORKS.

# See separate files for more information on each test.
reg_test = registration_test()                             # Registration tests.
login_tests = login_test()                                 # Login tests.
access_token = login_tests[len(login_tests) - 1]           # Access token needed for later tests.
pro_tests = profile_test(access_token)                     # Profile tests.
access_token = pro_tests[len(pro_tests) - 1]               # Access token needs to update for later tests.
post_tests = post_test(access_token)                       # Post tests.
access_token = post_tests[len(post_tests) - 1]             # Access token needs to update for later tests.
anon_tests = anon_test(access_token)                       # Anonymous post tests.
access_token = anon_tests[len(anon_tests) - 1]             # Access token needs to update for later tests.

            
# vote curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/

#new_post_test = open('vote_test.cmd', 'w+')
#new_post_test.seek(0)
#new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\":\\"testname\\",\\"type\\":\\"1\\",\\"id\\":\\"1\\",\\"vote\\":\\"1\\"}" http://localhost:5000/vote/ > test_output.txt""")
"""
new_post_test.truncate()
new_post_test.close()

subprocess.call([r'vote_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_vote = True
while line:	
	if failed_vote and line and line.find('token') != -1:
		vote_test = "PASSED: Vote Test"
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_vote = False
		break
	line = test_output.readline()
if failed_vote:
	vote_test = "FAILED: Vote Test"
test_output.close()
"""


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
for row in range(len(post_tests) - 1):
	print(post_tests[row])

print(" ")
print("Anonymous Posting Tests")
for row in range(len(anon_tests) - 1):
	print(anon_tests[row])

#print(vote_test)
