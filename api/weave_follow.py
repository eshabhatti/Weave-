from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re

weave_post = Blueprint('weave_follow', __name__)

# # # # Backend route for allowing the user to follow a user on Weave.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a message of success as a string. 
@weave_timeline.route("/followuser", methods=["POST"])
@jwt_required
def weave_follow_user():

    # The backend has recieved a request to make one user follow another.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        follow_info = request.get_json()
        
        # Checks for all needed elements in the JSON.
        if ("following" not in follow_info or "type" not in follow_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Grabs the identity of both users.
        follower = get_jwt_identity()
        followed = follow_info["following"]
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Handles instances where a new follow instance is being created.
        if (follow_info["type"] == 1):
            
            # Inserts new relationship entity.
            follow_query = "INSERT INTO FollowUser VALUES (%s, %s);"
            follow_values = (follower, followed)
            cursor.execute(follow_query, follow_values)
            
            # Updates the followed user's follower count attribute.
            update_query = "UPDATE UserAccount SET follower_count = follower_count + 1 WHERE username = %s;"
            update_values = (followed,)
            cursor.execute(update_query, update_values)
            mysql.connection.commit()

        # Handles instances where a follow instance is being deleted.
        elif (follow_info["type"] == -1):
            
            # Deletes relationship entity.
            follow_query = "DELETE FROM FollowUser WHERE user_follower = %s AND user_followed = %s;"
            follow_values - (follower, followed)
            cursor.execute(follow_query, follow_values)
            
            # Updates the ex-followed user's follower count attribute.
            update_query = "UPDATE UserAccount SET follower_count = follower_count - 1 WHERE username = %s;"
            update_values = (followed,)
            cursor.execute(update_query, update_values)
            mysql.connection.commit()

        return "follow user done"


# # # # Backend route for allowing the user to follow a topic on Weave.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a message of success as a string. 
@weave_timeline.route("/followtopic", methods=["POST"])
@jwt_required
def weave_follow_topic():

    # The backend has recieved a request to make one user follow some topic.
    if request.method == "POST":
        
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        follow_info = request.get_json()
        
        # Checks for all needed elements in the JSON.
        if ("following" not in follow_info or "type" not in follow_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Grabs the identity of the user and the topic
        follower = get_jwt_identity()
        followed = follow_info["following"]

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Handles instances where a new follow instance is being created.
        if (follow_info["type"] == 1):
            
            # Inserts new relationship entity.
            follow_query = "INSERT INTO FollowTopic VALUES (%s, %s);"
            follow_values = (follower, followed)
            cursor.execute(follow_query, follow_values)
            
            # Updates the followed topic's follow count attribute.
            update_query = "UPDATE Topic SET follower_count = follower_count + 1 WHERE topic_name = %s;"
            update_values = (followed,)
            cursor.execute(update_query, update_values)
            
            # Commits database.
            mysql.connection.commit()

        # Handles instances where a follow instance is being deleted.
        elif (follow_info["type"] == -1):
            
            # Deletes the old relationship entity.
            follow_query = "DELETE FROM FollowTopic WHERE user_follower = %s AND topic_followed = %s;"
            follow_values - (follower, followed)
            cursor.execute(follow_query, follow_values)
            
            # Updates the ex-followed topic's follow count attribute.
            update_query = "UPDATE Topic SET follower_count = follower_count - 1 WHERE topic_name = %s;"
            update_values = (followed,)
            cursor.execute(update_query, update_values)
            
            # Commits database.
            mysql.connection.commit()

        return "follow topic done"

# # # # Backend route for allowing the user to unfollow a user on Weave.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a message of success as a string. 
@weave_follow.route("/unfollowuser/", methods=["POST"])
@jwt_required
def weave_unfollow_user():
    # The backend has received a profile POST request.
    if request.method == "POST":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()

        # Checks for all needed JSON elements.
        if ("username" not in pull_info or "user" not in pull_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

# # # # Backend route for allowing the user to unfollow a topic on Weave.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a message of success as a string. 
@weave_follow.route("/unfollowtopic/", methods=["POST"])
@jwt_required
def weave_unfollow_topic():
    # The backend has received a profile POST request.
    if request.method == "POST":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()

        # Checks for all needed JSON elements.
        if ("username" not in pull_info or "topic" not in pull_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400