from flask import Blueprint, request, jsonify, current_app
from extensions import mysql
from os import path
import re
from werkzeug.utils import secure_filename
import json

weave_profile = Blueprint('weave_profile', __name__)


# # # # Backend code for editing profiles on Weave. 
# # DOES NOT expect a JSON but DOES expect a unique URL for the profile that needs to be displayed.
@weave_profile.route("/profile/<username>", methods=["GET"])
# @login_required
def weave_profile_data(username):
    
    # The backend has received a profile GET request.
    if request.method == "GET":
    
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks if username exists in db (need to grab more things eventually)
        cursor.execute("SELECT user_bio, user_pic, follower_count, first_name, last_name, date_joined FROM UserAccount WHERE username = %s;", (username,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'User does not exist'})
        
        # Returns each needed item in one JSON object
        return (cursor.fetchall())[0]


# # # # Backend code for editing profiles on Weave. 
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"newusername\":\"newtestname\",\"firstname\":\"Bob\",\"lastname\":\"Banana\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"newtestname\",\"newusername\":\"testname\",\"firstname\":\"Banana\",\"lastname\":\"Bob\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
@weave_profile.route('/editprofile/', methods=["GET", "POST"])
# @login_required
def weave_edit_profile():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # Uploads a photo if attached
        new_filename = "" #currently no uploaded file will stil change the path, should change
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                new_filename = secure_filename(file.filename)
                prefix = 0
                #adjusts filename for duplicate names
                while (path.exists(str(current_app.config['UPLOAD_FOLDER']) + str(prefix) + str(new_filename))):
                    prefix += 1
                new_filename = str(prefix) + new_filename
                file.save(str(current_app.config['UPLOAD_FOLDER']) + str(new_filename))
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # # # Validates JSON information.
        # Checks for JSON format. (Possibly change, this is how i got it to work with sending both an image and json data)
        mod_info = (request.form.to_dict())['json']
        mod_info = json.loads(mod_info)
        if type(mod_info) is not dict:
            return jsonify({'error_message':'Request Error: Not JSON.'}) 

        # Checks that the JSON has all elements.
        if ("username" not in mod_info or "newusername" not in mod_info or "firstname" not in mod_info or "lastname" not in mod_info or "biocontent" not in mod_info or "profilepic" not in mod_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'})

        # The original username should not need to be validated since it is not user input. (?)
        # If newusername is the same as the old one, then once again no validation needs to be done.
        # If there is a difference, however, then the new username needs to be checked for proper format.
        if (mod_info["username"] != mod_info["newusername"]):
            if (re.search("^[A-Za-z0-9_-]{6,20}$", mod_info["newusername"]) == None):
                return jsonify({'error_message':'Your new username is invalid.'})
        final_username = mod_info["newusername"]

        # There also cannot be repeated usernames, which should be checked for before we get a SQL error.    
        username_query = "SELECT username from UserAccount WHERE username = \"" + mod_info["newusername"] + "\";"
        cursor.execute(username_query)
        for row in cursor:
            if mod_info["newusername"] == row["username"]:
                return jsonify({'error_message':'Your new username has already been taken.'})  

        # If the name elements of the JSON are not empty strings, they also need to be checked.
        # Only capitals, lowercases, and numbers should be allow in names.
        # There should also not be more than 15 characters in each.
        final_firstname = None
        if (mod_info["firstname"] != ""):
            if (re.search("^[A-Za-z0-9]{0,15}", mod_info["firstname"]) == None):
                return jsonify({'error_message':'Your name is invalid.'})
            else:
                final_firstname = mod_info["firstname"]

        final_lastname = None
        if (mod_info["lastname"] != ""):
            if (re.search("^[A-Za-z0-9]{0,15}", mod_info["lastname"]) == None):
                return jsonify({'error_message':'Your name is invalid.'})
            else:
                final_lastname = mod_info["lastname"]

        # All biocontent should be fine EXCEPT FOR QUOTE CHARACTERS, WHICH MUST BE REPLACED BELOW.
        final_biocontent = None
        if (mod_info["biocontent"] != ""):
            final_biocontent = mod_info["biocontent"].replace("\\\"", "\\\\\\\"")

        # # # End validation
        # Updates the database with the new information.
        mod_query = "UPDATE UserAccount SET username = %s, first_name = %s, last_name = %s, user_bio = %s, user_pic = %s WHERE username = %s;"
        mod_values = (final_username, final_firstname, final_lastname, final_biocontent, new_filename, mod_info["username"])
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit() 

        # Prints new database row for debugging
        cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (mod_info["newusername"],))
        print(cursor.fetchall())
        return "user has updated account"

    # Not a POST request.        
    else:
        return "serve edit profile page"
