from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
weave_post = Blueprint('weave_post', __name__)


# # # # # Backend code for creating posts on Weave.
# # Will save a "text post" to the database. If the post has a picture component, another server request will be needed.
# # Expects a POST request with a JSON. Details are discussed in "/api/README.md".
# # Call this route from the Windows Command Prompt with:
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\",\"topic\":\"general\",\"type\":\"1\",\"title\":\"TESTPOST\",\"content\":\"hello hello hello hello\",\"anon\":\"0\"}" http://localhost:5000/createpost/
@weave_post.route("/createpost/", methods=["GET", "POST"])
@jwt_required
def weave_post_create():

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    # Checks for JSON format.
    if (not request.is_json):
        return jsonify({'error_message':'Request Error: Not JSON.'})
    post_info = request.get_json()
    post_info["username"] = get_jwt_identity()

    # This horrific thing checks that the JSON has all the needed elements.
    if ("username" not in post_info or "topic" not in post_info or "title" not in post_info or "content" not in post_info or "anon" not in post_info):
        return jsonify({'error_message':'Request Error: Missing JSON Element'}) 

    # Don't have to validate the username because the frontend should send us it directly. (?)
    # May want to validate anon flag for safety, even though the backend will always send it to us without user input. (?)
    # Topic stuff is not implemented in this sprint, but when it IS implemented there will need to be more stuff here.

    # Validates the content information.
    # Most strings will be fine. Empty content will be saved as an empty string. Any \" phrase must be replaced with \\\".
    post_info["content"].replace("\\\"", "\\\\\\\"")
    
    # The post will always be treated as a text post when it is being saved to the database. 
        
    # Assigns the Post a new post_id by querying the most recent post and then adding one.
    # The post_id is initialized to 1 because the first query should not return any posts.
    post_id = 1 
    id_query = "SELECT post_id FROM Post ORDER BY post_id DESC LIMIT 1;"
    cursor.execute(id_query)
    for row in cursor:
        post_id = row["post_id"] + 1

    # Gets the current date in "YYYY-MM-DD" format.
    current_date = datetime.today().strftime("%Y-%m-%d")

    # Insert new text post into the database.
    post_query = "INSERT INTO Post VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    post_values = (post_id, post_info["topic"], post_info["username"], current_date, 0, post_info["title"], post_info["content"], None, 0, 0, post_info["anon"], 0)
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
@weave_post.route("/createimage/", methods=["GET", "POST"])
@jwt_required
def weave_post_upload_image():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Uploads a photo if attached.
        new_filename = ""
        if 'file' in request.files:
            img_file = request.files['file']
            # Checks to make sure an image is attached.
            if img_file.filename != '':
                new_filename = secure_filename(img_file.filename)
                prefix = 0
                # Adjusts filename for duplicate names.
                while (path.exists(str(current_app.config['UPLOAD_FOLDER']) + str(prefix) + str(new_filename))):
                    prefix += 1
                new_filename = str(prefix) + new_filename
                img_file.save(str(current_app.config['UPLOAD_FOLDER']) + str(new_filename))
            else:
                return "no content"

        # Grabbing identity of uploader.
        identity = get_jwt_identity()
        
        # Putting file path into database for user's most recent post.
        # This should work as long as the database doesn't miss a request for some reason.
        mod_query = "UPDATE Post SET pic_path = %s WHERE creator = %s ORDER BY date_created DESC LIMIT 1;"
        mod_values = (new_filename, identity)
        cursor.execute(mod_query, mod_values)
        mysql.connection.commit() 
        return "user has added post picture"


# # # # # Backend code for viewing posts on Weave.
# # DOES NOT expect a JSON but DOES expect a unique URL for the post that needs to be displayed.
# # The frontend will need to make another call to /postimage/<post_id> to get any possible other image.
@weave_post.route("/post/<post_id>", methods=["GET"])
@jwt_required
def weave_post_data(post_id):
    
    # The backend has received a profile GET request.
    if request.method == "GET":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()
        
        # Checks if post exists in db and grabs relevant data.
        cursor.execute("SELECT topic_name, date_created, post_type, title, content, upvote_count, downvote_count, anon_flag, creator FROM POST WHERE post_id = %s;", (post_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'Post does not exist'}), 404
        
        # Checks and updates return items if post is anonymous.
        post_info = (cursor.fetchall())[0]
        print(post_info)
        if (post_info["anon_flag"] == True):
            post_info["creator"] = "anonymous"
        post_info.pop("anon_flag", None)

        # Adds identity of requester to the JSON.
        post_info["username"] = get_jwt_identity()
        
        # Returns post info as JSON object.
        return post_info


# # # # Backend code for getting a post's special qualities according to a specific user.
# # Expects a JSON with details defined in "api/README.md".
@weave_post.route("/poststates/", methods=["POST"])
@jwt_required
def weave_post_state():
    if request.method == "POST":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()
        
        saved = 0
        voted = 0
        
        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400
        post_info = request.get_json()
        post_info["username"] = get_jwt_identity()
        
        if ("username" not in post_info or "post_id" not in post_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400 
        
        # Checks if upvoted/downvoted
        vote_query = "SELECT score FROM PostVote WHERE username = %s and post_id = %s;"
        vote_values = (post_info["username"], post_info["post_id"])
        cursor.execute(vote_query, vote_values)
        if (cursor.rowcount > 0):
            voted = (cursor.fetchall())[0]["score"]
        
        # Checks is saved or not
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
# # DOES NOT expect a JSON but DOES expect a unique URL for the post that needs to be displayed.
# # This route will likely have to be called without explicitly navigating to this URL.
@weave_post.route("/postimage/<post_id>", methods=["GET"])
@jwt_required
def weave_post_image(post_id):

    # The backend has received a profile GET request.
    if request.method == "GET":
    
        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks if post exists in db; may not need to be done if we know the post data route is visited first.
        cursor.execute("SELECT pic_path FROM POST WHERE post_id = %s;", (post_id,))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'Post does not exist'}), 404
        
        # Pulls the picture path out of the cursor. 
        filename = cursor.fetchall()[0]["pic_path"]

        # Sends the file back to the frontend. 
        # Media file type detection should work automatically but may need to be updated if not. 
        return send_file(filename)


# # # # Backend code for pulling a user's posts on Weave
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
@weave_post.route("/userposts/", methods=["POST"])
# @jwt_required
def weave_pull_userposts():

    # The backend has received a saved post POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400
        pull_info = request.get_json()

        if ("username" not in pull_info or "start" not in pull_info or "end" not in pull_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400 

        # Checks if username exists in database.
        cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (pull_info["username"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'User does not exist'}), 404
        cursor.fetchall()

        # Pulls the user's most recent posts as specified by the range.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        pull_query = "SELECT post_id FROM Post WHERE creator = \"" + pull_info["username"] + "\" AND anon_flag = 0 ORDER BY date_created DESC LIMIT " + pull_info["start"] + ", " + pull_info["end"] + ";"
        cursor.execute(pull_query)

        # Adds the user's posts to a list that will then be returned.
        pull_list = []
        for row in cursor:
            pull_list.append(row["post_id"])

        # List needs to be rewritten as a string that frontend will have to parse.
        pull_string = ""
        for element in range(len(pull_list)):
            pull_string += str(pull_list[element])
            pull_string += ","   
        return jsonify({'pull_list':pull_string}), 200


# # # # Backend code for saving posts on Weave
# # Doesn't expect a unique URL right now, but this may be changed later.
# # Does expect a POST request along with a JSON. Details will be in "/api/README.md". 
@weave_post.route("/save/", methods=["POST"])
@jwt_required
def save_weave_post():

    # The backend has recieved information that needs to go into the database.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400
        save_info = request.get_json()
        print(save_info)

        # Checks for all needed elements in the JSON.
        if ("username" not in save_info or "post" not in save_info or "type" not in save_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400 

        # There shouldn't need to be any validation as the username and post_id are sent directly.
        
        # Gets the current date in "YYYY-MM-DD" format.
        current_date = datetime.today().strftime("%Y-%m-%d")
        if (save_info["type"] == 1):
            # Saves the specific username-post save relation as a database entity.
            save_query = "INSERT INTO SavedPost VALUES (%s, %s, %s);"
            save_values = (save_info["username"], save_info["post"], current_date)
            cursor.execute(save_query, save_values)
            mysql.connection.commit()       
        elif (save_info["type"] == -1):
            # Unsaves the specifice username-post save relation
            unsave_query = "DELETE FROM SavedPost WHERE username = %s AND post_id = %s;"
            unsave_values = (save_info["username"], save_info["post"])
            cursor.execute(unsave_query, unsave_values)
            mysql.connection.commit()  
        
        return "post has been saved"


# # # # Backend code for pulling a user's saved posts on Weave
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
#       curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"realuser1\",\"start\":\"0\",\"end\":\"10\"}" http://localhost:5000/savedposts/
@weave_post.route("/savedposts/", methods=["POST"])
# @jwt_required
def weave_pull_saves():

    # The backend has received a saved post POST request.
    if request.method == "POST":

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message':'Request Error: Not JSON.'}), 400
        save_info = request.get_json()

        # Checks for all needed elements in the JSON.
        if ("username" not in save_info or "start" not in save_info or "end" not in save_info):
            return jsonify({'error_message':'Request Error: Missing JSON Element'}), 400 

        # Checks if username exists in database.
        cursor.execute("SELECT * FROM UserAccount WHERE username = %s;", (save_info["username"],))
        if (cursor.rowcount == 0):
            return jsonify({'error_message':'User does not exist'}), 404
        cursor.fetchall()

        # Pulls the saved posts of the user as specified by the range.
        # This query has to be written this ugly way because otherwise the limit parameters will be written with surrounding quotes.
        save_query = "SELECT post_id FROM SavedPost WHERE username = \"" + save_info["username"] + "\" ORDER BY date_saved DESC LIMIT " + save_info["start"] + ", " + save_info["end"] + ";"
        cursor.execute(save_query)

        # Adds the saved posts to a list that will then be returned.
        save_list = []
        for row in cursor:
            save_list.append(row["post_id"])
        
        # List needs to be rewritten as a string that frontend will have to parse.
        save_string = ""
        for element in range(len(save_list)):
            save_string += str(save_list[element])
            save_string += ","
        return jsonify({'save_list':save_string}), 200
