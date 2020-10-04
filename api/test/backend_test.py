import subprocess

#Tests backend functionality with curl commands


# register curl test
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/

subprocess.call([r'registration_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_reg = True
while line:
	if failed_reg and line and line.find('access_token') != -1:
		reg_test = "PASSED: Registration Test (new user created)"
		failed_reg = False
		break
	if failed_reg and line and line.find('This username has already been used.') != -1:
		reg_test = "PASSED: Registration Test (attempt to register existing user)"
		failed_reg = False
		break
	line = test_output.readline()
if failed_reg:
	reg_test = "FAILED: Registration Test (make sure app and database are running)"
test_output.close()


# login curl test
#curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\"}" http://localhost:5000/login/

subprocess.call([r'login_test.cmd'])
test_output = open("test_output.txt", "r")


line = test_output.readline()
failed_login = True
while line:
	if failed_login and line and line.find('access_token') != -1:
		login_test = "PASSED: Login Test"
		access_token = line[line.find('token') + 9:len(line) - 4]
		failed_login = False
		break
	line = test_output.readline()
if failed_login:
	login_test = "FAILED: Login Test"
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
	if failed_profile1 and line and (line.find('user has updated account') != -1 or line.find('username') != -1):
		profile_test1 = "PASSED: Edit Profile Test (profile names changed)"
		failed_profile1 = False
		break
	if failed_profile1 and line and line.find('Your new username has already been taken') != -1:
		profile_test1 = "PASSED: Edit Profile Test (profile name already taken)"
		failed_profile1 = False
		break
	line = test_output.readline()
if failed_profile1:
	profile_test1 = "FAILED: Edit Profile Test"
test_output.close()

#revert profile test
new_profile_test = open('profile_test.cmd', 'r+')
new_profile_test.seek(0)
#new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"newusername\\":\\"newtestname\\",\\"firstname\\":\\"Bob\\",\\"lastname\\":\\"Banana\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"newtestname\\",\\"newusername\\":\\"testname\\",\\"firstname\\":\\"Banana\\",\\"lastname\\":\\"Bob\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
new_profile_test.truncate()
new_profile_test.close()

subprocess.call([r'profile_test.cmd'])
test_output = open("test_output.txt", "r")

line = test_output.readline()
failed_profile2 = True
while line:
	if failed_profile2 and line and (line.find('user has updated account') != -1 or line.find('username') != -1):
		profile_test2 = "PASSED: Revert Profile Edits Test (profile names changed)"
		failed_profile2 = False
		break
	if failed_profile2 and line and line.find('Your new username has already been taken') != -1:
		profile_test2 = "PASSED: Revert Profile Edits Test (profile name already taken)"
		failed_profile2 = False
		break
	
	line = test_output.readline()
if failed_profile2:
	profile_test2 = "FAILED: Revert Profile Edits Test"
test_output.close()


# post curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"topic\":\"general\",\"type\":\"1\",\"title\":\"TESTPOST\",\"content\":\"hello hello hello hello\",\"anon\":\"0\"}" http://localhost:5000/createpost/

#Missing Authorization Header
#Missing JSON Element (???)


# vote curl
#curl -i -X POST -H "Authorization: Bearer <access_token>" -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/

print(reg_test)
print(login_test)
print(profile_test1)
print(profile_test2)