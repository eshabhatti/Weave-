from flask import Blueprint, request, jsonify, current_app, send_file
from extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
weave_timeline = Blueprint('weave_timeline', __name__)

@weave_timeline.route("/timeline", methods=["POST"])
@jwt_required
def weave_render_timeline():

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    return "timeline"

@weave_timeline.route("/followuser", methods=["POST"])
@jwt_required
def weave_follow_user():

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    return "follow user"

@weave_timeline.route("/followtopic", methods=["POST"])
@jwt_required
def weave_follow_topic():

    # Initializes MySQL cursor
    cursor = mysql.connection.cursor()

    return "follow user"
