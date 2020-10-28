from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from werkzeug.utils import secure_filename
from os import path
import re
weave_post = Blueprint('weave_post', __name__)


# # # # # Backend code for creating posts on Weave.
# # Will save a "text post" to the database. If the post has a picture component, another server request will be needed.
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Returns a JSON with JWT tokens and confirmation of the user's identity.
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"topic\":\"general\",\"title\":\"TESTPOST\",\"content\":\"hello hello hello hello\",\"anon\":\"0\"}" http://localhost:5000/createpost/
@weave_post.route("/createpost/", methods=["GET", "POST"])
@jwt_required
def weave_post_create():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        post_info = request.get_json()
        post_info["username"] = get_jwt_identity()

        # This horrific thing checks that the JSON has all the needed elements.
        if ("username" not in post_info or "topic" not in post_info or "title" not in post_info or "content" not in post_info or "anon" not in post_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # The username does not need to be validated here because it's passed through JWT. 
        # The anonymous flag should not ever give an error because it's sent from the server directly.
        
        # Validates the title information.
        # Most strings will be fine. Empty strings are not allowed; however, this should be caught by the frontend.
        # Any single or double quote in strings will be taken care of as part of the cursor's execute method.
        if (len(post_info["title"]) > 100):
            return jsonify({'error_message': 'Title too long.'}), 400

        # Validates the content information.
        # Most strings will be fine. Empty content (currently not be possible) will be saved as an empty string.
        # Any single or double quote in strings will be taken care of as part of the cursor's execute method.
        if (len(post_info["content"]) > 750):
            return jsonify({'error_message': 'Post too large.'}), 400
        if (len(post_info["content"]) < 1):
            return jsonify({'error_message': 'Empty posts are not allowed.'}), 400

            
        # Validates the topic information.
        # Most strings will be fine. Empty content will be changed to the topic "general"
        # Any single or double quote in strings will be taken care of as part of the cursor's execute method.
        if (len(post_info["topic"]) > 50):
            return jsonify({'error_message': 'Topic too large.'}), 400
        if (re.search("^[A-Za-z0-9]*$", post_info["topic"]) == None):
            return jsonify({'error_message': 'Topic name invalid.'}), 400
        if (post_info["topic"] == ""):
            post_info["topic"] = "general"

        # Gets the current date in "YYYY-MM-DD HH:MI:SS" format.
        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        # Checks if topic exists in database. If not, the topic is added in all lowercase.
        cursor.execute("SELECT * FROM Topic WHERE topic_name = %s;", (post_info["topic"],))
        if (cursor.rowcount == 0):
            topic_query = "INSERT INTO Topic VALUES (%s, %s, %s, %s);"
            topic_values = (post_info["topic"].lower(), current_date, 0, 0)
            cursor.execute(topic_query, topic_values)
            mysql.connection.commit()
        
        # Assigns the Post a new post_id by querying the most recent post and then adding one.
        # The post_id is initialized to 1 because the first query should not return any posts.
        post_id = 1
        id_query = "SELECT post_id FROM Post ORDER BY post_id DESC LIMIT 1;"
        cursor.execute(id_query)
        for row in cursor:
            post_id = row["post_id"] + 1

        # Insert new text post into the database.
        post_query = "INSERT INTO Post VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        post_values = (post_id, post_info["topic"], post_info["username"], current_date, post_info["title"], post_info["content"], None, 0, 0, post_info["anon"], 0)
        cursor.execute(post_query, post_values)
        mysql.connection.commit()

        ret = {
            'access_token': create_access_token(identity=post_info["username"]),
            'refresh_token': create_refresh_token(identity=post_info["username"]),
            'username': post_info["username"]
        }
        return jsonify(ret), 200


# # # # Backend code for uploading post images on Weave.
# # Will save the picture image of a picture-caption post to the database.
# # Expects a POST request with a header holding authorization and an attached image file.
# # Returns a string confirmation of the image creation.
@weave_post.route("/createimage/", methods=["GET", "POST"])
@jwt_required
def weave_post_upload_image():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Uploads a photo if attached.
        new_filename = ""
        if 'image' in request.files:
            img_file = request.files['image']
            # Checks to make sure an image is attached.
            if img_file.filename != '':
                new_filename = secure_filename(img_file.filename)
                prefix = 0
                # Adjusts filename for duplicate names.
                while (path.exists(str(current_app.config['UPLOAD_FOLDER']) + str(prefix) + str(new_filename))):
                    prefix += 1
                new_filename = str(prefix) + new_filename
                if (len(new_filename) > 100):
                    return jsonify({'error_message': 'Image path too long'}), 400
                img_file.save(str(current_app.config['UPLOAD_FOLDER']) + str(new_filename))
            else:
                return "no content"

        # Grabbing identity of uploader.
        identity = get_jwt_identity()

        # Putting file path into database for user's most recent post.
        # This should work as long as the database doesn't miss a request for some reason.
        # TO-DO: ensure this is added on the right post
        mod_query = "UPDATE Post SET pic_path = %s WHERE creator = %s ORDER BY post_id DESC LIMIT 1;"
        mod_values = (new_filename, identity)
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit()
        return "user has added post picture"


# # # # # Backend code for viewing posts on Weave.
# # The frontend will need to make another call to /postimage/<post_id> to get any possible other image.
# # DOES NOT expect a JSON but DOES expect a unique URL for the post that needs to be displayed.
# # Returns a dictionary of post information including the topic, date created, title, content, image path, score, and creator.
@weave_post.route("/post/<post_id>", methods=["GET"])
@jwt_required
def weave_post_data(post_id):

    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks if post exists in db and grabs relevant data.
        cursor.execute("SELECT topic_name, date_created, title, content, upvote_count, downvote_count, anon_flag, creator, pic_path FROM POST WHERE post_id = %s;", (post_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Post does not exist'}), 404

        # Checks and updates return items if post is anonymous.
        post_info = (cursor.fetchall())[0]
        print(post_info)
        if (post_info["anon_flag"] == 1):
            post_info["creator"] = "anonymous"
        post_info.pop("anon_flag", None)

        # Adds identity of requester to the JSON.
        post_info["username"] = get_jwt_identity()
        if (post_info["pic_path"] is not None):
            post_info["pic_path"] = "http://localhost:5000/postimage/"+str(post_id)

        # Adds easily computed score to the JSON.
        post_info["score"] = post_info["upvote_count"] - post_info["downvote_count"]

        # Returns post info as JSON object.
        return post_info


# # # # Backend code for getting a post's special qualities according to a specific user.
# # Expects a JSON with details defined in "api/README.md".
# # Returns a JSON  that defines whether a post has been saved and/or voted on by the user passed.
@weave_post.route("/poststates/", methods=["POST"])
@jwt_required
def weave_post_state():
    
    # The backend has received a post state POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Initializes post state variables.
        saved = 0
        voted = 0

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        post_info = request.get_json()
        post_info["username"] = get_jwt_identity()

        # Checks that JSON has all needed elements.
        if ("username" not in post_info or "post_id" not in post_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Checks if post is upvoted/downvoted.
        vote_query = "SELECT score FROM PostVote WHERE username = %s and post_id = %s;"
        vote_values = (post_info["username"], post_info["post_id"])
        cursor.execute(vote_query, vote_values)
        if (cursor.rowcount > 0):
            voted = (cursor.fetchall())[0]["score"]

        # Checks if post is saved or not.
        save_query = "SELECT * FROM SavedPost WHERE username = %s and post_id = %s;"
        save_values = (post_info["username"], post_info["post_id"])
        cursor.execute(save_query, save_values)
        if (cursor.rowcount > 0):
            saved = 1
        else:
            saved = -1

        # Returns states
        ret_states = {
            "saved": saved,
            "voted": voted
        }
        print(ret_states)
        return jsonify(ret_states)


# # # # Backend code for a pulling a single post's image.
# # This route will likely have to be called without explicitly navigating to this URL.
# # DOES NOT expect a JSON but DOES expect a unique URL for the post that needs to be displayed.
# # Returns an image file if the post has a picture; returns empty otherwise.
@weave_post.route("/postimage/<post_id>", methods=["GET"])
def weave_post_image(post_id):

    # The backend has received a profile GET request.
    if request.method == "GET":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks if post exists in db; may not need to be done if we know the post data route is visited first.
        cursor.execute("SELECT pic_path FROM POST WHERE post_id = %s;", (post_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Post does not exist'}), 404

        # Pulls the picture path out of the cursor.
        filename = cursor.fetchall()[0]["pic_path"]
        if (filename != ""):
            # Sends the file back to the frontend.
            # Media file type detection should work automatically but may need to be updated if not.
            print('"' + filename + '"')
            print('HERE ' + str(current_app.config['UPLOAD_FOLDER']) + filename)
            return send_file(str(current_app.config['UPLOAD_FOLDER']) + filename)
        else:
            return {}


# # # # Backend code for pulling a user's posts on Weave
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the posts made by a user within the specified range.
@weave_post.route("/userposts/", methods=["POST"])
@jwt_required
def weave_pull_userposts():

    # The backend has received a saved post POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()

        # Checks for all needed JSON elements.
        if ("username" not in pull_info or "start" not in pull_info or "end" not in pull_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Checks if username exists in database.
        cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (pull_info["username"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'User does not exist'}), 404
        cursor.fetchall()

        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(pull_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(pull_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400

        # Pulls the user's most recent posts as specified by the range.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        pull_query = "SELECT post_id FROM Post WHERE creator = \"" + \
            pull_info["username"] + "\" AND anon_flag = 0 ORDER BY post_id DESC LIMIT " + \
            str(pull_info["start"]) + ", " + str(pull_info["end"]) + ";"
        cursor.execute(pull_query)

        # Adds the user's posts to a list that will then be returned.
        pull_list = []
        for row in cursor:
            pull_list.append(row["post_id"])

        # Pulls the count of all the posts that the user made.
        count_query = "SELECT COUNT(post_id) AS count FROM Post WHERE creator = %s;"
        cursor.execute(count_query, (pull_info["username"],))
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'pull_list': pull_list,
            'rowCount': count
        }


# # # # Backend code for saving posts on Weave
# # Doesn't expect a unique URL right now, but this may be changed later.
# # Does expect a POST request along with a JSON. Details will be in "/api/README.md".
# # Returns confirmation of success as a string.
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"realuser1\",\"post\":\"4\",\"type\":\"1\"}" http://localhost:5000/save/
@weave_post.route("/save/", methods=["POST"])
@jwt_required
def save_weave_post():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        save_info = request.get_json()
        save_info["username"] = get_jwt_identity();

        # Checks for all needed elements in the JSON.
        if ("username" not in save_info or "post" not in save_info or "type" not in save_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # There shouldn't need to be any validation as the username and post_id are sent directly.

        # Gets the current date in "YYYY-MM-DD HH:MI:SS" format.
        current_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        # If type is 1: Saves the specific username-post save relation as a database entity.
        if (save_info["type"] == 1):
            save_query = "INSERT INTO SavedPost VALUES (%s, %s, %s);"
            save_values = (save_info["username"], save_info["post"], current_date)
            cursor.execute(save_query, save_values)
            mysql.connection.commit()

        # If type is -1: Deletes the specifice username-post save relation entity from the database.
        elif (save_info["type"] == -1):
            unsave_query = "DELETE FROM SavedPost WHERE username = %s AND post_id = %s;"
            unsave_values = (save_info["username"], save_info["post"])
            cursor.execute(unsave_query, unsave_values)
            mysql.connection.commit()

        return "post has been saved"


# # # # Backend code for pulling a user's saved posts on Weave
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the posts that the user has saved within the specified range.
# # Call this route from the Windows Command Prompt with: 
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"realuser1\",\"start\":\"0\",\"end\":\"10\"}" http://localhost:5000/savedposts/
@weave_post.route("/savedposts/", methods=["POST"])
@jwt_required
def weave_pull_saves():

    # The backend has received a saved post POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        save_info = request.get_json()

        # Checks for all needed elements in the JSON.
        if ("start" not in save_info or "end" not in save_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        save_info["username"] = get_jwt_identity()

        # Checks if username exists in database.
        # This also doubles as a validation statement, assuming all previous usernames are validated correctly.
        cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (save_info["username"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'User does not exist'}), 404
        cursor.fetchall()

        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(save_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(save_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400
        
        # Pulls the saved posts of the user as specified by the range.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        save_query = "SELECT post_id FROM SavedPost WHERE username = \"" + \
            save_info["username"] + "\" ORDER BY date_saved DESC LIMIT " + \
            str(save_info["start"]) + ", " + str(save_info["end"]) + ";"
        cursor.execute(save_query)

        # Adds the saved posts to a list that will then be returned.
        save_list = []
        for row in cursor:
            save_list.append(row["post_id"])
        print(str(save_list)) # debugging

        # Pulls the count of all the saved posts of the user.
        count_query = "SELECT COUNT(post_id) AS count FROM SavedPost WHERE username = %s;"
        cursor.execute(count_query, (save_info["username"],))
        count = cursor.fetchall()[0]["count"]
        
        # Return as list
        return {'pull_list': save_list,
                'rowCount': count}
        
        
# # # # Backend code for pulling a list of posts that have a certain topic
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the posts in a topic within the specified range.
@weave_post.route("/topicposts/", methods=["POST"])
@jwt_required
def weave_pull_topicposts():

    # The backend has received a saved post POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()

        # Checks for all needed elements in the JSON.
        if ("topic" not in pull_info or "start" not in pull_info or "end" not in pull_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400
        
        # Checks if topic exists in database.
        cursor.execute("SELECT * FROM Topic WHERE topic_name = %s;", (pull_info["topic"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message': 'Topic does not exist'}), 404
        cursor.fetchall()
        
        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(pull_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(pull_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400

        # Pulls the user's most recent posts as specified by the range.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        pull_query = "SELECT post_id FROM Post WHERE topic_name = \"" + \
            pull_info["topic"] + "\" ORDER BY post_id DESC LIMIT " + \
            str(pull_info["start"]) + ", " + str(pull_info["end"]) + ";"
        cursor.execute(pull_query)

        # Adds the user's posts to a list that will then be returned.
        pull_list = []
        for row in cursor:
            pull_list.append(row["post_id"])
        print(pull_list)

        # Pulls the count of all the posts of the topic.
        count_query = "SELECT COUNT(post_id) AS count FROM Post WHERE topic_name = %s;"
        cursor.execute(count_query, (pull_info["topic"],))
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'pull_list': pull_list,
            'rowCount': count
        }