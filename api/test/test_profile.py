# # # # # # # # # # # # # # # # # # # # #
# # # # #  PROFILE CURL TESTS   # # # # # 
# # # # # # # # # # # # # # # # # # # # #
import subprocess

def profile_test(access_token):

    # Not sure what these mean so I'll leave them here:
    # user has updated account
    # (error): Your new username has already been taken
    # Missing Authorization Header

    pro_tests = []

    # Correct Profile Edit
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_profile_test = open('profile_test.cmd', 'w+')
    new_profile_test.seek(0)
    new_profile_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"newusername\\":\\"newtestname\\",\\"firstname\\":\\"Bob\\",\\"lastname\\":\\"Banana\\",\\"biocontent\\":\\"Hi I am Bob, aren't I cool?\\",\\"profilepic\\":\\"\\"}" http://localhost:5000/editprofile/ > test_output.txt""")
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
    pro_tests.append(profile_test1)    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Revert Profile Edit (NOT A TEST CASE)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_profile_test = open('profile_test.cmd', 'w+')
    new_profile_test.seek(0)
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
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Blank Profile Input Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_profile_test = open('profile_test.cmd', 'w+')
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
    pro_tests.append(profile_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Invalid Length Profile Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_profile_test = open('profile_test.cmd', 'w+')
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
            profile_test3 = "PASSED: Check that case where too many characters (>250) are entered does not update the database."
            failed_profile = False
            break
        line = test_output.readline()
    if failed_profile:
        profile_test3 = "FAILED: Check that case where too many characters (>250) are entered does not update the database."
    test_output.close()
    pro_tests.append(profile_test3)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    pro_tests.append(access_token)
    return pro_tests