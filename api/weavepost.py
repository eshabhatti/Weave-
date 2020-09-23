# from MySQLdb import _mysql

# def weave_post(reg_info):
    
#     # Initializes local database instance
#     mysql_cred = open("dbcredentials.txt")
#     db = _mysql.connect(host="localhost", user=mysql_cred.readline().strip("\n\r "), passwd=mysql_cred.readline().strip("\n\r "), db="weave")
#     mysql_cred.close()

#     # Authentication

#     # Assigns the Post a new post_id by querying the most recent post and then adding one.
#     db.query("SELECT post_id FROM Post ORDER BY date_created DESC LIMIT 1;")
#     newpost = db.store_result()
#     result = newpost.fetch_row()
#     print(result[0])
    

#     db.close()
    
#     return "sucess"