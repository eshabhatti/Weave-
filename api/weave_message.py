from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re
weave_message = Blueprint('weave_message', __name__)


# # # # Backend code for displaying a user's direct messages on Weave.
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the Directmessages made by a user within the specified range.
@weave_message.route("/message", methods=["MESSAGE"])
@jwt_required
def weave_render_messageList():

    # The backend has recieved a request to display the user's direct messages.
    if request.method == "message":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        message_info = request.get_json()

        # Checks for all needed JSON elements.
        if ("start" not in message_info or "end" not in message_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(message_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(message_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Grabs the identity of the user.
        username = get_jwt_identity()

        # This SQL statement will pull everything the we need from the database for direct messages display.
        # Not only is this thing long and ugly, but it is also insecure and requires the limits to be validated above. B)
        message_query = "SELECT message_id FROM Directmessage " + \
            "WHERE message_id IN ( SELECT message_id FROM Directmessage WHERE sender = %s ) " + \
            "ORDER BY date_created DESC " + \
            "LIMIT " + str(message_info["start"]) + ", " + str(message_info["end"]) + ";"
        message_values = (username)
        cursor.execute(message_query, message_values)

        # Adds the direct messages to a list that will then be returned.
        message_list = []
        for row in cursor:
            message_list.append(row["message_id"])
        #print(str(message_list)) #debugging

        # Returns the total count of direct messages.
        message_query = "SELECT COUNT(message_id) AS count FROM Directmessage " + \
            "WHERE message_id IN ( SELECT message_id FROM Directmessage WHERE sender = %s ) " + \
            "ORDER BY date_created DESC;"
        message_values = (username)
        cursor.execute(message_query, message_values)
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'pull_list': message_list,
            'rowCount': count
        }
