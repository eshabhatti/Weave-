from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re

from weave_block import weave_check_block
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

        # Checks to make sure the sender is not blocked by the receiver.
        if (weave_check_block(current_username=message_info["sender"], check_username=message_info["receiver"]) == True):
            return jsonify({'error_message': 'Blocked from content'}), 403

        # Grabs the privacy mode flag (moderation_status) for the receiver.
        cursor.execute("SELECT moderation_status FROM UserAccount WHERE username = %s;", (message_info["receiver"],))
        message_info["privacy"] = cursor.fetchall()[0]["moderation_status"]
        
        # If the user has privacy mode on, the message can still be sent if the receiver is following the sender.
        if (message_info["privacy"] == 1):

            # Grabs the users who the receiver is following.
            cursor.execute("SELECT user_followed FROM UserFollow WHERE user_follower = %s;", (message_info["receiver"],))
            
            # Checks the list of users who the receiver is following for the sender
            privacy_bypass = False
            for row in cursor:
                if (row["user_followed"] == message_info["sender"]):
                    privacy_bypass = True
                    break
                
            if (privacy_bypass == False):
                return jsonify({'error_message':'Message cannot be sent'}), 403
            
        # Checks for valid content length.
        # Direct messages cannot be more than 500 characters and cannot be empty.
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
        
        # Returns a success message
        return "message sent"


# # # # Backend code for deleting a user's direct message on Weave.
# # Direct messages will be deleted per user rather than completely, at least for single calls to the route.
# # Expects a POST request with a JSON. Details will be in 'api/README.md'.
# # Returns a success message upon route completion. 
@weave_message.route("/deletemessage/", methods=["POST"])
@jwt_required
def weave_delete_message():

    # The backend has recieved a request to delete the user's direct messages.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        delete_info = request.get_json()
        delete_info["username"] = get_jwt_identity()

        # Checks for all needed JSON elements.
        if ("message_id" not in delete_info or "username" not in delete_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Allows us to check if the user who wants to delete the message is the sender or receiver.
        # This could maybe be done earlier and passed into the route by the frontend, but this will also work.
        cursor.execute("SELECT sender, receiver FROM DirectMessage WHERE message_id = %s;", (delete_info["message_id"],))
        message_info = cursor.fetchall()[0]
        
        # If the user is the sender of the message, we update the sender_status attribute.
        if (message_info["sender"] == delete_info["username"]):
            cursor.execute("UPDATE DirectMessage SET sender_status = 0 WHERE sender = %s;", (delete_info["username"],))
            mysql.connection.commit()
            return "sender message deleted"

        # If the user is the receiver of the message, we update the receiver_status attribute.
        if (message_info["receiver"] == delete_info["username"]):
            cursor.execute("UPDATE DirectMessage SET receiver_status = 0 WHERE receiver = %s;", (delete_info["username"],))
            mysql.connection.commit()
            return "receiver message deleted"

        # This should never happen. (Even if the message does not exist, the server will likely crash earlier on.)
        return jsonify({'error_message': 'Could not delete message'}), 400
        

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
        message_query = "SELECT message_id FROM DirectMessage " + \
            "WHERE (sender = %s AND NOT sender_status = 0) " + \
            "OR (receiver = %s AND NOT receiver_status = 0) " + \
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

# # # # # Backend code for viewing posts on Weave.
# # The frontend will need to make another call to /postimage/<post_id> to get any possible other image.
# # DOES NOT expect a JSON but DOES expect a unique URL for the post that needs to be displayed.
# # Returns a dictionary of post information including the topic, date created, title, content, image path, score, and creator.
@weave_message.route("/message/<message_id>/", methods=["GET"])
@jwt_required
def weave_post_data(message_id):

    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks if post exists in db and grabs relevant data.
        cursor.execute("SELECT sender, receiver, content, date_created FROM DirectMessage WHERE message_id = %s;", (message_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Message does not exist'}), 404

        message_info = (cursor.fetchall())[0]
        message_info["username"] = get_jwt_identity()
            
        #blocking code?

        # Returns post info as JSON object.
        return message_info