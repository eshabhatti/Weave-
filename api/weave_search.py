from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re
weave_search = Blueprint('weave_search', __name__)


# # # # Backend code for inserting direct messages into the database.
# # Expects a POST request that includes a JSON. Details are in 'api/README.md'.
# # Returns a JSON with a new set of JWT tokens along with confirmation of the user's identity.
@weave_search.route("/search/", methods=["POST"])
def weave_page_search():
    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()
        
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        search_info = request.get_json()
        search_info["username"] = get_jwt_identity()
        
        # Checks for all needed JSON elements.
        if ("search_string" not in search_info or "search_type" not in search_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        
        ret = {
            "success": 1,
        }
        
        if(search_info["search_type"] == "topics"):
            cursor.execute("SELECT * FROM Topic WHERE topic_name = %s;", (search_info["search_string"],))
            if (cursor.rowcount > 0):
                return jsonify(ret)
        # theres a better way to check, without grabbing stuff may want to do later
        if(search_info["search_type"] == "profiles"):
            cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (search_info["search_string"],))
            if (cursor.rowcount > 0):
                return jsonify(ret)
        
        return jsonify({'error_message': 'No Results.'}), 400        