from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from extensions import mysql
from datetime import datetime
import re
import bcrypt

weave_register = Blueprint('weave_register', __name__)


# # # # Backend code for user registration on Weave.
# # Expects a POST request with a JSON object. Details are discussed in "/api/README.md".
# # Returns a JSON with JWT access tokens and confirmation of the user's identity. 
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
@weave_register.route('/register/', methods=["GET", "POST"])
def weave_register_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # # # Validates JSON information.
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400  
        reg_info = request.get_json()

        # Checks that the JSON has all elements.
        if ("username" not in reg_info or "password" not in reg_info or "email" not in reg_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400  

        # Checks for valid username format.
        # According to the backlog and the database, usernames should be between 6 and 20 characters.
        # Accepted characters are capital letters, lowercase letters, numerals, as well as: - _ 
        if (re.search("^[A-Za-z0-9_-]{6,20}$", reg_info["username"]) == None):
            return jsonify({'error_message':'Your username is invalid.'}), 400  

        # There also cannot be repeated usernames, which should be checked for before we get a SQL error.    
        cursor.execute("SELECT username FROM UserAccount WHERE username = %s;", (reg_info["username"],))
        for row in cursor:
            if reg_info["username"] == row["username"]:
                return jsonify({'error_message':'This username has already been used.'}), 400  

        # Checks for valid email format. 
        # Currently, the conditional checks the email string against a regex. See https://regex101.com/ for explanation.
        # Email regex should be [standard_characters]@[address].[suffix]
        # Validation also needs to check email length. Max length is 50.
        if (re.search("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$", reg_info["email"]) == None):
            return jsonify({'error_message':'Your email address is invalid.'}), 400  
        if (len(reg_info["email"]) > 50):
            return jsonify({'error_message':'Your email address is invalid.'}), 400  

        # There also cannot be repeated email, which should be checked for before we get a SQL error.    
        cursor.execute("SELECT email FROM UserAccount WHERE email = %s;", (reg_info["email"],))
        for row in cursor:
            if reg_info["email"] == row["email"]:
                return jsonify({'error_message':'This email has already been used.'}), 400  
        
        # Checks for valid password format.
        # According to the backlog and the database, passwords should be between 6 and 20 characters.
        # Accepted characters are capital letters, lowercase letters, numerals, as well as: ! @ # $ % & ? < > - _ +
        # They should also contain one capital, one lowercase, and one number.
        if (re.search("[A-Z]", reg_info["password"]) == None):
            return jsonify({'error_message':'Passwords need an uppercase letter.'}), 400  
        if (re.search("[a-z]", reg_info["password"]) == None):
            return jsonify({'error_message':'Passwords need a lowercase letter.'}), 400
        if (re.search("[0-9]", reg_info["password"]) == None):
            return jsonify({'error_message':'Passwords need a number.'}), 400        
        if (re.search("^[A-Za-z0-9!@#$%&?<>-_+]{6,20}$", reg_info["password"]) == None):
            return jsonify({'error_message':'Your password has an invalid character.'}), 400
        
        # # # End validation
        # Hashes the password for security before storing it in the database (using bcrypt).
        hash_password = bcrypt.hashpw(reg_info["password"].encode('utf8'), bcrypt.gensalt())

        # Gets the current date in "YYYY-MM-DD HH:MI:SS" format.
        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        # Insert new user into database.
        register_query = "INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        register_values = (reg_info["username"], reg_info["email"], hash_password, None, None, current_date , None, None, "0", "0")
        cursor.execute(register_query, register_values)
        mysql.connection.commit()         
            
        # Creates access token and sends it back once user is confirmed to be created
        ret = {
                'access_token': create_access_token(identity=reg_info["username"]),
                'refresh_token': create_refresh_token(identity=reg_info["username"]),
                'username': reg_info["username"]
        }
        return jsonify(ret), 201

    # Not a POST request.        
    else:
        return "serve register page"