import time
import re
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Config for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass' # original password is pass
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
# # Currently expects a POST request with a JSON formatted like: {"username":"[username]","email":"[email]"}  
# # Needs to be modified to also expect a password field within the JSON: "password":"[password-plaintext]"
# # See an example of current function (on Windows) with:
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\": \"testname\",  \"email\" : \"test@tes.com\" }" http://localhost:5000/register/
@app.route('/register/', methods=["GET", "POST"])
def register_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # # # Validates JSON information.
        valid_info = True

        # Checks for JSON format.
        if (not request.is_json):
            valid_info = False # Should this function just return an error if true?
        reg_info = request.get_json()

        # Checks for valid username format.
        #if(not username_valid(reg_info["username"]))
        #    valid_info = False
        
        # Checks for valid password format.
        #if(not password_valid(reg_info["password"]))
        #    valid_info = False

        # Checks for valid email format. 
        # Currently, the conditional checks the email string against a regex. See https://regex101.com/ for explanation.
        # Email regex should be [standard_characters]@[address].[suffix]
        # Regex works okay (users must have an '@' or a '.') but isn't flawless -- multiple @ are allowed, for instance.
        # Validation also needs to check email length. Max length is 50.
        if (re.search("^\S+@\S+\.\S+$", reg_info["email"]) == None):
            valid_info = False
        
        # # # End validation -- correct formats
        if(valid_info):

            # Insert new user into database.
            # Lots of strings are static right now. Names will probably have to be set to NULL instead.
            # Minor error: the values with "Null" in the above register are written to the database as strings ("Null") rather than the keyword (NULL)
            cursor = mysql.connection.cursor()
            register_query = "INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s);"
            register_values = (reg_info["username"],reg_info["email"], "pass", "word", "real", "user", "1998-12-12" , "Null", "Null", "0", "0")
            cursor.execute(register_query, register_values)
            mysql.connection.commit()         
            
            # Print resulting table for testing.
            cursor.execute("SELECT * from UserAccount")
            print(cursor.fetchall())
            return "send user to their new profile page"

        # # # End validation -- incorrect formats    
        else:
            return "invalid request"

    # Not a POST request.        
    else:
        return "serve register page"

# # # # Backend code for LOGIN requests
# Basically nothing here is implemented yet. Wow.
@app.route('/login/', methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        return "try to login user"
    else:
        return "serve the login page"

if __name__ == "__main__":
   app.run()
