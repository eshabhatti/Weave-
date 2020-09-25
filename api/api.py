import time
import re
import bcrypt
import datetime
from flask import Flask, request, jsonify
from extensions import mysql
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from flask_cors import CORS

from models import User
from weavepost import weave_post
from weaveregister import weave_register

# Initializes Flask
app = Flask(__name__)
flask_cred = open("credentials/flaskcredentials.txt")
app.secret_key = flask_cred.readline().strip("\n\r ").encode('utf8')

# Configures and initializes JWT
app.config['JWT_SECRET_KEY'] = flask_cred.readline().strip("\n\r ")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
jwt = JWTManager(app)
flask_cred.close()

# Allows CORS on all domains.
CORS(app)

# Config for MySQL
# RUN CREATETABLES.SQL ON YOUR LOCAL MYSQL SERVER IN ORDER FOR THE DATABASE TO WORK
mysql_cred = open("credentials/dbcredentials.txt")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = mysql_cred.readline().strip("\n\r ")      
app.config['MYSQL_PASSWORD'] = mysql_cred.readline().strip("\n\r ") 
app.config['MYSQL_DB'] = 'weave'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql_cred.close()

# Initializes MySQL
mysql.init_app(app)

# Breaks the Flask API into multiple sections.
with app.app_context():
    app.register_blueprint(weave_post)
    app.register_blueprint(weave_register)

# # # # Backend code for TIME requests. 
# # This is no longer implmented in the frontend, I believe.
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

# # # # Backend code for LOGIN requests
# Should expect a POST request with a JSON like this: {"username":"[username_or_email]","password":"[password]"}
# Test basic functionality with the following script (on Windows):
# curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\"}" http://localhost:5000/login/
@app.route('/login/', methods=["GET", "POST"])
def weave_login():

    # The backend has received a login POST request.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return "{\"error_message\":\"not_JSON\"}"
        login_info = request.get_json()
        
        # Checks for the correct credentials.
        if ("username" not in login_info or "password" not in login_info):
            return "{\"error_message\":\"missing_element\"}"
        
        # Get username and password from JSON.
        username = login_info["username"]
        password = login_info["password"]

        # Determines if username in the JSON relates to the username column or the email column
        username_type = "username"
        if (re.search("@", username) != None):
           username_type = "email"
           
        # Need to pull the hashed password of the selected user out of the database
        # This also needs to catch the case of an invalid user
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT encrypted_password FROM UserAccount WHERE " + username_type + " = %s;", (username,)) #args have to be a tuple
        if (cursor.rowcount == 0):
            return "{\"error_message\":\"invalid_credentials\"}"
        hashed_password = cursor.fetchall()
        hashed_password = (hashed_password[0])["encrypted_password"]
        
        # This will validate the user's password:
        valid_password = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')) #have to encode strings here
        if (not valid_password):
            return "{\"error_message\":\"invalid_credentials\"}"
            
        # This will fetch the user's information from the database after validation (should it all be grabbed in the first execute?)
        cursor.execute("SELECT * FROM UserAccount WHERE " + username_type + " = %s", (username,))
        account = cursor.fetchall()
        print(account) # debugging

        # Return "Profile page of account"
        for row in cursor:
            # creates an access token and refresh token using the usernamem
            ret = {
                'access_token': create_access_token(identity=row["username"]),
                'refresh_token': create_refresh_token(identity=row["username"])
            }
            return jsonify(ret), 200
        return "{\"error_message\": \"invalid_credentials\"}"

    # Not a POST request
    else:
        return "Serve login page"

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # refresh token endpoint
    current_user = get_jwt_identity()
    ret = {
            'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

@app.route("/protected")
@jwt_required
def protected():
    # Access the identity of current user
    current_user = get_jwt_identity
    return jsonify(logged_in=current_user)

@app.route("/partially_protected")
@jwt_optional
def partially_protected():
    # Access the identity of current user
    current_user = get_jwt_identity
    if current_user:
        return jsonify(logged_in=current_user)
    else:
        return jsonify(logged_in='anon')

# # # # Backend code for LOGOUT requests
@app.route("/logout")
def weave_logout():
    # logs the user using flask_login's method
    # login_required to travel to this route

    # travel to login page again
    # return redirect(url_for("login"))

    return "Logged out successfuly"


if __name__ == "__main__":
   app.run()
