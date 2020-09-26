# # # # # Backend code for Weave Profiles, that sends frontend
# # the appropriate data to display a users profile page.
#      

from flask import Blueprint, request, jsonify
from extensions import mysql

weave_profile = Blueprint('weave_profile', __name__)

@weave_profile.route("/profile/<username>", methods=["GET"])
# @login_required
def weave_profile_data(username):
    
    # The backend has received a profile GET request.
    if request.method == "GET":
    
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks if username exists in db (need to grab more things eventually)
        cursor.execute("SELECT username, user_bio, user_pic, follower_count FROM UserAccount WHERE username = %s;", (username,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'User does not exist'})
        # Returns each needed item in one JSON object
        return (cursor.fetchall())[0]
    