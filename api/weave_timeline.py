from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import re
weave_timeline = Blueprint('weave_timeline', __name__)


# # # # Backend code for displaying a user's timeline on Weave.
# # Does not expect a unique URL but does expect a JSON. Details will be in "api/README.md".
# # Returns a JSON with a list of the posts made by a user within the specified range.
@weave_timeline.route("/timeline", methods=["POST"])
@jwt_required
def weave_render_timeline():

    # The backend has recieved a request to display the user's timeline.
    if request.method == "POST":

        # Checks for JSON format.
        if (not request.is_json):
            return jsonify({'error_message': 'Request Error: Not JSON.'}), 400
        timeline_info = request.get_json()

        # Checks for all needed JSON elements.
        if ("start" not in timeline_info or "end" not in timeline_info):
            return jsonify({'error_message': 'Request Error: Missing JSON Element'}), 400

        # Validates start and end conditions because of the insecure query.
        # This SHOULD never return an error if called legitimately from the frontend.
        if (re.search("^[0-9]+$", str(timeline_info["start"])) == None):
            return jsonify({'error_message': 'Bad start value'}), 400
        if (re.search("^[0-9]+$", str(timeline_info["end"])) == None):
            return jsonify({'error_message': 'Bad end value'}), 400

        # Initializes MySQL cursor.
        cursor = mysql.connection.cursor()

        # Grabs the identity of the user.
        username = get_jwt_identity()

        # This SQL statement will pull everything the we need from the database for timeline display.
        # Not only is this thing long and ugly, but it is also insecure and requires the limits to be validated above. B)
        timeline_query = "SELECT post_id FROM Post " + \
            "WHERE post_id IN ( SELECT post_id FROM Post WHERE creator = %s AND anon_flag = 0 ) " + \
            "OR post_id IN ( SELECT post_id FROM Post AS P, FollowTopic AS T " + \
                "WHERE T.topic_followed = P.topic_name AND T.user_follower = %s ) " + \
            "OR post_id IN ( SELECT post_id FROM Post AS P, FollowUser AS F " + \
                "WHERE F.user_followed = P.creator AND P.anon_flag = 0 AND F.user_follower = %s ) " + \
            "ORDER BY date_created DESC " + \
            "LIMIT " + str(timeline_info["start"]) + ", " + str(timeline_info["end"]) + ";"
        timeline_values = (username, username, username)
        cursor.execute(timeline_query, timeline_values)

        # Adds the timeline posts to a list that will then be returned.
        timeline_list = []
        for row in cursor:
            timeline_list.append(row["post_id"])
        print(str(timeline_list)) #debugging

        # Returns the total count of timeline posts.
        timeline_query = "SELECT COUNT(post_id) AS count FROM Post " + \
            "WHERE post_id IN ( SELECT post_id FROM Post WHERE creator = %s AND anon_flag = 0 ) " + \
            "OR post_id IN ( SELECT post_id FROM Post AS P, FollowTopic AS T " + \
                "WHERE T.topic_followed = P.topic_name AND T.user_follower = %s ) " + \
            "OR post_id IN ( SELECT post_id FROM Post AS P, FollowUser AS F " + \
                "WHERE F.user_followed = P.creator AND P.anon_flag = 0 AND F.user_follower = %s ) " + \
            "ORDER BY date_created DESC " + \
            "LIMIT " + str(timeline_info["start"]) + ", " + str(timeline_info["end"]) + ";"
        timeline_values = (username, username, username)
        cursor.execute(timeline_query, timeline_values)
        count = cursor.fetchall()[0]["count"]

        # Return as list
        return {
            'timeline_list': timeline_list,
            'rowCount': count
        }
