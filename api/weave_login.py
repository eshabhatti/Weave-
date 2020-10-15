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
# # Returns a JSON including JWT tokens and confirmation of user identity.
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\"}" http://localhost:5000/login/
@weave_login.route('/login/', methods=["GET", "POST"])
def weave_user_login():

    # The backend has received a login POST request.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400  
        login_info = request.get_json()
        
        # Checks for the correct credentials.
        if ("username" not in login_info or "password" not in login_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400  
        
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
        cursor.execute("SELECT encrypted_password FROM UserAccount WHERE " + username_type + " = %s;", (username,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'Username and password do not match.'}), 401
        hashed_password = cursor.fetchall()
        hashed_password = (hashed_password[0])["encrypted_password"]
        
        # This will validate the user's password:
        valid_password = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')) 
        if (not valid_password):
            return jsonify({'error_message':'Username and password do not match.'}), 401 
            
        # This will fetch the user's information from the database after validation (should it all be grabbed in the first execute?)
        cursor.execute("SELECT * FROM UserAccount WHERE " + username_type + " = %s", (username,))
        account = cursor.fetchall()

        # Return "Profile page of account"
        for row in cursor:
            # Creates an access token and refresh token using the usernamem
            ret = {
                'access_token': create_access_token(identity=row["username"]),
                'refresh_token': create_refresh_token(identity=row["username"]),
                'username': row["username"]
            }
            return jsonify(ret), 200
        return jsonify({'error_message':'Username and password do not match.'}), 401

    # Not a POST request
    else:
        return ("", 204)


# # # # Backend code for logging out of Weave
# # Right now this route blacklists access tokens, and another route blacklists refresh tokens.
# # Returns an empty access token and confirmation of user identity.
@weave_login.route("/logout", methods=["DELETE"])
@jwt_required
def weave_logout():

    # Initializes MySQL cursor.
    cursor = mysql.connection.cursor()
    
    # Gets the current JWT token.
    token = get_raw_jwt()["jti"]

    # Checks to see if the token already exists in the database.
    # This shouldn't ever happen BUT it's useful during debugging since the database commits before return to frontend.
    cursor.execute("SELECT token FROM Blacklist WHERE token = %s;", (token,))
    if (cursor.rowcount != 0):
        return jsonify({'error_message':'Token already blacklisted.'}), 400

    # Blacklists access tokens by sending them to the database.
    cursor.execute("INSERT INTO Blacklist VALUES (%s);", (token,))
    mysql.connection.commit()

    # Returns empty access token, 
    blacklist_ret = {
        'access_token': None,
        'username': get_jwt_identity()
    }
    return jsonify(blacklist_ret), 200


# # # # Backend code for logging out of Weave
# # Right now this route blacklists refresh tokens, and another route blacklists access tokens.
# # Returns empty refresh token and confirmation of user identity.
@weave_login.route("/logout2", methods=["DELETE"])
@jwt_refresh_token_required
def weave_logout2():
    
    # Initializes MySQL cursor.
    cursor = mysql.connection.cursor()

    # Gets the current JWT token.
    token = get_raw_jwt()["jti"]

    # Checks to see if the token already exists in the database.
    # This shouldn't ever happen BUT it's useful during debugging since the database commits before return to frontend.
    cursor.execute("SELECT token FROM Blacklist WHERE token = %s;", (token,))
    if (cursor.rowcount != 0):
        return jsonify({'error_message':'Token already blacklisted.'}), 400
    
    # Blacklists refresh tokens by sending them to the database.
    cursor.execute("INSERT INTO Blacklist VALUES (%s);", (token,))
    mysql.connection.commit()

    # Returns empty refresh token, 
    blacklist_ret = {
        'refresh_token': None,
        'username': get_jwt_identity()
    }
    return jsonify(blacklist_ret), 200
