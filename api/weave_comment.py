from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from extensions import mysql
import re
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import json

weave_comment = Blueprint('weave_comment', __name__)

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
        
        if ("creator" not in comment_info or "content" not in comment_info or "post_id" not in comment_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
            
        if (len(comment_info["content"]) > 750 or len(comment_info["content"]) == 0):
            return jsonify({'error_message': 'Invalid Comment Body.'}), 400

        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        
        # Creating new comment id
        comment_id = 1
        id_query = "SELECT comment_id FROM PostComment ORDER BY comment_id DESC LIMIT 1;"
        cursor.execute(id_query)
        for row in cursor:
            comment_id = row["comment_id"] + 1
        
        # Insert new comment into the database.
        comment_query = "INSERT INTO PostComment VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        comment_values = (comment_id, comment_info["post_id"], comment_info["creator"], 0, current_date, comment_info["content"], 0, 0, 0)
        cursor.execute(comment_query, comment_values)
        mysql.connection.commit()
        
        # Return values
        ret = {
            'access_token': create_access_token(identity=comment_info["creator"]),
            'refresh_token': create_refresh_token(identity=comment_info["creator"]),
            'username': comment_info["creator"]
        }
        return jsonify(ret), 200

# # # # # Backend code for viewing comments
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

        # Returns post info as JSON object.
        return comment_info
        
# # # # # Backend code for pulling comments ids for a post
@weave_comment.route("/pullcomments/", methods=["POST"])
@jwt_required
def weave_comment_pull():

    # The backend has received a profile GET request.
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
        cursor.execute("SELECT post_id FROM POST WHERE post_id = %s;", (pull_info["post_id"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Post does not exist'}), 404
            
        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(pull_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(pull_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400
        
        # Pulls comment ids for specific post
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        pull_query = "SELECT comment_id FROM PostComment WHERE post_parent = \"" + \
            str(pull_info["post_id"]) + "\" ORDER BY comment_id DESC LIMIT " + \
            str(pull_info["start"]) + ", " + str(pull_info["end"]) + ";"
        cursor.execute(pull_query)

        # Adds the user's comments to a list that will then be returned.
        pull_list = []
        for row in cursor:
            pull_list.append(row["comment_id"])

        # Return as list
        return {'pull_list': pull_list}
