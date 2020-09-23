import time
import re
import bcrypt
from datetime import datetime
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Config for MySQL
# RUN CREATETABLES.SQL ON YOUR LOCAL MYSQL SERVER IN ORDER FOR THE DATABASE TO WORK
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'     # Credentials should be saved in an untracked file during real deployment
app.config['MYSQL_PASSWORD'] = 'pass' # Original password is "pass"
app.config['MYSQL_DB'] = 'weave'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initializes MySQL
mysql = MySQL(app)


# # # # Backend code for TIME requests. 
# # This is no longer implmented in the frontend, I believe.
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

# # # # Backend code for REGISTER requests.
# # Expects a POST request with a JSON formatted like: {"username":"[username]","password":"[password-plaintext]","email":"[email]"}  
# # See an example of current function (on Windows) with:
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
@app.route('/register/', methods=["GET", "POST"])
def register_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # # # Validates JSON information.
        valid_info = True

        # Checks for JSON format.
        if (not request.is_json):
            return "Error: Request is not JSON"
        reg_info = request.get_json()

        # Checks for valid username format.
        # According to the backlog and the database, usernames should be between 6 and 20 characters.
        # Accepted characters are capital letters, lowercase letters, numerals, as well as: - _ 
        if (re.search("^[A-Za-z0-9_-]{6,20}$", reg_info["username"]) == None):
            return "Error: Invalid username format"

        # There also cannot be repeated usernames, which should be checked for before we get a SQL error.    
        username_query = "SELECT username from UserAccount WHERE username = \"" + reg_info["username"] + "\";"
        cursor.execute(username_query)
        for row in cursor:
            if reg_info["username"] == row["username"]:
                return "Error: Repeated username"
        
        # Checks for valid password format.
        # According to the backlog and the database, passwords should be between 6 and 20 characters.
        # Accepted characters are capital letters, lowercase letters, numerals, as well as: ! @ # $ % & ? < > - _ +
        # They should also contain one capital, one lowercase, and one number.
        if (re.search("^\S*[A-Z]\S*$", reg_info["password"]) == None):
            return "Error: No capital in password"
        if (re.search("^\S*[a-z]\S*$", reg_info["password"]) == None):
            return "Error: No lowercase in password"
        if (re.search("^\S*[0-9]\S*$", reg_info["password"]) == None):
            return "Error: No number in password"
        if (re.search("^[A-Za-z0-9!@#$%&?<>-_+]{6,20}$", reg_info["password"]) == None):
            return "Error: Invalid password format"

        # Checks for valid email format. 
        # Currently, the conditional checks the email string against a regex. See https://regex101.com/ for explanation.
        # Email regex should be [standard_characters]@[address].[suffix]
        # Validation also needs to check email length. Max length is 50.
        if (re.search("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$", reg_info["email"]) == None):
            return "Error: Invalid email format"
        if (len(reg_info["email"]) > 50):
            return "Error: Invalid email length"

        # There also cannot be repeated email, which should be checked for before we get a SQL error.    
        email_query = "SELECT email from UserAccount WHERE email = \"" + reg_info["email"] + "\";"
        cursor.execute(email_query)
        for row in cursor:
            if reg_info["email"] == row["email"]:
                return "Error: Repeated email"
        
        # # # End validation
        if(valid_info):

            # Hashes the password for security before storing it in the database (using bcrypt).
            hash_password = bcrypt.hashpw(reg_info["password"].encode(), bcrypt.gensalt())

            # Gets the current date in "YYYY-MM-DD" format.
            current_date = datetime.today().strftime("%Y-%m-%d")

            # Insert new user into database.
            register_query = "INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            register_values = (reg_info["username"], reg_info["email"], hash_password, None, None, current_date , None, None, "0", "0")
            cursor.execute(register_query, register_values)
            mysql.connection.commit()         
            
            # Print resulting table for testing.
            cursor.execute("SELECT * from UserAccount")
            print(cursor.fetchall())
            return "send user to their new profile page"

    # Not a POST request.        
    else:
        return "serve register page"

# # # # Backend code for LOGIN requests
# Should expect a POST request with a JSON like this: {"username":"[username_or_email]","password":"[password]""}
# Test basic functionality with the following script (on Windows):
# curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\"}" http://localhost:5000/login/
@app.route('/login/', methods=["GET", "POST"])
def login_user():

    # The backend has received a login POST request.
    if request.method == "POST":
        # Checks for JSON format.
        if (not request.is_json):
            return "Error: Request is not JSON"
        login_info = request.get_json()
        
        if ("username" not in login_info or "password" not in login_info):
            return "Error: Missing credentials"
        
        # Get username and password from json
        username = login_info['username']
        password = login_info['password']

        # Need to determine if username in the JSON relates to the username column or the email column
        username_type = "username"
        if (re.search("@", username) != None):
           username_type = "email"
           
        # Need to pull the hashed password of the selected user out of the database
        # This also needs to catch the case of an invalid user
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT encrypted_password FROM UserAccount WHERE " + username_type + " = %s", (username,)) #args have to be a tuple
        hashed_password = cursor.fetchall();
        if (hashed_password == []):
            return "Invalid credentials"
        hashed_password = (hashed_password[0])["encrypted_password"]
        
        # This will validate the user's password:
        valid_password = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')) #have to encode strings here
        if (not valid_password):
            return "Invalid credentials"
            
        # This will fetch the user's information from the database after validation (should it all be grabbed in the first execute?)
        cursor.execute("SELECT encrypted_password FROM UserAccount WHERE " + username_type + " = %s", (username,))
        account = cursor.fetchall()
        return "Profile page of account"

    # Not a POST request
    else:
        return "Serve login page"

#def logout_user():

if __name__ == "__main__":
   app.run()
