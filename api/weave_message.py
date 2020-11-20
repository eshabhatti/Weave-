from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re
weave_message = Blueprint('weave_message', __name__)


# # # # Backend code for inserting direct messages into the database.
# # Expects a POST request that includes a JSON. Details are in 'api/README.md'.
# # Returns a JSON with a new set of JWT tokens along with confirmation of the user's identity.
@weave_message.route("/createmessage/", methods=["POST"])
@jwt_required
def weave_message_create():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        message_info = request.get_json()
        message_info["sender"] = get_jwt_identity()
        
        # Checks for all needed JSON elements.
        if ("sender" not in message_info or "receiver" not in message_info or "content" not in message_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
            
        # Checks for valid content length
        if (len(message_info["content"]) > 500 or len(message_info["content"]) == 0):
            return jsonify({'error_message': 'Invalid message body'}), 400

        # Caches the current date and time in the proper format.
        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        
        # Creates the new message ID based on the last one.
        message_id = 1
        cursor.execute("SELECT message_id FROM DirectMessage ORDER BY message_id DESC LIMIT 1;")
        for row in cursor:
            message_id = row["message_id"] + 1
        
        # Inserts the new message into the database.
        message_query = "INSERT INTO DirectMessage VALUES (%s, %s, %s, %s, %s, %s, %s);"
        message_values = (message_id, message_info["sender"], message_info["receiver"], 1, 2, message_info["content"], current_date)
        cursor.execute(message_query, message_values)
        mysql.connection.commit()
        
        # Returns a set of refreshed tokens. (May be able to remove later.)
        ret = {
            'access_token': create_access_token(identity=message_info["sender"]),
            'refresh_token': create_refresh_token(identity=message_info["sender"]),
            'username': message_info["sender"]
        }
        return jsonify(ret), 200



# # # # Backend code for displaying a user's direct messages on Weave.
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the direct messages made by a user within the specified range.
@weave_message.route("/allmessages/", methods=["POST"])
@jwt_required
def weave_render_messages():

    # The backend has recieved a request to display the user's direct messages.
    if request.method == "POST":

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
        message_query = "SELECT message_id FROM DirectMessage WHERE sender = %s OR receiver = %s" + \
            "ORDER BY date_created DESC " + \
            "LIMIT " + str(message_info["start"]) + ", " + str(message_info["end"]) + ";"
        message_values = (username, username)
        cursor.execute(message_query, message_values)

        # Adds the direct messages to a list that will then be returned.
        message_list = []
        for row in cursor:
            message_list.append(row["message_id"])
        #print(str(message_list)) #debugging

        # Returns the total count of direct messages.
        message_query = "SELECT COUNT(message_id) AS count FROM DirectMessage WHERE sender = %s OR receiver = %s;"
        message_values = (username, username)
        cursor.execute(message_query, message_values)
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'pull_list': message_list,
            'rowCount': count
        }
