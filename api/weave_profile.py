from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from os import path
import re
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import json
import bcrypt

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
            
        # Adds following count for profiles and topics
        cursor.execute("SELECT * FROM FollowUser WHERE user_follower = %s;", (username,))
        profile_data["following_count"] = cursor.rowcount
        cursor.execute("SELECT * FROM FollowTopic WHERE user_follower = %s;", (username,))
        profile_data["topic_count"] = cursor.rowcount
        
        # Checks if the current user is following the given user.
        follow_query = "SELECT * FROM FollowUser WHERE user_follower = %s AND user_followed = %s;"
        follow_values = (profile_data["username"], username)
        cursor.execute(follow_query, follow_values)
        if (cursor.rowcount > 0):
            profile_data["follow"] = 1
        else:
            profile_data["follow"] = 0
            
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
        if ("firstname" not in mod_info or "lastname" not in mod_info or "biocontent" not in mod_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        mod_info["username"] = get_jwt_identity()

        # Gets the current profile information to prevent overwriting.
        current_firstname = ""
        current_lastname = ""
        current_bio = ""
        current_query = "SELECT first_name, last_name, user_bio FROM UserAccount WHERE username = %s;"
        cursor.execute(current_query, (mod_info["username"],))
        for row in cursor:
            current_firstname = row["first_name"]
            current_lastname = row["last_name"]
            current_bio = row["user_bio"]

        # If the name elements of the JSON are not empty strings, they also need to be checked.
        # Only capitals, lowercases, numbers, and spaces should be allow in names. (Maybe single quotes too?)
        # There should also not be more than 15 characters in each.
        final_firstname = current_firstname
        if (mod_info["firstname"] != ""):
            if (re.search("^[A-Za-z0-9 ]{0,15}$", mod_info["firstname"]) == None):
                return jsonify({'error_message': 'Your name is invalid.'}), 400
            else:
                final_firstname = mod_info["firstname"]

        final_lastname = current_lastname
        if (mod_info["lastname"] != ""):
            if (re.search("^[A-Za-z0-9 ]{0,15}$", mod_info["lastname"]) == None):
                return jsonify({'error_message': 'Your name is invalid.'}), 400
            else:
                final_lastname = mod_info["lastname"]

        # All biocontent should be fine. Quote characters should be replaced during the cursor execution statement.
        # Not sure how this might affect length, however. Very specific edge case to test if we have time.
        final_biocontent = current_bio
        if (mod_info["biocontent"] != ""):
            final_biocontent = mod_info["biocontent"]
        if (final_biocontent != None and len(final_biocontent) > 250):
            return jsonify({'error_message': 'Your biography is too long.'}), 400

        # # # End validation
        # Updates the database with the new information.
        mod_query = "UPDATE UserAccount SET first_name = %s, last_name = %s, user_bio = %s WHERE username = %s;"
        mod_values = (final_firstname, final_lastname, final_biocontent, mod_info["username"])
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit()

        # Access token refresh isn't really needed anymore but I don't particularly want to change it.
        ret = {
            'access_token': create_access_token(identity=mod_info["username"]),
            'refresh_token': create_refresh_token(identity=mod_info["username"]),
            'username': mod_info["username"]
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
                if (len(new_filename) > 100):
                    return jsonify({'error_message': 'Image path too long'}), 400
                img_file.save(str(current_app.config['UPLOAD_FOLDER']) + str(new_filename))

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


# # # # Backend code for modifying senstive account information
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Returns a JSON with JWT tokens and confirmation of the user's identity.
@weave_profile.route('/editsettings/', methods=["POST"])
@jwt_required
def weave_update_settings():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'})
        settings_info = request.get_json()
        current_username = get_jwt_identity()

        # Checks that the JSON has the required element.
        if ("currentpass" not in settings_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Pulls the user's encrypted password out of the database and then validates it.
        cursor.execute("SELECT encrypted_password FROM UserAccount WHERE username = %s;", (current_username,))
        correct_password = cursor.fetchall()[0]["encrypted_password"]
        attempted_password = settings_info["currentpass"]
        valid_password = bcrypt.checkpw(attempted_password.encode('utf8'), correct_password.encode('utf8')) 
        if (not valid_password):
            return jsonify({'error_message':'Password incorrect.'}), 401

        # # # Allows the user to change their email.
        if ("newemail" in settings_info and settings_info["newemail"] != ""):

            # Verifies the new email's format.
            if (re.search("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$", settings_info["newemail"]) == None):
                return jsonify({'error_message':'Your email address is invalid.'}), 400  
            if (len(settings_info["newemail"]) > 50):
                return jsonify({'error_message':'Your email address is invalid.'}), 400

            # Checks for repeated email.
            cursor.execute("SELECT email FROM UserAccount WHERE email = %s;", (settings_info["newemail"],))
            if (cursor.rowcount != 0):
                return jsonify({'error_message':'This email has already been used.'}), 400

            # Updates the email column in the account entity.
            cursor.execute("UPDATE UserAccount SET email = %s WHERE username = %s;", (settings_info["newemail"], current_username))
            mysql.connection.commit()
        
        # # # Allows the user to change their password.
        if ("newpass" in settings_info and settings_info["newpass"] != ""):

            # Verifies the new password's format.
            if (re.search("[A-Z]", settings_info["newpass"]) == None):
                return jsonify({'error_message':'Passwords need an uppercase letter.'}), 400  
            if (re.search("[a-z]", settings_info["newpass"]) == None):
                return jsonify({'error_message':'Passwords need a lowercase letter.'}), 400
            if (re.search("[0-9]", settings_info["newpass"]) == None):
                return jsonify({'error_message':'Passwords need a number.'}), 400        
            if (re.search("^[A-Za-z0-9!@#$%&?<>-_+]{6,20}$", settings_info["newpass"]) == None):
                return jsonify({'error_message':'Your password has an invalid character.'}), 400

            # Encrypts the password for storage in the database.
            hash_password = bcrypt.hashpw(settings_info["newpass"].encode('utf8'), bcrypt.gensalt())

            # Updates the password column in the account entity.
            cursor.execute("UPDATE UserAccount SET encrypted_password = %s WHERE username = %s;", (hash_password, current_username))
            mysql.connection.commit()

        # # # Allows the user to change their usernames.
        if ("newusername" in settings_info and settings_info["newusername"] != ""):

            # Verifies the new username's format.
            if (re.search("^[A-Za-z0-9_-]{6,20}$", settings_info["newusername"]) == None):
                return jsonify({'error_message':'Your username is invalid.'}), 400

            # Checks for repeated username.
            cursor.execute("SELECT username FROM UserAccount WHERE username = %s;", (settings_info["newusername"],))
            if (cursor.rowcount != 0):
                return jsonify({'error_message':'This email has already been used.'}), 400              

            # Updates the username column in the account entity.
            cursor.execute("UPDATE UserAccount SET username = %s WHERE username = %s;", (settings_info["newusername"], current_username))
            mysql.connection.commit()

            # Updates the current username
            current_username = settings_info["newusername"]

        # # # Allows the user to update their privacy settings
        # This setting condition will likely always be met. Changes will be made based on existing data versus new data.
        if ("privacy" in settings_info):

            # Checks the old moderation status value.
            # A value of 0 means that privacy mode is currently off, while a value of 1 means that it is currently on.
            cursor.execute("SELECT moderation_status FROM UserAccount WHERE username = %s;", (current_username,))
            current_moderation = cursor.fetchall()[0]["moderation_status"]

            # Checks if this route actually needs to do anything.
            if (str(current_moderation) != str(settings_info["privacy"])):

                # Updates the database with the new privacy value.
                cursor.execute("UPDATE UserAccount SET moderation_status = %s WHERE username = %s;", (settings_info["privacy"], current_username))
                mysql.connection.commit()

        # # # Returns a new access token for the updated username.
        ret = {
            'access_token': create_access_token(identity=current_username),
            'refresh_token': create_refresh_token(identity=current_username),
            'username': current_username
        }
        return jsonify(ret), 200
        