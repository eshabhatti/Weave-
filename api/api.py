import time
import re
import bcrypt
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Config for MySQL
# RUN CREATETABLES.SQL ON YOUR LOCAL MYSQL SERVER IN ORDER FOR THE DATABASE TO WORK
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
# # Currently expects a POST request with a JSON formatted like: {"username":"[username]","password":"[password-plaintext]","email":"[email]"}  
# # See an example of current function (on Windows) with:
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
@app.route('/register/', methods=["GET", "POST"])
def register_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # # # Validates JSON information.
        valid_info = True

        # Checks for JSON format.
        if (not request.is_json):
            return "Error: Request is not JSON"
        reg_info = request.get_json()

        # Checks for valid username format.
        #if(not username_valid(reg_info["username"]))
        #    valid_info = False
        
        # Checks for valid password format.
        # According to the backlog and the database, passwords should be between 6 and 20 characters.
        # They should also contain one capital, one lowercase, and one number.
        if (re.search("^\S*[A-Z]\S*$", reg_info["password"]) == None):
            return "Error: No capital in password"
        if (re.search("^\S*[a-z]\S*$", reg_info["password"]) == None):
            return "Error: No lowercase in password"
        if (re.search("^\S*[0-9]\S*$", reg_info["password"]) == None):
            return "Error: No number in password"
        if len(reg_info["password"]) > 20 or len(reg_info["password"]) < 6: 
            return "Error: Invalid password length"

        # Checks for valid email format. 
        # Currently, the conditional checks the email string against a regex. See https://regex101.com/ for explanation.
        # Email regex should be [standard_characters]@[address].[suffix]
        # Validation also needs to check email length. Max length is 50.
        if (re.search("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$", reg_info["email"]) == None):
            return "Error: Invalid email format"
        if (len(reg_info["email"]) > 50):
            return "Error: Invalid email length"
        
        # # # End validation
        if(valid_info):

            # # Hashes the password for security before storing it in the database
            # Creates a random salt using the bcrypt library.
            salt = bcrypt.gensalt()
            # Hashes the password with bcrypt.
            hash_password = bcrypt.hashpw(reg_info["password"].encode(), salt)

            # Insert new user into database.
            # Lots of strings are static right now. Names will probably have to be set to NULL instead.
            # We also need to insert the actual date into the database, not just a static value.
            # Minor error: the values with "Null" in the above register are written to the database as strings ("Null") rather than the keyword (NULL)
            cursor = mysql.connection.cursor()
            register_query = "INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            register_values = (reg_info["username"], reg_info["email"], hash_password, "real", "user", "1998-12-12" , "Null", "Null", "0", "0")
            cursor.execute(register_query, register_values)
            mysql.connection.commit()         
            
            # Print resulting table for testing.
            cursor.execute("SELECT * from UserAccount")
            print(cursor.fetchall())
            return "send user to their new profile page"

        # # # End validation -- incorrect formats    
        # else:
        #    return "invalid request"

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
