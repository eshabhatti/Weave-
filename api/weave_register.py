# # # # Backend code for REGISTER requests.
# # Expects a POST request with a JSON formatted like: {"username":"[username]","password":"[password-plaintext]","email":"[email]"}  
# # See an example of current function (on Windows) with:
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"password\":\"Gudpasswurd22\",\"email\":\"test@tes.com\"}" http://localhost:5000/register/
from flask import Blueprint, request, jsonify
from extensions import mysql
from datetime import datetime
import re
import bcrypt

weave_register = Blueprint('weave_register', __name__)

@weave_register.route('/register/', methods=["GET", "POST"])
def weave_register_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # # # Validates JSON information.
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'})  
        reg_info = request.get_json()

        # Checks that the JSON has all elements.
        if ("username" not in reg_info or "password" not in reg_info or "email" not in reg_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'})  

        # Checks for valid username format.
        # According to the backlog and the database, usernames should be between 6 and 20 characters.
        # Accepted characters are capital letters, lowercase letters, numerals, as well as: - _ 
        if (re.search("^[A-Za-z0-9_-]{6,20}$", reg_info["username"]) == None):
            return jsonify({'error_message':'Your username is invalid.'})  

        # There also cannot be repeated usernames, which should be checked for before we get a SQL error.    
        username_query = "SELECT username from UserAccount WHERE username = \"" + reg_info["username"] + "\";"
        cursor.execute(username_query)
        for row in cursor:
            if reg_info["username"] == row["username"]:
                return jsonify({'error_message':'This username has already been used.'})  

        # Checks for valid email format. 
        # Currently, the conditional checks the email string against a regex. See https://regex101.com/ for explanation.
        # Email regex should be [standard_characters]@[address].[suffix]
        # Validation also needs to check email length. Max length is 50.
        if (re.search("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$", reg_info["email"]) == None):
            return jsonify({'error_message':'Your email address is invalid.'})  
        if (len(reg_info["email"]) > 50):
            return jsonify({'error_message':'Your email address is invalid.'})  

        # There also cannot be repeated email, which should be checked for before we get a SQL error.    
        email_query = "SELECT email from UserAccount WHERE email = \"" + reg_info["email"] + "\";"
        cursor.execute(email_query)
        for row in cursor:
            if reg_info["email"] == row["email"]:
                return jsonify({'error_message':'This email has already been used.'})  
        
        # Checks for valid password format.
        # According to the backlog and the database, passwords should be between 6 and 20 characters.
        # Accepted characters are capital letters, lowercase letters, numerals, as well as: ! @ # $ % & ? < > - _ +
        # They should also contain one capital, one lowercase, and one number.
        if (re.search("[A-Z]", reg_info["password"]) == None):
            return jsonify({'error_message':'Passwords need an uppercase letter.'})  
        if (re.search("[a-z]", reg_info["password"]) == None):
            return jsonify({'error_message':'Passwords need a lowercase letter.'})  
        if (re.search("[0-9]", reg_info["password"]) == None):
            return jsonify({'error_message':'Passwords need a number.'})        
        if (re.search("^[A-Za-z0-9!@#$%&?<>-_+]{6,20}$", reg_info["password"]) == None):
            return jsonify({'error_message':'Your password has an invalid character.'})
        
        # # # End validation
        # Hashes the password for security before storing it in the database (using bcrypt).
        hash_password = bcrypt.hashpw(reg_info["password"].encode('utf8'), bcrypt.gensalt())

        # Gets the current date in "YYYY-MM-DD" format.
        current_date = datetime.today().strftime("%Y-%m-%d")

        # Insert new user into database.
        register_query = "INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        register_values = (reg_info["username"], reg_info["email"], hash_password, None, None, current_date , None, None, "0", "0")
        cursor.execute(register_query, register_values)
        mysql.connection.commit()         
            
        # Will eventually return login credentials.
        return jsonify({'anything':'anything'})

    # Not a POST request.        
    else:
        return "serve register page"