from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from extensions import mysql
import bcrypt
import re

weave_login = Blueprint('weave_login', __name__)


# # # # Backend code for logging into Weave. 
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\"}" http://localhost:5000/login/
@weave_login.route('/login/', methods=["GET", "POST"])
def weave_user_login():

    # The backend has received a login POST request.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'})  
        login_info = request.get_json()
        
        # Checks for the correct credentials.
        if ("username" not in login_info or "password" not in login_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'})  
        
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
            return jsonify({'error_message':'Username and password do not match.'}) 
        hashed_password = cursor.fetchall()
        hashed_password = (hashed_password[0])["encrypted_password"]
        
        # This will validate the user's password:
        valid_password = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')) #have to encode strings here
        if (not valid_password):
            return jsonify({'error_message':'Username and password do not match.'}) 
            
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
        return jsonify({'error_message':'Username and password do not match.'})  

    # Not a POST request
    else:
        return ("", 204)


# # # # Backend code for logging out of Weave
# # Needs to be implemented still. 
@app.route("/logout")
def weave_logout():
    # logs the user using flask_login's method
    # login_required to travel to this route

    # travel to login page again
    # return redirect(url_for("login"))

    return "Logged out successfuly"
