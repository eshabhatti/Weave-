import time
import re
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
#config for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'weave'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#initializes MySQL
mysql = MySQL(app)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}
    
@app.route('/register/', methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        valid_info = True
        if (not request.is_json):
            valid_info = False
        reg_info = request.get_json()
        #if(not username_valid(reg_info["username"]))
        #    valid_info = False
        #if(not password_valid(reg_info["password"]))
        #    valid_info = False
        if(re.search("^\S+@\S+$",reg_info["email"]) == None):
            valid_info = False
        
        if(valid_info):
            #insert new user into database
            cursor = mysql.connection.cursor()
            register_query = "INSERT INTO UserAccount VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s);"
            register_values = (reg_info["username"],reg_info["email"], "pass", "word", "real", "user", "1998-12-12" , "Null", "Null", "0", "0")
            cursor.execute(register_query, register_values)
            mysql.connection.commit()
            #print resulting table for testing
            cursor.execute("SELECT * from UserAccount")
            print(cursor.fetchall())
            return "send user to their new profile page"
        else:
            return "invalid request"
    else:
        return "serve register page"

@app.route('/login/', methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        return "try to login user"
    else:
        return "serve the login page"

if __name__ == "__main__":
   app.run()
