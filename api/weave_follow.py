from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re

weave_follow = Blueprint('weave_follow', __name__)


# # # # Backend route for allowing the user to follow a user on Weave.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a message of success as a string. 
@weave_follow.route("/followuser/", methods=["POST"])
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

        # Initializes the return JSON.
        ret = {
            "followState": 0,
            "followCount": 0
        }

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

            # Updates the follow state.
            ret["followState"] = 1

        # Handles instances where a follow instance is being deleted.
        elif (follow_info["type"] == -1):
            
            # Deletes relationship entity.
            follow_query = "DELETE FROM FollowUser WHERE user_follower = %s AND user_followed = %s;"
            follow_values = (follower, followed)
            cursor.execute(follow_query, follow_values)
            
            # Updates the ex-followed user's follower count attribute.
            update_query = "UPDATE UserAccount SET follower_count = follower_count - 1 WHERE username = %s;"
            update_values = (followed,)
            cursor.execute(update_query, update_values)
            mysql.connection.commit()

            # Updates the follow state.
            ret["followState"] = 0

        # Gets the total number of followers for the user that is being followed.
        follow_query = "SELECT follower_count FROM UserAccount WHERE username = %s;"
        follow_values = (followed,)
        cursor.execute(follow_query, follow_values)
        ret["followCount"] = cursor.fetchall()[0]["follower_count"]

        return ret


# # # # Backend route for allowing the user to follow a topic on Weave.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a message of success as a string. 
@weave_follow.route("/followtopic/", methods=["POST"])
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

        # Initializes the return JSON.
        ret = {
            "followState": 0,
            "followCount": 0
        }

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

            # Updates the follow state.
            ret["followState"] = 1

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

            # Updates the follow state.
            ret["followState"] = 0
        
        # Gets the total number of followers for the topic that is being followed.
        follow_query = "SELECT follower_count FROM Topic WHERE topic_name = %s;"
        follow_values = (followed,)
        cursor.execute(follow_query, follow_values)
        ret["followCount"] = cursor.fetchall()[0]["follower_count"]
        
        return ret