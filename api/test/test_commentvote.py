# # # # # # # # # # # # # # # # # # # # # #
# # # # # COMMENT VOTE CURL TESTS # # # # # 
# # # # # # # # # # # # # # # # # # # # # #
import subprocess

def comment_vote_test(access_token):

    commentvote_tests = []

    # Comment Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    vote_command = open('vote_test.cmd', 'w+')
    vote_command.seek(0)
    vote_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"2\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    vote_command.truncate()
    vote_command.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 1') != -1:
    		vote_test_1 = "PASSED: Comments can be upvoted."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test_1 = "FAILED: Comments can be upvoted."
    test_output.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Comment Upvote to Downvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    vote_command = open('vote_test.cmd', 'w+')
    vote_command.seek(0)
    vote_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"2\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    vote_command.truncate()
    vote_command.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": -1') != -1:
    		vote_test_5 = "PASSED: Comment upvotes can changed to downvotes."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test_5 = "FAILED: Comment upvotes can changed to downvotes."
    test_output.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Comment Remove Downvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    vote_command = open('vote_test.cmd', 'w+')
    vote_command.seek(0)
    vote_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"2\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    vote_command.truncate()
    vote_command.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 0') != -1:
    		vote_test_4 = "PASSED: Comment downvotes can be removed."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test_4 = "FAILED: Comment downvotes can be removed."
    test_output.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Comment Downvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    vote_command = open('vote_test.cmd', 'w+')
    vote_command.seek(0)
    vote_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"2\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    vote_command.truncate()
    vote_command.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": -1') != -1:
    		vote_test_2 = "PASSED: Comments can be downvoted."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test_2 = "FAILED: Comments can be downvoted."
    test_output.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Comment Downvote to Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    vote_command = open('vote_test.cmd', 'w+')
    vote_command.seek(0)
    vote_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"2\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    vote_command.truncate()
    vote_command.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 1') != -1:
    		vote_test_6 = "PASSED: Comment downvotes can be changed to upvotes."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test_6 = "FAILED: Comment downvotes can be changed to upvotes."
    test_output.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Comment Remove Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    vote_command = open('vote_test.cmd', 'w+')
    vote_command.seek(0)
    vote_command.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"2\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    vote_command.truncate()
    vote_command.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 0') != -1:
    		vote_test_3 = "PASSED: Comment upvotes can be removed."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test_3 = "FAILED: Comment upvotes can be removed."
    test_output.close()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    commentvote_tests.append(vote_test_1)
    commentvote_tests.append(vote_test_2)
    commentvote_tests.append(vote_test_3)
    commentvote_tests.append(vote_test_4)
    commentvote_tests.append(vote_test_5)
    commentvote_tests.append(vote_test_6)
    return commentvote_tests
