# # # # # # # # # # # # # # # # # # # #
# # # # # # POST CURL TESTS # # # # # #
# # # # # # # # # # # # # # # # # # # #
import subprocess

def post_test(access_token):

    post_tests = []

    # Correct Post Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"hello hello hello hello\\",\\"anon\\":\\"0\\"}" http://localhost:5000/createpost/ > test_output.txt""")
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
    if failed_post:
        post_test1 = "FAILED: Check that a valid post should always be posted."
    test_output.close()
    post_tests.append(post_test1)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Blank Post Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
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
    if failed_post:
        post_test2 = "FAILED: Check that blank posts can't be posted."
    test_output.close()
    post_tests.append(post_test2)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Invalid Post Length Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
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
    post_tests.append(post_test3)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    post_tests.append(access_token)
    return post_tests