from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from os import path
import re
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import json

weave_profile = Blueprint('weave_profile', __name__)


# # # # Backend code for viewing profiles on Weave.
# # Needs to make a separate call to profilepic/<username> to get the profile picture
# # DOES NOT expect a JSON but DOES expect a unique URL for the profile that needs to be displayed.
# # Returns a JSON with profile information including the user's real name, date joined, bio, profile picture, and follower count.
@weave_profile.route("/profile/<username>", methods=["GET"])
@jwt_required
def weave_profile_data(username):

    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks if username exists in db and grabs relevant data
        cursor.execute("SELECT user_bio, user_pic, follower_count, first_name, last_name, date_joined FROM UserAccount WHERE username = %s;", (username,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'User does not exist'}), 404

        # Returns each needed item in one JSON object
        profile_data = (cursor.fetchall())[0]
        profile_data["username"] = get_jwt_identity()
        if (profile_data["user_pic"] == None):
            profile_data["user_pic"] = None
        else:
            profile_data["user_pic"] = "http://localhost:5000/profile_picture/" + username
        return profile_data

# # # # Backend code for editing user profile pictures on Weave.
# # Needs to be called in cordination with the /profile/<username> route.
# # DOES NOT expect a JSON but DOES expect a unique URL for the profile that needs to be displayed.
# # Returns an image file that corresponds to the user's profile picture. 
@weave_profile.route("/profile_picture/<username>", methods=["GET"])
def weave_profile_picture(username):
    
    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks if username exists in db and grabs relevant data
        cursor.execute("SELECT user_pic FROM UserAccount WHERE username = %s;", (username,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'User does not exist'}), 404

        # Returns each needed item in one JSON object
        filename = (cursor.fetchall())[0]["user_pic"]
        return send_file(str(current_app.config['UPLOAD_FOLDER']) + filename)


# # # # Backend code for editing profiles on Weave.
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Returns a JSON with JWT tokens and confirmation of the user's identity.
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"newusername\":\"newtestname\",\"firstname\":\"Bob\",\"lastname\":\"Banana\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"newtestname\",\"newusername\":\"testname\",\"firstname\":\"Banana\",\"lastname\":\"Bob\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
@weave_profile.route('/editprofile/', methods=["GET", "POST"])
@jwt_required
def weave_edit_profile():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # # # Validates JSON information.
        # Checks for JSON format. (Possibly change, this is how i got it to work with sending both an image and json data)
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'})
        mod_info = request.get_json()

        # Checks that the JSON has all elements.
        if ("newusername" not in mod_info or "firstname" not in mod_info or "lastname" not in mod_info or "biocontent" not in mod_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        mod_info["username"] = get_jwt_identity()
        # The original username should not need to be validated since it is not user input. (?)
        # If newusername is the same as the old one, then once again no validation needs to be done.
        # If there is a difference, however, then the new username needs to be checked for proper format.
        final_username = mod_info["username"]
        if (mod_info["username"] != mod_info["newusername"] and mod_info["newusername"] != ""):
            if (re.search("^[A-Za-z0-9_-]{6,20}$", mod_info["newusername"]) == None):
                return jsonify({'error_message': 'Your new username is invalid.'}), 400
            final_username = mod_info["newusername"]

        # There also cannot be repeated usernames, which should be checked for before we get a SQL error.
        username_query = "SELECT username from UserAccount WHERE username = \"" + mod_info["newusername"] + "\";"
        cursor.execute(username_query)
        for row in cursor:
            if (mod_info["username"] != mod_info["newusername"]) and (mod_info["newusername"] == row["username"]):
                return jsonify({'error_message': 'Your new username has already been taken.'}), 400

        # If the name elements of the JSON are not empty strings, they also need to be checked.
        # Only capitals, lowercases, numbers, and spaces should be allow in names. (Maybe single quotes too?)
        # There should also not be more than 15 characters in each.
        final_firstname = None
        if (mod_info["firstname"] != ""):
            if (re.search("^[A-Za-z0-9 ]{0,15}$", mod_info["firstname"]) == None):
                return jsonify({'error_message': 'Your name is invalid.'}), 400
            else:
                final_firstname = mod_info["firstname"]

        final_lastname = None
        if (mod_info["lastname"] != ""):
            if (re.search("^[A-Za-z0-9 ]{0,15}$", mod_info["lastname"]) == None):
                return jsonify({'error_message': 'Your name is invalid.'}), 400
            else:
                final_lastname = mod_info["lastname"]

        # All biocontent should be fine. Quote characters should be replaced during the cursor execution statement.
        # Not sure how this might affect length, however. Very specific edge case to test if we have time.
        final_biocontent = None
        if (mod_info["biocontent"] != ""):
            final_biocontent = mod_info["biocontent"]
        if (final_biocontent != None and len(final_biocontent) > 250):
            return jsonify({'error_message': 'Your biography is too long.'}), 400

        # # # End validation
        # Updates the database with the new information.
        mod_query = "UPDATE UserAccount SET username = %s, first_name = %s, last_name = %s, user_bio = %s WHERE username = %s;"
        mod_values = (final_username, final_firstname, final_lastname, final_biocontent, mod_info["username"])
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit()

        # Prints new database row for debugging
        # cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (mod_info["username"],))
        # print(cursor.fetchall())

        ret = {
            'access_token': create_access_token(identity=final_username),
            'refresh_token': create_refresh_token(identity=final_username),
            'username': final_username
        }
        return jsonify(ret), 200

    # Not a POST request.
    else:
        return "serve edit profile page"


# # # # Backend code for updating user profile images on Weave.
# # Expects a POST request with a header holding authorization and an attached image file.
# # Returns a JSON with confirmation of the user's identity.
@weave_profile.route('/editprofilepic/', methods=["GET", "POST"])
@jwt_required
def weave_edit_profile_pic():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Uploads a photo if attached
        new_filename = ""
        if 'image' in request.files:
            img_file = request.files['image']
            # Checks to make sure an image is attached.
            if img_file.filename != '':
                new_filename = secure_filename(img_file.filename)
                prefix = 0
                # Adjusts filename for duplicate names
                while (path.exists(str(current_app.config['UPLOAD_FOLDER']) + str(prefix) + str(new_filename))):
                    prefix += 1
                new_filename = str(prefix) + new_filename
                img_file.save(
                    str(current_app.config['UPLOAD_FOLDER']) + str(new_filename))
                # TODO: Make sure that the filename is not too long for the database

        # Grabbing identity of uploader
        identity = get_jwt_identity()

        # Putting file path into database for user
        mod_query = "UPDATE UserAccount SET user_pic = %s WHERE username = %s;"
        mod_values = (new_filename, identity)
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit()

        ret = {
            'username': identity
        }
        return jsonify(ret), 200
