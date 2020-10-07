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
		reg_test1 = "PASSED: Register new user (new valid user created)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test1 = "FAILED: Register new user (make sure app and database are running and that database is reset)"
test_output.close()

#attempt to register existing user
subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('This username has already been used.') != -1:
		reg_test2 = "PASSED: Fail to register existing user (failed attempt to register existing user)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test2 = "FAILED: Fail to register existing user (failed attempt to register existing user)"
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
		reg_test3 = "PASSED: Fail to register user with blank inputs (failed attempt to register user with blank inputs)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test3 = "FAILED: Fail to register user with blank inputs (failed attempt to register user with blank inputs)"
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
		reg_test4 = "PASSED: Fail to register user with too short of inputs (inputs less than 6 chars)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test4 = "FAILED: Fail to register user with too short of inputs (inputs less than 6 chars)"
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
		reg_test5 = "PASSED: Fail to register user with too large of inputs (inputs greater than 42 characters)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test5 = "FAILED: Fail to register user with too large of inputs (inputs greater than 42 characters)"
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
		login_test1 = "PASSED: Login valid user"
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test1 = "FAILED: Login valid user"
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
		login_test2 = "PASSED: Fail to login user with empty inputs"
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test2 = "FAILED: Fail to login user with empty inputs"
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
		login_test3 = "PASSED: Fail to login nonexistent user"
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test3 = "FAILED: Fail to login nonexistent user"
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
failed_profile1 = True
while line:
	if failed_profile1 and line and line.find('token') != -1:
		profile_test1 = "PASSED: Valid profile change (profile names changed)"
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_profile1 = False
		break
	line = test_output.readline()
if failed_profile1:
	profile_test1 = "FAILED: Valid profile change (profile names changed)"
test_output.close()

#edit profile blank inputs test


#revert profile test file
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

	print(line)

	if failed_post and line and line.find('token') != -1:
		post_test = "PASSED: Post Test"
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_post = False
		#break
	line = test_output.readline()
if failed_login:
	login_test = "FAILED: Post Test"
test_output.close()


# vote curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/

new_post_test = open('vote_test.cmd', 'r+')
new_post_test.seek(0)
new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\":\\"testname\\",\\"type\\":\\"1\\",\\"id\\":\\"1\\",\\"vote\\":\\"1\\"}" http://localhost:5000/vote/ > test_output.txt""")
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

print(reg_test1)
print(reg_test2)
print(reg_test3)
print(reg_test4)
print(reg_test5)

print(login_test1)
print(login_test2)
print(login_test3)

print(profile_test1)
print(post_test)
print(vote_test)
