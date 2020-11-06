## BUG LOG FOR WEAVE

### Functionality Errors
 
* The back button on the profile modification page does not return the user to the correct profile if their username is modified.
* Deleting a user's account does not remove votes (allowing spammers or trolls to make an account, vote on a post, delete their account, then make an account to do all this over again).
* Deleting a user's account also does not remove follows, once again allowing people to inflate these numbers.
* Somewhat minor, but deleting an account will also rewrite the account's anonymous posts as DELETED, which breaks the garuntee of anonymousness that the functionality was supposed to have.
* Users oftentimes have to refresh upon a modification to their profile page, probably caused by how we route back to this page.
* Following count on the profile page still needs to be implemented or removed.
* For some reason, the cursor doesn't work in the fourth follow test and thus the test only relies on what the backend says rather than the actual database entity. (Super minor.)

### Style Errors

* After successful post creation, the form should refresh to prevent spam and to show successful post creation.
* After successful comment creation, the post page should refresh to prevent spam and to show successful comment creation.  
* There are a lot of warnings in the NPM compile output. May want to look into some of these.
* Post text only takes up about 40% of the avaliable space on a post container, making the whole thing look very lopsided. 
* The posts on most feed pages are centered with the page and not with the non-sidebar white space and this makes me very upset.
* Inputs on Weave should eventually have some sort of help icon that shows the constraints behind each input.
* There really should be some way for the user to see what picture is currently in the upload queue. 
