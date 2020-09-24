from flask import Blueprint, request
from extensions import mysql
weave_post = Blueprint('weave_post', __name__)

# # # # # Backend code for CREATEPOST requests
# # Expects JSON of {"username":"[username]","topic":"[topic]","type":"[post-type]","title":"[title]","content":"[content]","picpath":"[picpath]"}
# # curl -i -X POST -H "Content-Type:application/json" -d "{\"username\":\"testname\"}" http://localhost:5000/createpost/
@weave_post.route("/createpost/", methods=["GET", "POST"])
def weave_post_create():

    #Checks for JSON format.
    if (not request.is_json):
        return "Error: Request is not JSON"
    return "function called"

#def weave_post_test(reg_info):

#     # Authentication

#     # Assigns the Post a new post_id by querying the most recent post and then adding one.
#     db.query("SELECT post_id FROM Post ORDER BY date_created DESC LIMIT 1;")
#     newpost = db.store_result()
#     result = newpost.fetch_row()
#     print(result[0])
    

#     return "sucess"