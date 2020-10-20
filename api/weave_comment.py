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