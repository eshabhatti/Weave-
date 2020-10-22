# # # # # # # # # # # # # # # # # # # 
# # # # # FOLLOW CURL TESTS # # # # # 
# # # # # # # # # # # # # # # # # # # 
import subprocess
import mysql.connector

# Initializes the database instance.
mysql_cred = open("../credentials/dbcredentials.txt", "r")
db = mysql.connector.connect(
	host="localhost", 
	user=mysql_cred.readline().strip("\n\r "), 
	password=mysql_cred.readline().strip("\n\r "),
    database="weave"
)
mysql_cred.close()


# Runs test cases.
def follow_test(access_token, valid_post_1, valid_post_2):

    cursor = db.cursor()
    follow_tests = []

    # Adds information to the database needed to run all further tests.
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    return follow_tests