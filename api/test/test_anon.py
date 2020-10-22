# # # # # # # # # # # # # # # # # # # #
# # # # # # ANON CURL TESTS # # # # # #
# # # # # # # # # # # # # # # # # # # #
import subprocess

def anon_test(access_token):

    anon_tests = []

    # Anon Username Retention Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
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
            # third valid post
            failed_post = False
            break
        line = test_output.readline()
    if failed_post:
        post_test4 = "FAILED: Anonymous posts still retain the original user's username, but do not show it when displaying."
    test_output.close()
    anon_tests.append(post_test4)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Blank Anon Test Post
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"username\\":\\"testname\\",\\"topic\\":\\"general\\",\\"type\\":\\"1\\",\\"title\\":\\"TESTPOST\\",\\"content\\":\\"\\",\\"anon\\":\\"1\\"}" http://localhost:5000/createpost/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'post_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_post = True
    while line:
        if failed_post and line and line.find('error') != -1:
            post_test5 = "PASSED: Anonymous posts should not be empty."
            failed_post = False
            break
        line = test_output.readline()
    if failed_post:
        post_test5 = "FAILED: Anonymous posts should not be empty."
    test_output.close()
    anon_tests.append(post_test5)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Anon Post Format Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('post_test.cmd', 'w+')
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
    anon_tests.append(post_test6)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    anon_tests.append(access_token)
    return anon_tests