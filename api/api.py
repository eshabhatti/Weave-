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

# Initializes Flask
app = Flask(__name__)
flask_cred = open("credentials/flaskcredentials.txt")
app.secret_key = flask_cred.readline().strip("\n\r ").encode('utf8')

# Configures and initializes JWT
app.config['JWT_SECRET_KEY'] = flask_cred.readline().strip("\n\r ")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    current_user = get_jwt_identity
    return jsonify(logged_in=current_user)

@app.route("/partially_protected")
@jwt_optional
def partially_protected():
    # Access the identity of current user
    current_user = get_jwt_identity
    if current_user:
        return jsonify(logged_in=current_user)
    else:
        return jsonify(logged_in='anon')

# # # # Backend code for LOGOUT requests
@app.route("/logout")
def weave_logout():
    # logs the user using flask_login's method
    # login_required to travel to this route

    # travel to login page again
    # return redirect(url_for("login"))

    return "Logged out successfuly"


if __name__ == "__main__":
   app.run()
