from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import bcrypt

weave_delete = Blueprint('weave_delete', __name__)


# # # # Backend code for account deletion.
# # Expects a POST request and a JWT token, along with the user's current password.
# # Returns JSON that tells whether the account was successfully deleted.
@weave_delete.route("/deleteaccount/", methods=["POST"])
@jwt_required
def weave_delete_account():
    
    print("HELLO EVERYONE") # DEBUGGING

    # The backend has received a POST request.
    if request.method == "POST":
        
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'})
        user_info = request.get_json()

        # Checks for password.
        if ("password" not in user_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Gets username in JSON format.
        user_info["username"] = get_jwt_identity()

        # Checks password before allowing the account to be deleted.
        cursor.execute("SELECT encrypted_password FROM UserAccount WHERE username = %s;", (user_info["username"],))
        correct_password = cursor.fetchall()[0]["encrypted_password"]
        attempted_password = user_info["password"]
        valid_password = bcrypt.checkpw(attempted_password.encode('utf8'), correct_password.encode('utf8')) 
        if (not valid_password):
            return jsonify({'error_message':'Password incorrect.'}), 401

        # Deletes post votes in database by user (does not change total count)
        post_vote_delete_query = 'DELETE from PostVote WHERE username = %s;'
        post_vote_delete_values = (user_info["username"],)
        
        # Deletes comment votes in database (does not change total counts)
        comment_vote_delete_query = 'DELETE from CommentVote WHERE username = %s;'
        comment_vote_delete_values = (user_info["username"],)        
        
        # Deletes following data in database
        user_follow_delete_query = 'DELETE from FollowUser WHERE user_follower = %s OR user_followed = %s;'
        user_follow_delete_values = (user_info["username"], user_info["username"])  

        # Deletes following data in database
        topic_follow_delete_query = 'DELETE from FollowTopic WHERE user_follower = %s;'
        topic_follow_delete_values = (user_info["username"],) 
        
        # Changes posts made by user to show DELETED as creator
        post_delete_query = 'UPDATE Post SET creator = "DELETED" WHERE creator = %s;'
        post_delete_values = (user_info["username"],)

        # Changes comments made by user to show DELETED as creator
        comment_delete_query = 'UPDATE PostComment SET user_parent = "DELETED" WHERE user_parent = %s;'
        comment_delete_values = (user_info["username"],)
        
        # Deletes account from database by setting username to DELETED
        delete_query = "DELETE FROM UserAccount WHERE username = %s;"
        delete_values = (user_info["username"],)

        cursor.execute(post_vote_delete_query, post_vote_delete_values)
        mysql.connection.commit()
  
        cursor.execute(comment_vote_delete_query, comment_vote_delete_values)
        mysql.connection.commit()

        cursor.execute(user_follow_delete_query, user_follow_delete_values)
        mysql.connection.commit()

        cursor.execute(topic_follow_delete_query, topic_follow_delete_values)
        mysql.connection.commit()
        
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

    else:
        return jsonify({'error_message': 'Request Error: Not POST Request'}), 400

 