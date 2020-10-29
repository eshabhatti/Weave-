from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from werkzeug.utils import secure_filename
from os import path
import re

weave_delete = Blueprint('weave_delete', __name__)


# # # # Backend code for account deletion.
# # Expects a GET request and a JWT token.
# # Returns JSON that tells whether the account was successfully deleted.
@weave_delete.route("/deleteaccount/", methods=["GET"])
@jwt_required
def weave_delete_account():
    
    # The backend has received a DELETE request.
    if request.method == "GET":
        
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Gets username in JSON format.
        user_info = {"username" : get_jwt_identity()}

        # Changes posts made by user to show DELETED as creator
        post_delete_query = 'UPDATE post SET creator = "DELETED" WHERE creator = %s;'
        post_delete_values = (user_info["username"],)

        # Changes comments made by user to show DELETED as creator
        comment_delete_query = 'UPDATE postcomment SET user_parent = "DELETED" WHERE user_parent = %s;'
        comment_delete_values = (user_info["username"],)
        
        # Deletes account from database by setting username to DELETED
        delete_query = "DELETE FROM UserAccount WHERE username = %s;"
        delete_values = (user_info["username"],)

        cursor.execute(post_delete_query, post_delete_values)
        mysql.connection.commit()

        cursor.execute(comment_delete_query, comment_delete_values)
        mysql.connection.commit()
        
        cursor.execute(delete_query, delete_values)
        mysql.connection.commit()

        ret = {
            'account_deletion' : 'account successfully deleted',
            'username': user_info["username"]
        }
        return jsonify(ret), 200


 