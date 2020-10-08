import subprocess

#Tests backend functionality with curl commands


# register curl tests
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
new_register_test = open('registration_test.cmd', 'r+')
new_register_test.seek(0)
new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"password\\":\\"Gudpasswurd22\\",\\"email\\":\\"test@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
new_register_test.truncate()
new_register_test.close()

subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('access_token') != -1:
		reg_test1 = "PASSED: Checking that an account is created in the database"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test1 = "FAILED: Checking that an account is created in the database"
test_output.close()

#attempt to register existing user
subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('This username has already been used.') != -1:
		reg_test2 = "PASSED: Checking that duplicate accounts cannot be created"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test2 = "FAILED: Checking that duplicate accounts cannot be created"
test_output.close()

#attempt to register blank user and password
new_register_test = open('registration_test.cmd', 'r+')
new_register_test.seek(0)
new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"\\",\\"password\\":\\"\\",\\"email\\":\\"\\"}" http://localhost:5000/register/ > test_output.txt""")
new_register_test.truncate()
new_register_test.close()

subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('Your username is invalid.') != -1:
		reg_test3 = "PASSED: Checking that empty inputs can't be accepted"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test3 = "FAILED: Checking that empty inputs can't be accepted"
test_output.close()

#attempt to register user with user and pass that are too small (<6 chars)
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"test\",\"password\":\"Gudp\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
new_register_test = open('registration_test.cmd', 'r+')
new_register_test.seek(0)
new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"test\\",\\"password\\":\\"Gudp\\",\\"email\\":\\"test@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
new_register_test.truncate()
new_register_test.close()

subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('Your username is invalid.') != -1:
		reg_test4 = "PASSED: Checking that inputs with incorrect format can't be accepted. (inputs less than 6 chars)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test4 = "FAILED: Checking that inputs with incorrect format can't be accepted. (inputs less than 6 chars)"
test_output.close()

#attempt to register user with user and pass that are too large (>42 chars)
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testtesttetesttesttetesttesttetesttesttetesttesttetesttestte\",\"password\":\"testtesttetesttesttetesttesttetesttesttetesttestte\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
new_register_test = open('registration_test.cmd', 'r+')
new_register_test.seek(0)
new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testtesttetesttesttetesttesttetesttesttetesttesttetesttestte\\",\\"password\\":\\"testtesttetesttesttetesttesttetesttesttetesttestte\\",\\"email\\":\\"test@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
new_register_test.truncate()
new_register_test.close()

subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('Your username is invalid.') != -1:
		reg_test5 = "PASSED: Checking that inputs with incorrect format can't be accepted. (inputs greater than 42 characters)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test5 = "FAILED: Checking that inputs with incorrect format can't be accepted. (inputs greater than 42 characters)"
test_output.close()




# login curl test
# curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\"}" http://localhost:5000/login/
new_login_test = open('login_test.cmd', 'r+')
new_login_test.seek(0)
new_login_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"password\\":\\"Gudpasswurd22\\"}" http://localhost:5000/login/ > test_output.txt""")
new_login_test.truncate()
new_login_test.close()

subprocess.call([r'login_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_login = True
while line:
	if failed_login and line and line.find('access_token') != -1:
		login_test1 = "PASSED: Checking a valid username and password."
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test1 = "FAILED: Checking a valid username and password."
test_output.close()

#login test for empty inputs
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"\",\"password\":\"\"}" http://localhost:5000/login/
new_login_test = open('login_test.cmd', 'r+')
new_login_test.seek(0)
new_login_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"\\",\\"password\\":\\"\\"}" http://localhost:5000/login/ > test_output.txt""")
new_login_test.truncate()
new_login_test.close()

subprocess.call([r'login_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_login = True
while line:
	if failed_login and line and line.find('Username and password do not match.') != -1:
		login_test2 = "PASSED: Checking empty input boxes."
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test2 = "FAILED: Checking empty input boxes."
test_output.close()

#login test for user not in database
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testtest\",\"password\":\"testtest\"}" http://localhost:5000/login/
new_login_test = open('login_test.cmd', 'r+')
new_login_test.seek(0)
new_login_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testtest\\",\\"password\\":\\"testtest\\"}" http://localhost:5000/login/ > test_output.txt""")
new_login_test.truncate()
new_login_test.close()

subprocess.call([r'login_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_login = True
while line:
	if failed_login and line and line.find('Username and password do not match.') != -1:
		login_test3 = "PASSED: Checking an invalid username and password."
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test3 = "FAILED: Checking an invalid username and password."
test_output.close()



# edit profile curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"newusername\":\"newtestname\",\"firstname\":\"Bob\",\"lastname\":\"Banana\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"newtestname\",\"newusername\":\"testname\",\"firstname\":\"Banana\",\"lastname\":\"Bob\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/

#user has updated account
#(error): Your new username has already been taken
#Missing Authorization Header

#edit profile test
new_profile_test = open('profile_test.cmd', 'r+')
new_profile_test.seek(0)
new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"newusername\\":\\"newtestname\\",\\"firstname\\":\\"Bob\\",\\"lastname\\":\\"Banana\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
#new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"newtestname\\",\\"newusername\\":\\"testname\\",\\"firstname\\":\\"Banana\\",\\"lastname\\":\\"Bob\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.truncate()
new_profile_test.close()

subprocess.call([r'profile_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_profile = True
while line:
	if failed_profile and line and line.find('token') != -1:
		profile_test1 = "PASSED: Check that a normal case updates the database."
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_profile = False
		break
	line = test_output.readline()
if failed_profile:
	profile_test1 = "FAILED: Check that a normal case updates the database."
test_output.close()

#revert profile test file NOT A TEST CASE
new_profile_test = open('profile_test.cmd', 'r+')
new_profile_test.seek(0)
#new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"newusername\\":\\"newtestname\\",\\"firstname\\":\\"Bob\\",\\"lastname\\":\\"Banana\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"newtestname\\",\\"newusername\\":\\"testname\\",\\"firstname\\":\\"Banana\\",\\"lastname\\":\\"Bob\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.truncate()
new_profile_test.close()

subprocess.call([r'profile_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
while line:
	if line and line.find('token') != -1:
		access_token = line[line.find('token') + 9:len(line) - 4]
		break
	line = test_output.readline()
test_output.close()

#edit profile blank inputs test doesnt work
new_profile_test = open('profile_test.cmd', 'r+')
new_profile_test.seek(0)
new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"newusername\\":\\"\\",\\"firstname\\":\\"\\",\\"lastname\\":\\"\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.truncate()
new_profile_test.close()

subprocess.call([r'profile_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_profile = True
while line:
		
	if failed_profile and line and line.find('token') != -1:
		profile_test2 = "PASSED: Check that blank inputs are not accepted."
		failed_profile = False
		break
	line = test_output.readline()
if failed_profile:
	profile_test2 = "FAILED: Check that blank inputs are not accepted."
test_output.close()

#edit profile too many characters test
new_profile_test = open('profile_test.cmd', 'r+')
new_profile_test.seek(0)
new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"newusername\\":\\"testtesttetesttesttetesttesttetesttesttetesttestte\\",\\"firstname\\":\\"Bob\\",\\"lastname\\":\\"Banana\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.truncate()
new_profile_test.close()

subprocess.call([r'profile_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_profile = True
while line:

	if failed_profile and line and line.find('Your new username is invalid.') != -1:
		profile_test3 = "PASSED: Check that case where too many characters are entered does not update the database. (>250 characters)"
		failed_profile = False
		break
	line = test_output.readline()
if failed_profile:
	profile_test3 = "FAILED: Check that case where too many characters are entered does not update the database. (>250 characters)"
test_output.close()


# post curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"topic\":\"general\",\"type\":\"1\",\"title\":\"TESTPOST\",\"content\":\"hello hello hello hello\",\"anon\":\"0\"}" http://localhost:5000/createpost/

new_post_test = open('post_test.cmd', 'r+')
new_post_test.seek(0)
new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"hello hello hello hello\\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
new_post_test.truncate()
new_post_test.close()

subprocess.call([r'post_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_post = True
while line:
	if failed_post and line and line.find('token') != -1:
		post_test1 = "PASSED: Check that a valid post should always be posted."
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_post = False
		break
	line = test_output.readline()
if failed_login:
	post_test1 = "FAILED: Check that a valid post should always be posted."
test_output.close()

#post blank post test doesnt work
new_post_test = open('post_test.cmd', 'r+')
new_post_test.seek(0)
new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"\\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
new_post_test.truncate()
new_post_test.close()

subprocess.call([r'post_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_post = True
while line:
	if failed_post and line and line.find('token') != -1:
		post_test2 = "PASSED: Check that blank posts can't be posted."
		failed_post = False
		break
	line = test_output.readline()
if failed_login:
	post_test2 = "FAILED: Check that blank posts can't be posted."
test_output.close()

#post test: fail to post that is too long >750 chars
new_post_test = open('post_test.cmd', 'r+')
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



#anon post Tests

#anon retain original username (returns token)
new_post_test = open('post_test.cmd', 'r+')
new_post_test.seek(0)
new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"hello hello hello hello\\",\\"anon\\":\\"1\\"}" http://localhost:5000/createpost/ > test_output.txt""")
new_post_test.truncate()
new_post_test.close()

subprocess.call([r'post_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_post = True
while line:
	if failed_post and line and line.find('token') != -1:
		post_test4 = "PASSED: Anonymous posts still retain the original user's username, but do not show it when displaying."
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_post = False
		break
	line = test_output.readline()
if failed_post:
	post_test4 = "FAILED: Anonymous posts still retain the original user's username, but do not show it when displaying."
test_output.close()

#blank anon post test
new_post_test = open('post_test.cmd', 'r+')
new_post_test.seek(0)
new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"\\",\\"anon\\":\\"1\\"}" http://localhost:5000/createpost/ > test_output.txt""")
new_post_test.truncate()
new_post_test.close()

subprocess.call([r'post_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_post = True
while line:
	if failed_post and line and line.find('token') != -1:
		post_test5 = "PASSED: Anonymous posts should not be empty."
		failed_post = False
		break
	line = test_output.readline()
if failed_post:
	post_test5 = "FAILED: Anonymous posts should not be empty."
test_output.close()

#format anon post requirement
new_post_test = open('post_test.cmd', 'r+')
new_post_test.seek(0)
new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test test \\",\\"anon\\":\\"1\\"}" http://localhost:5000/createpost/ > test_output.txt""")
new_post_test.truncate()
new_post_test.close()

subprocess.call([r'post_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_post = True
while line:
	if failed_post and line and line.find('error') != -1:
		post_test6 = "PASSED: Anonymous posts should not break any formally-established format requirements."
		failed_post = False
		break
	line = test_output.readline()
if failed_post:
	post_test6 = "FAILED: Anonymous posts should not break any formally-established format requirements."
test_output.close()




# vote curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/

#new_post_test = open('vote_test.cmd', 'r+')
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
print(" ")
print("Registration Tests")
print(reg_test1)
print(reg_test2)
print(reg_test3)
print(reg_test4)
print(reg_test5)

print(" ")
print("Login Tests")
print(login_test1)
print(login_test2)
print(login_test3)

print(" ")
print("Profile Changing Tests")
print(profile_test1)
print(profile_test2)
print(profile_test3)

print(" ")
print("Posting Tests")
print(post_test1)
print(post_test2)
print(post_test3)

print(" ")
print("Anonymous Posting Tests")
print(post_test4)
print(post_test5)
print(post_test6)

#print(vote_test)
