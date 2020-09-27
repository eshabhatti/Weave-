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

* Profile Editing (`/editprofile/`) requires a JSON object where JSON = 
    * username: \[original-username\]
    * newusername: \[updated-username\]
        * Note that the new username will be the same as the old username if there is no change.
    * firstname: \[first-name\]
    * lastname: \[last-name\]
    * biocontent: \[user-bio-string\]
    * profilepic: \[path-to-profile-image\]
        * Note that if any of the above four items can be passed as empty strings.

* Post Saving (`/save/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * post: \[post-id\]