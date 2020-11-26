from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from extensions import mysql
import re
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity, create_access_token, create_refresh_token
import json

from weave_block import weave_check_block
weave_comment = Blueprint('weave_comment', __name__)


# # # # Backend code for inserting comments into the database.
# # Expects a POST request that includes a JSON. Details are in 'api/README.md'.
# # Returns a JSON with a new set of JWT tokens along with confirmation of the user's identity.
@weave_comment.route("/createcomment/", methods=["POST"])
@jwt_required
def weave_comment_create():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        comment_info = request.get_json()
        comment_info["creator"] = get_jwt_identity()
        
        # Checks for all needed JSON elements.
        if ("creator" not in comment_info or "content" not in comment_info or "post_id" not in comment_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
            
        # Checks for valid content length
        if (len(comment_info["content"]) > 400 or len(comment_info["content"]) == 0):
            return jsonify({'error_message': 'Invalid Comment Body.'}), 400

        # Caches the current date and time in the proper format.
        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        
        # Creates the new comment ID based on the last one.
        comment_id = 1
        id_query = "SELECT comment_id FROM PostComment ORDER BY comment_id DESC LIMIT 1;"
        cursor.execute(id_query)
        for row in cursor:
            comment_id = row["comment_id"] + 1
        
        # Inserts the new comment into the database.
        comment_query = "INSERT INTO PostComment VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        comment_values = (comment_id, comment_info["post_id"], comment_info["creator"], 0, current_date, comment_info["content"], 0, 0, 0)
        cursor.execute(comment_query, comment_values)
        mysql.connection.commit()
        
        # Returns a set of refreshed tokens.
        ret = {
            'access_token': create_access_token(identity=comment_info["creator"]),
            'refresh_token': create_refresh_token(identity=comment_info["creator"]),
            'username': comment_info["creator"]
        }
        return jsonify(ret), 200


# # # # Backend code for viewing comments on Weave.
# # Expects a GET request on a unique URL.
# # Returns the comment information as a JSON object.
@weave_comment.route("/comment/<comment_id>", methods=["GET"])
@jwt_required
def weave_comment_data(comment_id):

    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks if comment exists in db and grabs relevant data.
        cursor.execute("SELECT * FROM POSTCOMMENT WHERE comment_id = %s;", (comment_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Comment does not exist'}), 404

        # Gets comment info from db result
        comment_info = (cursor.fetchall())[0]

        # Adds identity of requester to the JSON.
        comment_info["username"] = get_jwt_identity()

        # Checks if the comment creator has blocked the active username and returns a fake comment if so.
        if (weave_check_block(current_username=comment_info["username"], check_username=comment_info["user_parent"]) == True):
            ret = {
                "comment_id": comment_info["comment_id"],
                "post_parent": comment_info["post_parent"],
                "user_parent": "BLOCKED",
                "comment_parent": comment_info["comment_parent"],
                "date_created": comment_info["date_created"],
                "content": "You have been blocked from viewing this comment.",
                "username": comment_info["username"],
            }
            return jsonify(ret), 403

        # Calculates score for the comment.
        comment_info["score"] = comment_info["upvote_count"] - comment_info["downvote_count"]

        # Returns post info as JSON object.
        return comment_info


# # # # Backend code for pulling comments IDs for a post.
# # Expects a POST request with a JSON. Details are in 'api/README.md'. 
# # Returns a list of comments that belong to a certain post.
@weave_comment.route("/postcomments/", methods=["POST"])
@jwt_required
def weave_comment_pull():

    # The backend has received a profile POST request.
    if request.method == "POST":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()
        
        # Checks for all needed JSON elements.
        if ("post_id" not in pull_info or "start" not in pull_info or "end" not in pull_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        
        # Checks if post exists in db and grabs relevant data.
        cursor.execute("SELECT post_id from Post WHERE post_id = %s;", (pull_info["post_id"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Post does not exist'}), 404
            
        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(pull_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(pull_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400
        
        # Pulls comment ids for a specific post.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        pull_query = "SELECT comment_id FROM PostComment WHERE post_parent = \"" + \
            str(pull_info["post_id"]) + "\" ORDER BY upvote_count - downvote_count DESC LIMIT " + \
            str(pull_info["start"]) + ", " + str(pull_info["end"]) + ";"
        cursor.execute(pull_query)

        # Adds the user's comments to a list that will then be returned.
        pull_list = []
        for row in cursor:
            pull_list.append(row["comment_id"])

        # Pulls the count of all the comments of the post.
        count_query = "SELECT COUNT(comment_id) AS count FROM PostComment WHERE post_parent = %s;"
        cursor.execute(count_query, (pull_info["post_id"],))
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'pull_list': pull_list,
            'rowCount': count
        }


# # # # Backend code for pulling comments IDs for a user
# # This will show on a users "interactions" feed
# # Expects a POST request with a JSON. Details are in 'api/README.md'.
# # Returns a list of comments that are attached to the specified user.
@weave_comment.route("/usercomments/", methods=["POST"])
def weave_user_comment_pull():

    # The backend has received a profile POST request.
    if request.method == "POST":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()
        
        # Checks for all needed JSON elements.
        if ("username" not in pull_info or "start" not in pull_info or "end" not in pull_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        
        # Checks if user exists in db and grabs relevant data.
        cursor.execute("SELECT username FROM UserAccount WHERE username = %s;", (pull_info["username"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Post does not exist'}), 404
        
        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(pull_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(pull_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400
        
        # Pulls comment ids for specific user.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        pull_query = "SELECT comment_id FROM PostComment WHERE user_parent = \"" + \
            str(pull_info["username"]) + "\" ORDER BY upvote_count - downvote_count DESC LIMIT " + \
            str(pull_info["start"]) + ", " + str(pull_info["end"]) + ";"
        cursor.execute(pull_query)

        # Adds the user's comments to a list that will then be returned.
        pull_list = []
        for row in cursor:
            pull_list.append(row["comment_id"])

        # Pulls the count of all the comments of the user.
        count_query = "SELECT COUNT(comment_id) AS count FROM PostComment WHERE user_parent = %s;"
        cursor.execute(count_query, (pull_info["username"],))
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'pull_list': pull_list,
            'rowCount': count
        }



# # # # Backend code for getting a post's special qualities according to a specific user.
# # Expects a JSON with details defined in "api/README.md".
# # Returns a JSON that defines whether a comment has been voted on by the user passed.
@weave_comment.route("/commentstates/", methods=["POST"])
@jwt_required
def weave_comment_state():
    
    # The backend has received a post state POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Initializes post state variables.
        voted = 0

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        comment_info = request.get_json()
        comment_info["username"] = get_jwt_identity()

        # Checks that JSON has all needed elements.
        if ("username" not in comment_info or "comment_id" not in comment_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Checks if post is upvoted/downvoted.
        vote_query = "SELECT score FROM CommentVote WHERE username = %s and comment_id = %s;"
        vote_values = (comment_info["username"], comment_info["comment_id"])
        cursor.execute(vote_query, vote_values)
        if (cursor.rowcount > 0):
            voted = (cursor.fetchall())[0]["score"]

        # Returns states
        ret_states = {
            "voted": voted
        }
        print(ret_states)
        return jsonify(ret_states)

