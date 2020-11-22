from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, jwt_optional
import re

weave_topic = Blueprint('weave_topic', __name__)

@weave_topic.route("/topic/<topic_name>", methods=["GET"])
@jwt_required
def weave_topic_data(topic_name):
    
    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks if topic exists in db and grabs relevant data
        cursor.execute("SELECT * FROM Topic WHERE topic_name = %s;", (topic_name,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Topic does not exist'}), 404

        # Returns each needed item in one JSON object
        topic_data = (cursor.fetchall())[0]
        topic_data["username"] = get_jwt_identity()
        
        # Checks if the current user is following the given topic.
        follow_query = "SELECT * FROM FollowTopic WHERE user_follower = %s AND topic_followed = %s;"
        follow_values = (topic_data["username"], topic_name)
        cursor.execute(follow_query, follow_values)
        if (cursor.rowcount > 0):
            topic_data["follow"] = 1
        else:
            topic_data["follow"] = 0
             
        return topic_data