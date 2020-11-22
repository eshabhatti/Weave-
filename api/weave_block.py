from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

weave_block = Blueprint('weave_block', __name__)


# # # # Backend code for checking if one user has blocked another.
# # This is NOT a route and thus cannot be called from the frontend. The backend will call this internally.
# # The first parameter ("current_username") represents the current active user.
# # The second parameter ("check_username") represents the user whose information the current user is trying to access.
# # Returns TRUE if "check_username" has blocked "current_username". Returns FALSE otherwise.
# # Call this function with the import line "from weave_block import weave_check_block".
def weave_check_block(current_username, check_username):

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    # Debugging statement
    # print("Current username == " + str(current_username))
    # print("Check username == " + str(check_username))

    # Function assumes that the usernames are passed in correctly. Validate usernames beforehand.
    # Checks if there exists a UserBlock entity where "check_username" has blocked "current_username".
    block_query = "SELECT * FROM UserBlock WHERE user_blocker = %s AND user_blocked = %s;"
    block_values = (check_username, current_username)
    cursor.execute(block_query, block_values)
    if (cursor.rowcount > 0):
        return True
    else:
        return False

# # # # Backend code for inserting blocking user info into the database.
# # Expects a POST request that includes a JSON. Details are in 'api/README.md'.
# # Returns a JSON with a new set of JWT tokens along with confirmation of the user's identity.
@weave_block.route("/blockuser/", methods=["POST"])
@jwt_required
def weave_block_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()
        
        # Initializes the return JSON.
        ret = {
            "blockState": 0,
        }

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        block_info = request.get_json()
        block_info["user_blocker"] = get_jwt_identity()
        
        # Checks for all needed JSON elements.
        if ("user_blocker" not in block_info or "user_blocked" not in block_info or "type" not in block_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
            
        # Handles instances where a new block instance is being created.
        if (block_info["type"] == 1):
            # Inserts the new block into the database.
            block_query = "INSERT INTO UserBlock VALUES (%s, %s);"
            block_values = (block_info["user_blocker"], block_info["user_blocked"])
            cursor.execute(block_query, block_values)
            mysql.connection.commit()
            
            ret["blockState"] = 1
        
        # Handles instances where a block instance is being deleted.
        elif (block_info["type"] == -1):
            # Deletes information about the specific block from the database.
            block_query = "DELETE FROM UserBlock WHERE user_blocker = %s AND user_blocked = %s;"
            block_values = (block_info["user_blocker"], block_info["user_blocked"])
            cursor.execute(block_query, block_values)
            mysql.connection.commit()   

            ret["blockState"] = 1
            
        return jsonify(ret), 200