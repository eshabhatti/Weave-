from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

weave_vote = Blueprint('weave_vote', __name__)
VOTE_ERROR = -50     # Essentially a constant that handles errors between functions.


# # # # Backend function that handles post voting on Weave.
# # This is not a route itself, but its parameter is the JSON information that is originally passed into weave_voting().
# # Returns an integer that will update the change field in the return JSON.
def weave_post_vote(vote_info):
    
    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    # # # Handles upvotes to posts.
    if (vote_info["vote"] == 1):

        # Checks for repeated votes.
        cursor.execute("SELECT score FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
        
        # If there is no repeated vote, the new vote can just be added into the database.
        if (cursor.rowcount == 0):

            # Adds the actual vote entity into the database.
            vote_query = "INSERT INTO PostVote VALUES (%s, %s, %s);"
            vote_values = (vote_info["username"], vote_info["id"], vote_info["vote"])
            cursor.execute(vote_query, vote_values)

            # Updates the post table with the upvote.
            cursor.execute("UPDATE Post SET upvote_count = upvote_count + 1 WHERE post_id = %s;", (vote_info["id"],))

            mysql.connection.commit()
            return 1

        # If there is a repeated vote, we need to see if the score is different.
        # If so, delete the downvote and change to an upvote. If not, delete the upvote completely.
        else:
            
            # Gets old score.
            oldvote = cursor.fetchall()
            oldvote = (oldvote[0])["score"]

            # If the old score was an upvote, we will delete it from the database.
            if (oldvote == 1):
                
                # Deletes the vote entity from the database.
                cursor.execute("DELETE FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
            
                # Removes upvote from the appropriate post.
                cursor.execute("UPDATE Post SET upvote_count = upvote_count - 1 WHERE post_id = %s", (vote_info["id"],))
                
                mysql.connection.commit()
                return 0

            # If the old score was a downvote, remove it and add an upvote instead.
            else:

                # Modifies the PostVote entity.
                cursor.execute("UPDATE PostVote SET score = 1 WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # Removes downvote and adds upvote to the appropriate post.
                cursor.execute("UPDATE Post SET downvote_count = downvote_count - 1, upvote_count = upvote_count + 1 WHERE post_id = %s;", (vote_info["id"],))

                mysql.connection.commit()
                return 1
    # # #

    # # # Handles downvotes to posts.
    elif (vote_info["vote"] == -1):

        # Checks for repeated votes.
        cursor.execute("SELECT score FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
        
        # If there is no repeated vote, the new vote can just be added into the database.
        if (cursor.rowcount == 0):

            # Adds the actual vote entity into the database.
            vote_query = "INSERT INTO PostVote VALUES (%s, %s, %s);"
            vote_values = (vote_info["username"], vote_info["id"], vote_info["vote"])
            cursor.execute(vote_query, vote_values)

            # Updates the post table with the downvote.
            cursor.execute("UPDATE Post SET downvote_count = downvote_count + 1 WHERE post_id = %s;", (vote_info["id"],))
    
            mysql.connection.commit()
            return -1

        # If there is a repeated vote, we need to see if the score is different.
        # If so, delete the upvote and change to a downvote. If not, remove the old vote from the database.
        else: 

            # Gets old score.
            oldvote = cursor.fetchall()
            oldvote = (oldvote[0])["score"]

            # If the old score was an downvote, we will remove it from the database.
            if (oldvote == -1):

                # Deletes the vote entity from the database.
                cursor.execute("DELETE FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # Removes the downvote from the post entity.
                cursor.execute("UPDATE Post SET downvote_count = downvote_count - 1 WHERE post_id = %s", (vote_info["id"],))

                mysql.connection.commit()
                return 0

            # If the old score was a upvote, remove it and add an downvote instead.
            else:

                # Modifies the PostVote entity.
                cursor.execute("UPDATE PostVote SET score = -1 WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # Removes downvote and adds upvote to the appropriate post.
                cursor.execute("UPDATE Post SET downvote_count = downvote_count + 1, upvote_count = upvote_count - 1 WHERE post_id = %s;", (vote_info["id"],))

                mysql.connection.commit()
                return -1
    # # #

    # # # This should never happen. It catches bad vote errors. 
    else:
        return VOTE_ERROR


# # # # Backend function that handles post voting on Weave.
# # This is not a route itself, but its parameter is the JSON information that is originally passed into weave_voting().
# # Returns an integer that will update the change field in the return JSON.
def weave_comment_vote(vote_info):

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    # # # Handles upvotes to comments.
    if (vote_info["vote"] == 1):

        # Checks for repeated votes.
        cursor.execute("SELECT score FROM CommentVote WHERE comment_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
        
        # If there is no repeated vote, the new vote can just be added into the database.
        if (cursor.rowcount == 0):

            # Adds the actual vote entity into the database.
            vote_query = "INSERT INTO CommentVote VALUES (%s, %s, %s);"
            vote_values = (vote_info["username"], vote_info["id"], vote_info["vote"])
            cursor.execute(vote_query, vote_values)

            # Updates the comment table with the upvote.
            cursor.execute("UPDATE PostComment SET upvote_count = upvote_count + 1 WHERE comment_id = %s;", (vote_info["id"],))

            mysql.connection.commit()
            return 1

        # If there is a repeated vote, we need to see if the score is different.
        # If so, delete the downvote and change to an upvote. If not, delete the upvote completely.
        else:
            
            # Gets old score.
            oldvote = cursor.fetchall()
            oldvote = (oldvote[0])["score"]

            # If the old score was an upvote, we will delete it from the database.
            if (oldvote == 1):
                
                # Deletes the CommentVote entity from the database.
                cursor.execute("DELETE FROM CommentVote WHERE comment_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
            
                # Removes upvote from the appropriate comment.
                cursor.execute("UPDATE PostComment SET upvote_count = upvote_count - 1 WHERE comment_id = %s", (vote_info["id"],))
                
                mysql.connection.commit()
                return 0

            # If the old score was a downvote, remove it and add an upvote instead.
            else:

                # Modifies the CommentVote entity.
                cursor.execute("UPDATE CommentVote SET score = 1 WHERE comment_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # Removes downvote and adds upvote to the appropriate comment.
                cursor.execute("UPDATE PostComment SET downvote_count = downvote_count - 1, upvote_count = upvote_count + 1 WHERE comment_id = %s;", (vote_info["id"],))

                mysql.connection.commit()
                return 1
    # # #

    # # # Handles downvotes to comments.
    elif (vote_info["vote"] == -1):

        # Checks for repeated votes.
        cursor.execute("SELECT score FROM CommentVote WHERE comment_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
        
        # If there is no repeated vote, the new vote can just be added into the database.
        if (cursor.rowcount == 0):

            # Adds the actual vote entity into the database.
            vote_query = "INSERT INTO CommentVote VALUES (%s, %s, %s);"
            vote_values = (vote_info["username"], vote_info["id"], vote_info["vote"])
            cursor.execute(vote_query, vote_values)

            # Updates the post table with the downvote.
            cursor.execute("UPDATE PostComment SET downvote_count = downvote_count + 1 WHERE comment_id = %s;", (vote_info["id"],))
    
            mysql.connection.commit()
            return -1

        # If there is a repeated vote, we need to see if the score is different.
        # If so, delete the upvote and change to a downvote. If not, remove the old vote from the database.
        else: 

            # Gets old score.
            oldvote = cursor.fetchall()
            oldvote = (oldvote[0])["score"]

            # If the old score was an downvote, we will remove it from the database.
            if (oldvote == -1):

                # Deletes the CommentVote entity from the database.
                cursor.execute("DELETE FROM CommentVote WHERE comment_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # Removes the downvote from the comment entity.
                cursor.execute("UPDATE PostComment SET downvote_count = downvote_count - 1 WHERE comment_id = %s", (vote_info["id"],))

                mysql.connection.commit()
                return 0

            # If the old score was a upvote, remove it and add an downvote instead.
            else:

                # Modifies the PostComment entity.
                cursor.execute("UPDATE CommentVote SET score = -1 WHERE comment_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # Removes downvote and adds upvote to the appropriate comment.
                cursor.execute("UPDATE PostComment SET downvote_count = downvote_count + 1, upvote_count = upvote_count - 1 WHERE comment_id = %s;", (vote_info["id"],))

                mysql.connection.commit()
                return -1
    # # #

    # # # This should never happen. It catches bad vote errors. 
    else:
        return VOTE_ERROR


# # # # Backend code for adding votes to posts and comments
# # Like saving posts, this method assumes we can call routes without navigating to that page on the frontend.
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Returns a JSON with a flag corresponding to how the vote has been changed. 
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/
@weave_vote.route("/vote/", methods=["POST"])
@jwt_required
def weave_voting():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":
        
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Initializes return values
        ret = {
            "voteState": 0,
            "score": 0
        }
        
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400
        vote_info = request.get_json()
        vote_info["username"] = get_jwt_identity()

        # Checks for all needed elements in the JSON.
        if ("username" not in vote_info or "id" not in vote_info or "type" not in vote_info or "vote" not in vote_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400

        # There should be no real need for validation since the frontend will send the JSON without user input.
        # The check for repeated votes will be done within the conditionals below because they need to be handled differently in each context.

        # # # Handles votes for posts.
        if (vote_info["type"] == "1"):

            # Modifies the vote table and post table separate from the main route.
            ret["voteState"] = weave_post_vote(vote_info)

            # Queries the database for the post's new score.
            vote_query = "SELECT upvote_count - downvote_count AS score FROM Post WHERE post_id = %s;"
            vote_values = (vote_info["id"],)
            ret["score"] = cursor.fetchall()[0]["score"]
            
            # Checks for errors and then returns.
            if ret["change"] == VOTE_ERROR:
                return jsonify({'error_message':'Bad vote score'}), 400
            else:
                return ret

        # # # Handles votes for comments.
        elif (vote_info["type"] == "2"):
            
            # Modifies the vote table and the comment table separate from the main route.
            ret["change"] = weave_comment_vote(vote_info)

            # Queries the database for the comment's new score.
            vote_query = "SELECT upvote_count - downvote_count AS score FROM PostComment WHERE comment_id = %s;"
            vote_values = (vote_info["id"],)
            ret["score"] = cursor.fetchall()[0]["score"]

            # Checks for errors and then returns.
            if ret["change"] == VOTE_ERROR:
                return jsonify({'error_message':'Bad vote score'}), 400
            else:
                return ret

        # # # This should never happen. It catches bad vote type errors.
        else:
            return jsonify({'error_message':'Invalid vote type.'}), 400

    else:
        return jsonify({'error_message':'Not POST request.'}), 400


