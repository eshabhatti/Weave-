# # # # # # # # # # # # # # # # # # # #
# # # # # REGISTER CURL TESTS # # # # #
# # # # # # # # # # # # # # # # # # # # 
import subprocess

def registration_test():

    reg_test = []

    # # Correct Registration Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
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
    reg_test.append(reg_test1)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # Register Existing Username Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"password\\":\\"Gudpasswurd22\\",\\"email\\":\\"testtess@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

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
    reg_test.append(reg_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # Register Existing Email Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testname111\\",\\"password\\":\\"Gudpasswurd22\\",\\"email\\":\\"test@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('This email has already been used.') != -1:
            reg_test3 = "PASSED: Checking that duplicate emails cannot be used"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test3 = "FAILED: Checking that duplicate emails cannot be used"
    test_output.close()
    reg_test.append(reg_test3)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # # Register Blank User and Password Test 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
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
            reg_test4 = "PASSED: Checking that empty inputs can't be accepted"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test4 = "FAILED: Checking that empty inputs can't be accepted"
    test_output.close()
    reg_test.append(reg_test4)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Small Username (<6 Chars) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"test\\",\\"password\\":\\"Gudpassword3\\",\\"email\\":\\"test@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Your username is invalid.') != -1:
            reg_test5 = "PASSED: Checking that inputs with incorrect format can't be accepted (username less than 6 chars)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test5 = "FAILED: Checking that inputs with incorrect format can't be accepted (username less than 6 chars)"
    test_output.close()
    reg_test.append(reg_test5)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Large Username (>42 Chars) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testtesttetesttesttetesttesttetesttesttetesttesttetesttestte\\",\\"password\\":\\"testTEST33\\",\\"email\\":\\"test@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Your username is invalid.') != -1:
            reg_test6 = "PASSED: Checking that inputs with incorrect format can't be accepted (username greater than 42 characters)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test6 = "FAILED: Checking that inputs with incorrect format can't be accepted (username greater than 42 characters)"
    test_output.close()
    reg_test.append(reg_test6)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Length Password (>20 Chars) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"testTEST3333333333333333333333333333333333\\",\\"email\\":\\"testtesta@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Your password has an invalid character.') != -1:
            reg_test7 = "PASSED: Checking that inputs with incorrect format can't be accepted (password length)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test7 = "FAILED: Checking that inputs with incorrect format can't be accepted (password length)"
    test_output.close()
    reg_test.append(reg_test7)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Length Email (>50 Chars) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"testTEST3\\",\\"email\\":\\"testtestatestststeststsasdfadsfafsdfasdfasdfljakfdlja@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Your email address is invalid.') != -1:
            reg_test8 = "PASSED: Checking that inputs with incorrect format can't be accepted (email length)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test8 = "FAILED: Checking that inputs with incorrect format can't be accepted (email length)"
    test_output.close()
    reg_test.append(reg_test8)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Email Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"testTEST3\\",\\"email\\":\\"testemail\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Your email address is invalid.') != -1:
            reg_test9 = "PASSED: Checking that inputs with incorrect format can't be accepted (email regex)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test9 = "FAILED: Checking that inputs with incorrect format can't be accepted (email regex)"
    test_output.close()
    reg_test.append(reg_test9)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Password (Invalid Chars) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"testTEST 33\\",\\"email\\":\\"testtesta@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Your password has an invalid character.') != -1:
            reg_test10 = "PASSED: Checking that inputs with incorrect format can't be accepted (password characters)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test10 = "FAILED: Checking that inputs with incorrect format can't be accepted (password characters)"
    test_output.close()
    reg_test.append(reg_test10)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Password (No Uppercase) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"testtest33\\",\\"email\\":\\"testtesta@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Passwords need an uppercase letter.') != -1:
            reg_test11 = "PASSED: Checking that inputs with incorrect format can't be accepted (no uppercase in password)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test11 = "FAILED: Checking that inputs with incorrect format can't be accepted (no uppercase in password)"
    test_output.close()
    reg_test.append(reg_test11)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Password (No Lowercase) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"TESTTEST33\\",\\"email\\":\\"testtesta@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Passwords need a lowercase letter.') != -1:
            reg_test12 = "PASSED: Checking that inputs with incorrect format can't be accepted (no lowercase in password)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test12 = "FAILED: Checking that inputs with incorrect format can't be accepted (no lowercase in password)"
    test_output.close()
    reg_test.append(reg_test12)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Register Invalid Password (No Number) Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_register_test = open('registration_test.cmd', 'w+')
    new_register_test.seek(0)
    new_register_test.write("""curl -i -X POST -H "Content-Type:application/json" -d "{\\"username\\":\\"testertest\\",\\"password\\":\\"TESTtester\\",\\"email\\":\\"testtesta@tes.com\\"}" http://localhost:5000/register/ > test_output.txt""")
    new_register_test.truncate()
    new_register_test.close()

    subprocess.call([r'registration_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_reg = True
    while line:
        if failed_reg and line and line.find('Passwords need a number.') != -1:
            reg_test13 = "PASSED: Checking that inputs with incorrect format can't be accepted (no number in password)"
            failed_reg = False
            break
        line = test_output.readline()
    if failed_reg:
        reg_test13 = "FAILED: Checking that inputs with incorrect format can't be accepted (no number in password)"
    test_output.close()
    reg_test.append(reg_test13)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    return reg_test