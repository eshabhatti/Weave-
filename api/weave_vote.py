from flask import Blueprint, request, jsonify
from extensions import mysql

weave_vote = Blueprint('weave_vote', __name__)


# # # # Backend code for adding votes to posts (this should also scale to voting on comments)
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Like saving posts, this method assumes we can call routes without navigating to that page on the frontend.
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"type\":\"1\",\"id\":\"1\",\"vote\":\"1\"}" http://localhost:5000/vote/
@weave_vote.route("/vote/", methods=["POST"])
# @login_required
def weave_voting():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'})
        vote_info = request.get_json()
        print(vote_info) # debugging

        # Checks for all needed elements in the JSON.
        if ("username" not in vote_info or "id" not in vote_info or "type" not in vote_info or "vote" not in vote_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}) 

        # There should be no real need for validation since the frontend will send the JSON without user input.
        # The check for repeated votes will be done within the conditionals below because they need to be handled differently in each context.

        # Handles votes for posts.
        if (vote_info["type"] == "1"):

            # Adds an upvote to the post.
            if (vote_info["vote"] == "1"):

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
                    return "upvote recorded"

                # If there is a repeated vote, we need to see if the score is different.
                # If so, return an error. If not, delete the downvote and change to an upvote.
                else:
                    
                    # Gets old score.
                    oldvote = cursor.fetchall()
                    oldvote = (oldvote[0])["score"]

                    # If the old score was an upvote, we will not modify the post score.
                    if (oldvote == 1):
                        return jsonify({'error_message':'User has already upvoted this post.'})

                    # If the old score was a downvote, remove it and add an upvote instead.
                    else:

                        # Modifies the PostVote entity.
                        cursor.execute("UPDATE PostVote SET score = 1 WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                        # Removes downvote and adds upvote to the appropriate post.
                        cursor.execute("UPDATE Post SET downvote_count = downvote_count - 1, upvote_count = upvote_count + 1 WHERE post_id = %s;", (vote_info["id"],))

                        mysql.connection.commit()
                        return "upvote recorded"

            # Adds a downvote to the post.
            elif (vote_info["vote"] == "-1"):

                # Checks for repeated votes.
                cursor.execute("SELECT score FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
                
                # If there is no repeated vote, the new vote can just be added into the database.
                if (cursor.rowcount == 0):

                    # Adds the actual vote entity into the database.
                    vote_query = "INSERT INTO PostVote VALUES (%s, %s, %s);"
                    vote_values = (vote_info["username"], vote_info["id"], vote_info["vote"])
                    cursor.execute(vote_query, vote_values)

                    # Updates the post table with the upvote.
                    cursor.execute("UPDATE Post SET downvote_count = downvote_count + 1 WHERE post_id = %s;", (vote_info["id"],))
            
                    mysql.connection.commit()
                    return "downvote recorded"

                # If there is a repeated vote, we need to see if the score is different.
                # If so, return an error. If not, delete the upvote and change to a downvote.
                else: 

                    # Gets old score.
                    oldvote = cursor.fetchall()
                    oldvote = (oldvote[0])["score"]

                    # If the old score was an downvote, we will not modify the post score.
                    if (oldvote == -1):
                        return jsonify({'error_message':'User has already downvoted this post.'})

                    # If the old score was a downvote, remove it and add an upvote instead.
                    else:

                        # Modifies the PostVote entity.
                        cursor.execute("UPDATE PostVote SET score = -1 WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                        # Removes upvote and adds downvote to the appropriate post.
                        cursor.execute("UPDATE Post SET downvote_count = downvote_count + 1, upvote_count = upvote_count - 1 WHERE post_id = %s;", (vote_info["id"],))

                        mysql.connection.commit()
                        return "downvote recorded"

            # Removes a vote from the post.
            elif (vote_info["vote"] == "0"):

                # The backend needs to know whether the vote was up or down to update the Post table correctly.
                # So the first thing we do is pull the old vote entity out of the database.
                cursor.execute("SELECT score FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))
                if (cursor.rowcount == 0):
                    return jsonify({'error_message':'User has not voted on this post.'}) 
                oldvote = cursor.fetchall()
                oldvote = (oldvote[0])["score"]

                # Deletes the vote entity from the database.
                cursor.execute("DELETE FROM PostVote WHERE post_id = %s AND username = %s;", (vote_info["id"], vote_info["username"]))

                # If the old vote was an upvote, it must be removed.
                if (oldvote == 1):
                    cursor.execute("UPDATE Post SET upvote_count = upvote_count - 1 WHERE post_id = %s", (vote_info["id"]))

                # If the old vote was an downvote, it must be removed.
                else:
                    cursor.execute("UPDATE Post SET downvote_count = downvote_count - 1 WHERE post_id = %s", (vote_info["id"]))

                mysql.connection.commit()
                return "vote deleted" 

            # This should never happen. It catches bad vote errors. 
            else:
                return jsonify({'error_message':'Invalid vote score.'})

        # Handles votes for comments.
        elif (vote_info["type"] == "2"):
            return "not implemented yet"

        # This should never happen. It catches bad vote type errors.
        else:
            return jsonify({'error_message':'Invalid vote type.'})

    else:
        return jsonify({'error_message':'Not POST request.'})
