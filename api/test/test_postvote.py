# # # # # # # # # # # # # # # # # # # # #
# # # # # POST VOTE CURL TESTS  # # # # # 
# # # # # # # # # # # # # # # # # # # # #
import subprocess

def post_vote_test(access_token):

    postvote_tests = []

    # Post Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"1\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 1') != -1:
    		vote_test = "PASSED: Posts can be upvoted."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test = "FAILED: Posts can be upvoted."
    test_output.close()
    postvote_tests.append(vote_test)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Remove Post Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"1\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 0') != -1:
    		vote_test = "PASSED: Upvotes on posts can be removed."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test = "FAILED: Upvotes on posts can be removed."
    test_output.close()
    postvote_tests.append(vote_test)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Post Downvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"1\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": -1') != -1:
    		vote_test = "PASSED: Posts can be downvoted."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test = "FAILED: Posts can be downvoted."
    test_output.close()
    postvote_tests.append(vote_test)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # Post Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"1\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 0') != -1:
    		vote_test = "PASSED: Downvotes on posts can be removed."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test = "FAILED: Downvotes on posts can be removed."
    test_output.close()
    postvote_tests.append(vote_test)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Post Upvote to Downvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"1\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()
    subprocess.call([r'vote_test.cmd'])

    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"1\\",\\"type\\":\\"1\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": -1') != -1:
    		vote_test = "PASSED: Upvotes on posts can be changed to downvotes."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test = "FAILED: Upvotes on posts can be changed to downvotes."
    test_output.close()
    postvote_tests.append(vote_test)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Post Downvote to Upvote Test
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"2\\",\\"type\\":\\"1\\",\\"vote\\":-1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()
    subprocess.call([r'vote_test.cmd'])

    new_post_test = open('vote_test.cmd', 'w+')
    new_post_test.seek(0)
    new_post_test.write("""curl -i -X POST -H "Authorization: Bearer """ + access_token + """\" -H "Content-Type:application/json" -d "{\\"id\\":\\"2\\",\\"type\\":\\"1\\",\\"vote\\":1}" http://localhost:5000/vote/ > test_output.txt""")
    new_post_test.truncate()
    new_post_test.close()

    subprocess.call([r'vote_test.cmd'])
    test_output = open("test_output.txt", "r")

    line = test_output.readline()
    failed_vote = True
    while line:	
    	if failed_vote and line and line.find('\"voteState\": 1') != -1:
    		vote_test = "PASSED: Downvotes on posts can be changed to upvotes."
    		failed_vote = False
    		break
    	line = test_output.readline()
    if failed_vote:
    	vote_test = "FAILED: Downvotes on posts can be changed to upvotes."
    test_output.close()
    postvote_tests.append(vote_test)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    return postvote_tests