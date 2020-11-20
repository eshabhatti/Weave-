from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

weave_block = Blueprint('weave_block', __name__)

# # # # Backend code for inserting blocking user info into the database.
# # Expects a BLOCK request that includes a JSON. Details are in 'api/README.md'.
# # Returns a JSON with a new set of JWT tokens along with confirmation of the user's identity.
@weave_block.route("/blockuser/", methods=["BLOCK"])
@jwt_required
def weave_block_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "BLOCK":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        block_info = request.get_json()
        block_info["user_blocker"] = get_jwt_identity()
        
        # Checks for all needed JSON elements.
        if ("user_blocker" not in block_info or "user_blocked" not in block_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        
        # Inserts the new block into the database.
        block_query = "INSERT INTO UserBlock VALUES (%s, %s);"
        block_values = (block_info["user_blocker"], block_info["user_blocked"])
        cursor.execute(block_query, block_values)
        mysql.connection.commit()
        
        # Returns a set of refreshed tokens.
        ret = {
            'access_token': create_access_token(identity=block_info["user_blocker"]),
            'refresh_token': create_refresh_token(identity=block_info["user_blocker"]),
            'username': block_info["user_blocker"]
        }
        return jsonify(ret), 200



# # # # Backend code for unblocking a user and removing blocking info from the database.
# # Expects a BLOCK request that includes a JSON. Details are in 'api/README.md'.
# # Returns a JSON with a new set of JWT tokens along with confirmation of the user's identity.
@weave_block.route("/unblockuser/", methods=["BLOCK"])
@jwt_required
def weave_unblock_user():
    
    # The backend has recieved information that needs to go into the database.
    if request.method == "BLOCK":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        block_info = request.get_json()
        block_info["user_blocker"] = get_jwt_identity()
        
        # Checks for all needed JSON elements.
        if ("user_blocker" not in block_info or "user_blocked" not in block_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        
        # Deletes information about the specific block from the database.

        block_query = "DELETE FROM UserBlock WHERE user_blocker = %s AND user_blocked = %s;"
        block_values = (block_info["user_blocker"], block_info["user_blocked"])
        cursor.execute(block_query, block_values)
        mysql.connection.commit()
        
        # Returns a set of refreshed tokens.
        ret = {
            'access_token': create_access_token(identity=block_info["user_blocker"]),
            'refresh_token': create_refresh_token(identity=block_info["user_blocker"]),
            'username': block_info["user_blocker"]
        }
        return jsonify(ret), 200