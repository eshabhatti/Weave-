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

        # Modifies post scores by removing the user's votes.
        cursor.execute("SELECT * FROM PostVote WHERE username = %s;", (user_info["username"],))
        score_reset_list = cursor.fetchall()
        for row in score_reset_list:
            if (row["score"] == 1):
                cursor.execute("UPDATE Post SET upvote_count = upvote_count - 1 WHERE post_id = %s;", (row["post_id"],))
            elif (row["score"] == -1):
                cursor.execute("UPDATE Post SET downvote_count = downvote_count - 1 WHERE post_id = %s;", (row["post_id"],))
            else:
                return jsonify({'error_message': 'Request Error: Bad Score'}), 400
            mysql.connection.commit()

        # Modifies comment scores by removing the user's votes.
        cursor.execute("SELECT * FROM CommentVote WHERE username = %s;", (user_info["username"],))
        score_reset_list = cursor.fetchall()
        for row in score_reset_list:
            if (row["score"] == 1):
                cursor.execute("UPDATE PostComment SET upvote_count = upvote_count - 1 WHERE comment_id = %s;", (row["comment_id"],))
            elif (row["score"] == -1):
                cursor.execute("UPDATE PostComment SET downvote_count = downvote_count - 1 WHERE comment_id = %s;", (row["comment_id"],))
            else:
                return jsonify({'error_message': 'Request Error: Bad Score'}), 400
            mysql.connection.commit()

        # Modifies the follower_count column for users who have been followed by the deleted user.
        # Following counts do not need to be modified since they are determined directly be entities in the database.
        cursor.execute("SELECT * FROM FollowUser WHERE user_follower = %s;", (user_info["username"],))
        follower_reset_list = cursor.fetchall()
        for row in follower_reset_list:
            cursor.execute("UPDATE UserAccount SET follower_count = follower_count - 1 WHERE username = %s;", (row["user_followed"],))
            mysql.connection.commit()

        # Modifies the follower_count column for topics who have been followed by the deleted user.
        # Following counts do not need to be modified since they are determined directly be entities in the database.
        cursor.execute("SELECT * FROM FollowTopic WHERE user_follower = %s;", (user_info["username"],))
        follower_reset_list = cursor.fetchall()
        for row in follower_reset_list:
            cursor.execute("UPDATE Topic SET follower_count = follower_count - 1 WHERE topic_name = %s;", (row["topic_followed"],))
            mysql.connection.commit()
        
        # Changes posts made by user to show DELETED as creator
        post_delete_query = 'UPDATE Post SET creator = "DELETED" WHERE creator = %s;'
        post_delete_values = (user_info["username"],)

        # Changes comments made by user to show DELETED as creator
        comment_delete_query = 'UPDATE PostComment SET user_parent = "DELETED" WHERE user_parent = %s;'
        comment_delete_values = (user_info["username"],)
        
        # Deletes account from database by setting username to DELETED
        delete_query = "DELETE FROM UserAccount WHERE username = %s;"
        delete_values = (user_info["username"],)

        # Other entities that need to be deleted, including votes and follows, will be deleted by the database cascade.
        # Initiaizes account removal from the database.
        cursor.execute(post_delete_query, post_delete_values)
        cursor.execute(comment_delete_query, comment_delete_values)
        cursor.execute(delete_query, delete_values)
        mysql.connection.commit()

        ret = {
            'account_deletion' : 'account successfully deleted',
            'username': user_info["username"]
        }
        return jsonify(ret), 200

    else:
        return jsonify({'error_message': 'Request Error: Not POST Request'}), 400

 