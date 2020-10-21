# # # # # # # # # # # # # # # # # # # # #
# # # # # # LOGIN CURL TESTS  # # # # # #
# # # # # # # # # # # # # # # # # # # # #
import subprocess

def login_test():

    login_tests = []

    # Correct Login Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_login_test = open('login_test.cmd', 'w+')
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
    login_tests.append(login_test1)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Empty Input Login Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_login_test = open('login_test.cmd', 'w+')
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
    login_tests.append(login_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    # Nonexistant User Login Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #    
    new_login_test = open('login_test.cmd', 'w+')
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
    login_tests.append(login_test3)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    login_tests.append(access_token)
    return login_tests