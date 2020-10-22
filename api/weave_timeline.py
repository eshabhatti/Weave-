from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re
weave_timeline = Blueprint('weave_timeline', __name__)

# # # # Backend code for displaying a user's timeline on Weave.
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the posts made by a user within the specified range.
@weave_timeline.route("/timeline", methods=["POST"])
@jwt_required
def weave_render_timeline():

    # The backend has recieved a request to display the user's timeline.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        timeline_info = request.get_json()

        # Checks for all needed JSON elements.
        if ("start" not in timeline_info or "end" not in timeline_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(timeline_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(timeline_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Grabs the identity of the user.
        username = get_jwt_identity()

        # This SQL statement will pull everything the we need from the database for timeline display.
        # Not only is this thing long and ugly, but it is also insecure and requires the limits to be validated above. B)
        # TODO: THIS SHOWS THE ANONYMOUS POSTS OF OTHER USERS AS WELL AS ONE'S OWN ANON POSTS.
        timeline_query = "SELECT post_id FROM Post WHERE creator = %s " + \
            "OR topic_name IN (SELECT topic_followed AS topic_name FROM FollowTopic WHERE user_follower = %s) " + \
            "OR creator IN (SELECT user_followed AS creator FROM FollowUser WHERE user_follower = %s) " + \
            "ORDER BY date_created DESC " + \
            "LIMIT " + str(timeline_info["start"]) + ", " + str(timeline_info["end"]) + ";"
        timeline_values = (username, username, username)
        cursor.execute(timeline_query, timeline_values)

        # Adds the timeline posts to a list that will then be returned.
        timeline_list = []
        for row in cursor:
            timeline_list.append(row["post_id"])
        print(timeline_list) #debugging

        # Return as list
        return {'timeline_list': timeline_list}


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
