import time
import re
import datetime
from flask import Flask, request, jsonify
from extensions import mysql
from flask_jwt_extended import (
    JWTManager, jwt_required, jwt_optional, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from flask_cors import CORS

from models import User
from weave_post import weave_post
from weave_register import weave_register
from weave_login import weave_login
from weave_profile import weave_profile
from weave_vote import weave_vote
from weave_timeline import weave_timeline
from weave_comment import weave_comment
from weave_follow import weave_follow
from weave_delete import weave_delete
from weave_topic import weave_topic
from weave_message import weave_message
from weave_block import weave_block
from weave_search import weave_search

# Initializes Flask
app = Flask(__name__)
flask_cred = open("credentials/flaskcredentials.txt")
app.secret_key = flask_cred.readline().strip("\n\r ").encode('utf8') # I'm not sure we need this anymore. 

# Configures saving path for photos
saving_path = open("credentials/savingpath.txt")
saving_path = saving_path.readline().strip("\n\r ")
app.config['UPLOAD_FOLDER'] = saving_path
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
# saving_path.close()

# Configures and initializes JWT
app.config['JWT_SECRET_KEY'] = flask_cred.readline().strip("\n\r ")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
flask_cred.close()

# Allows CORS on all domains.
CORS(app)

# Config for MySQL
# RUN CREATETABLES.SQL ON YOUR LOCAL MYSQL SERVER IN ORDER FOR THE DATABASE TO WORK
mysql_cred = open("credentials/dbcredentials.txt")
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = mysql_cred.readline().strip("\n\r ")      
app.config['MYSQL_PASSWORD'] = mysql_cred.readline().strip("\n\r ") 
app.config['MYSQL_DB'] = 'weave'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql_cred.close()

# Initializes MySQL
mysql.init_app(app)

# Breaks the Flask API into multiple sections.
with app.app_context():
    app.register_blueprint(weave_post)
    app.register_blueprint(weave_register)
    app.register_blueprint(weave_login)
    app.register_blueprint(weave_profile)
    app.register_blueprint(weave_vote)
    app.register_blueprint(weave_timeline)
    app.register_blueprint(weave_comment)
    app.register_blueprint(weave_follow)
    app.register_blueprint(weave_delete)
    app.register_blueprint(weave_topic)
    app.register_blueprint(weave_message)
    app.register_blueprint(weave_block)
    app.register_blueprint(weave_search)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # Backend code for token blacklist checking
# # Looks for the token in the database of blacklisted tokens.
# # Returns true if the token is in the blacklist; returns false otherwise. 
@jwt.token_in_blacklist_loader
def check_against_blacklist(passed_token):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT token FROM Blacklist WHERE token = %s;", (passed_token,))
    if (cursor.rowcount == 0):
        return False
    else:
        return True

# # # # Backend code for TIME requests. 
# # This is no longer implmented in the frontend, I believe.
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # refresh token endpoint
    current_user = get_jwt_identity()
    ret = {
            'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

@app.route("/protected")
@jwt_required
def protected():
    # Access the identity of current user
    current_user = get_jwt_identity()
    return jsonify(logged_in=current_user)

@app.route("/partially_protected")
@jwt_optional
def partially_protected():
    # Access the identity of current user
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in=current_user)
    else:
        return jsonify(logged_in='anon')

if __name__ == "__main__":
   app.run()
