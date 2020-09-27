from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import mysql

weave_post = Blueprint('weave_post', __name__)


# # # # # Backend code for creating posts on Weave.
# # Will save a post to the database -- a text post if the type is 1, a picture-caption post if the type is 2.
# # Eventually it may need to save a series of picture posts but let's not worry about that right now.
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"topic\":\"general\",\"type\":\"1\",\"title\":\"TESTPOST\",\"content\":\"hello hello hello hello\",\"picpath\":\"none\",\"anon\":\"0\"}" http://localhost:5000/createpost/
@weave_post.route("/createpost/", methods=["GET", "POST"])
# @login_required
def weave_post_create():

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    # Checks for JSON format.
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


# # # # # Backend code for viewing posts on Weave
# # DOES NOT expect a JSON but DOES expect a unique URL for the post that needs to be displayed.
@weave_post.route("/post/<post_id>", methods=["GET"])
def weave_post_data(post_id):
    
    # The backend has received a profile GET request.
    if request.method == "GET":
    
        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()
        
        # Checks if post exists in db
        cursor.execute("SELECT topic_name, date_created, post_type, title, content, pic_path, upvote_count, downvote_count, anon_flag FROM POST WHERE post_id = %s;", (post_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'User does not exist'})
        
        # Checks and updates return items if post is anonymous
        post_info = (cursor.fetchall())[0]
        if (post_info["anon_flag"] == True):
            post_info.pop("creator", None)
        post_info.pop("anon_flag", None)
        
        # Returns post info as JSON object
        return post_info


# @weave_post.route("/save/<post_id>", methods=["POST"])
# # @login_required
# def save_weave_post():
