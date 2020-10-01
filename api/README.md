# API: Weave Backend

To run the backend: 
1. Activate the your Python virtual environment with `source venv/bin/activate` on MacOS/Linux or `venv\Scripts\activate` on Windows. 
2. Make sure to install any relevant dependencies with `pip install -r requirements.txt`.
3. Run `python3 api.py`. 

Note: If you install any dependencies, make sure they are installed while the virtual environment is active. After installation, run `pip freeze > requirements.txt` to save them as project dependencies.

### JSON Information

POST requests to the following routes require JSON objects formatted as shown:

* User registration (`/register/`) requires a JSON object where JSON =
    * username: \[username-string\]
    * password: \[plaintext-password\]
    * email: \[email-string\]

* User login (`/login/`) requires a JSON object where JSON = 
    * username: \[username-or-email\]
    * password: \[plaintext-password\]

* Post creation (`/createpost/`) requires a JSON object where JSON = 
    * username: \[creator-username\]
    * topic: \[post-topic\]
    * type: \[post-type\]
        * Note that the post type will be 1 if the post is text and 2 if the post is picture-caption.
    * title: \[post-title\]
    * content: \[post-content-or-caption\]
    * picpath: \[location-of-image\]
    * anon: \[anonymous-identifier\]
        * Note that the anon flag will be 0 if the post is not anonymous and 1 if the post is anonymous. 

* Profile editing (`/editprofile/`) requires a JSON object where JSON = 
    * username: \[original-username\]
    * newusername: \[updated-username\]
        * Note that the new username will be the same as the old username if there is no change.
    * firstname: \[first-name\]
    * lastname: \[last-name\]
    * biocontent: \[user-bio-string\]
    * profilepic: \[path-to-profile-image\]
        * Note that if any of the above four items can be passed as empty strings.

* Post saving (`/save/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * post: \[post-id\]

* Post voting (`/vote/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * type: \[post-or-comment\]
        * Note that vote type will be 1 if the vote is for a post and 2 if the vote is for a comment.
    * id: \[post-or-comment-id\]
    * vote: \[vote-score\]
        * Note that the score will be 1 if the vote is up, -1 if the vote is down, and 0 if the vote should be deleted.

* Saved post pulling (`/savedposts/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * start: \[begin-value\]
    * end: \[end-value\]
        * Note that begin-value will start at 0 and end value will be exclusive (range 0-10 will give 10 posts).

* Post pulling per user (`/userposts/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * start: \[begin-value\]
    * end: \[end-value\]
        * Note that begin-value will start at 0 and end value will be exclusive (range 0-10 will give 10 posts).