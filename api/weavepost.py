# # # # # Backend code for Weave CREATEPOST requests
# # Will save a post to the database -- a text post if the type is 1, a picture-caption post if the type is 2
# # Eventually it may need to save a series of picture posts but let's not worry about that right now.
# # Note that a post is anonymous if the anon flag is set to 1. It should be set to zero otherwise.
# # Expects JSON of {"username":"[username]","topic":"[topic]","type":"[post-type]","title":"[title]","content":"[content]","picpath":"[picpath]","anon":"[anon]"}
# # Test on Windows with the following curl script:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"topic\":\"general\",\"type\":\"1\",\"title\":\"TESTPOST\",\"content\":\"hello hello hello hello\",\"picpath\":\"none\",\"anon\":\"0\"}" http://localhost:5000/createpost/
from datetime import datetime
from flask import Blueprint, request
from extensions import mysql

weave_post = Blueprint('weave_post', __name__)

@weave_post.route("/createpost/", methods=["GET", "POST"])
# @login_required
def weave_post_create():

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    #Checks for JSON format.
    if (not request.is_json):
        return "{\"error_message\":\"not_JSON\"}"
    post_info = request.get_json()

    # This horrific thing checks that the JSON has all the needed elements.
    if ("username" not in post_info or "topic" not in post_info or "type" not in post_info or "title" not in post_info or "content" not in post_info or "picpath" not in post_info or "anon" not in post_info):
        return "{\"error_message\":\"missing_element\"}"

    # Don't have to validate the username because the frontend should send us it directly. (?)
    # May want to validate anon flag for safety, even though the backend will always send it to us without user input. (?)
    # Topic stuff is not implemented in this sprint, but when it IS implemented there will need to be more stuff here.

    # Validates the content information.
    # Most strings will be fine. However, any \" phrase must be replaced with \\\".
    post_info["content"].replace("\\\"", "\\\\\\\"")

    # I have no idea how image pathing is going to work right now. Does the filepath even need to be validated?
    # In any case, there's no point doing that unless the post is picture-caption, so we check for post type below first.
    
    # # # Post is text.
    if (post_info["type"] == "1"):
        
        # Assigns the Post a new post_id by querying the most recent post and then adding one.
        # The post_id is initialized to 1 because the first query should not return any posts.
        post_id = 1 
        id_query = "SELECT post_id FROM Post ORDER BY date_created DESC LIMIT 1;"
        cursor.execute(id_query)
        for row in cursor:
            post_id = row["post_id"] + 1

        # Gets the current date in "YYYY-MM-DD" format.
        current_date = datetime.today().strftime("%Y-%m-%d")

        # Insert new text post into the database.
        post_query = "INSERT INTO Post VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        post_values = (post_id, post_info["topic"], post_info["username"], current_date, post_info["type"], post_info["title"], post_info["content"], None, 0, 0, post_info["anon"], 0)
        cursor.execute(post_query, post_values)
        mysql.connection.commit()   

        return "user has made a post"

    # # # Post is picture-caption
    else:
        print("picture-caption post")
        # Validate picture path?
        # Do other stuff
        return "Error: Not implemented yet"

