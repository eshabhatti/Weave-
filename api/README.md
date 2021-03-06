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

* The text portion of post creation (`/createpost/`) requires a JSON object where JSON = 
    * username: \[creator-username\]
    * topic: \[post-topic\]
    * type: \[post-type\]
        * Note that the post type will be 1 if the post is text and 2 if the post is picture-caption.
    * title: \[post-title\]
    * content: \[post-content-or-caption\]
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
    * type: \[save-or-unsave\]
        * Note that type will be 1 if the post is being saved, and -1 is the post is being unsaved.

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

* Special per-user post data pulling (`/poststates/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * post_id: \[post-id\]

* Post pulling per topic (`/topicposts/`) requires a JSON object where JSON = 
    * topic: \[topic-name\]
    * start: \[begin-value\]
    * end: \[end-value\]
        * Note that begin-value will start at 0 and end value will be exclusive (range 0-10 will give 10 posts).

* Timeline post pulling (`/timeline`) requires a JSON object where JSON = 
    * start: \[begin-value\]
    * end: \[end-value\]
        * Note that begin-value will start at 0 and end value will be exclusive (range 0-10 will give 10 posts).

* Following users (`/followuser`) requires a JSON object where JSON = 
    * following: \[username-to-follow\]
    * type: \[follow-or-unfollow\]
        * Note that type will be 1 if the user is being followed, and -1 is the user is being unfollowed.

* Following topics (`/followtopic`) requires a JSON object where JSON = 
    * following: \[topic-to-follow\]
    * type: \[follow-or-unfollow\]
        * Note that type will be 1 if the topic is being followed, and -1 is the topic is being unfollowed.

* Comment creation (`/createcomment/`) requires a JSON object where JSON = 
    * creator: \[user-creator\]
    * content: \[comment-content\]
    * post_id: \[post-above-comment\]

* Comment pulling per post (`/pullcomments/`) requires a JSON object where JSON = 
    * post_id: \[post-id\]
    * start: \[begin-value\]
    * end: \[end-value\]
        * Note that begin-value will start at 0 and end value will be exclusive (range 0-10 will give 10 posts).

* Comment pulling per user (`/pullusercomments/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * start: \[begin-value\]
    * end: \[end-value\]
        * Note that begin-value will start at 0 and end value will be exclusive (range 0-10 will give 10 posts).

* Special per-user comment data pulling (`/commentstates/`) requires a JSON object where JSON = 
    * username: \[username-string\]
    * comment_id: \[comment-id\]

* Sensitive information updating (`/updatesettings/`) requires a JSON object where JSON = 
    * currentpass: \[current-plaintext-password-string\]
    * newpass: \[optional-new-plaintext-password-string\]
    * newusername: \[optional-new-username-string\]
    * newemail: \[optional-new-email-string\]
    * privacy: \[optional-privacy-mode-flag\]

* Direct message creation (`/createmessage/`) requires a JSON object where JSON = 
    * receiver: \[username-of-receiver\]
    * content: \[content-of-message\]