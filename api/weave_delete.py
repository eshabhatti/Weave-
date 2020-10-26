from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from werkzeug.utils import secure_filename
from os import path
import re
weave_delete = Blueprint('weave_delete', __name__)


#Backend code for account deletion
#expects a JSON that contains a user's username to delete
#sets moderation status on account to 2 to indicate a deletion
#returns JSON that tells whether the account was successfully deleted

@weave_delete.route("/profile/<username>/", methods=["DELETE"])
@jwt_required
def weave_delete_account():
    
    # The backend has received a DELETE request.
    if request.method == "DELETE":
        
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        #checks for JSON format
        if (not request.is_json):
                return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        user_info = request.get_json()
        user_info["username"] = get_jwt_identity()


        # deletes account from database by setting username to DELETED
        delete_query = "UPDATE UserAccount SET moderation_status = %d WHERE username = %s;"
        delete_values = (1, user_info["username"])
        cursor.execute(delete_query, delete_values)
        mysql.connection.commit()
    

        ret = {
            'account_deletion' : 'account successfully deleted'
            'access_token': create_access_token(identity=user_info["username"]),
            'refresh_token': create_refresh_token(identity=user_info["username"]),
            'username': user_info["username"]
        }
        return jsonify(ret), 200


 