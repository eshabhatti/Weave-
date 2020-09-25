# # # # Backend code for EDITPROFILE requests.
# # Expects a POST request with a JSON formatted like: {"username":"[username]","newusername":"[newusername]","firstname":"[firstname]","lastname":"[lastname]","biocontent":"[biocontent]","profilepic":"[profilepic]"}
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"newusername\":\"newtestname\",\"firstname\":\"Bob\",\"lastname\":\"Banana\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"newtestname\",\"newusername\":\"testname\",\"firstname\":\"Banana\",\"lastname\":\"Bob\",\"biocontent\":\"Hi I am Bob, aren't I cool?\",\"profilepic\":\"\"}" http://localhost:5000/editprofile/
from flask import Blueprint, request, jsonify
from extensions import mysql
import re

weave_editprofile = Blueprint('weave_editprofile', __name__)

@weave_editprofile.route('/editprofile/', methods=["GET", "POST"])
def weave_edit_profile():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # # # Validates JSON information.
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'})  
        mod_info = request.get_json()

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

        # The image should be stored in a public folder, where the filepath is a hashed using the user id
        final_picpath = None
        if (mod_info["profilepic"] != ""):
            final_picpath = mod_info["profilepic"]

        # # # End validation
        # Updates the database with the new information.
        mod_query = "UPDATE UserAccount SET username = %s, first_name = %s, last_name = %s, user_bio = %s, user_pic = %s WHERE username = %s;"
        mod_values = (final_username, final_firstname, final_lastname, final_biocontent, final_picpath, mod_info["username"])
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit() 

        # Prints new database row for debugging
        cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (mod_info["newusername"],))
        print(cursor.fetchall())
        return "user has updated account"

    # Not a POST request.        
    else:
        return "serve edit profile page"
