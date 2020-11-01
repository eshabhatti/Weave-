## BUG LOG FOR WEAVE

### Functionality Errors
 
* Creating posts with images causes a race condition that may result in the image getting attached (and possibly overwriting) the wrong post.
* 404 routing no longer works on incorrect profile pages; returning to 404 profiles instead gives a React error.
* The back button on the profile modification page does not return the user to the correct profile if their username is modified.
* Somewhat minor, but deleting an account will also rewrite the account's anonymous posts as DELETED, which breaks the garuntee of anonymousness that the functionality was supposed to have.
* For some reason, the cursor doesn't work in the forth follow test and thus the test only relies on what the backend says rather than the actual database entity. 
* Users oftentimes have to refresh upon a modification to their profile page, probably caused by how we route back to this page.
* Not having any input in the edit profile fields deletes any previous modifications, instead of keeping them the same.
* Following count still needs to be implemented (may be a sprint three thing).

### Style Errors

* There needs to be navigation to the user's profile page somewhere on the website. The Weave icon in the navigation bar could be used for this.
* After successful post creation, the form should refresh to prevent spam and to show successful post creation.
* After successful comment creation, the post page should refresh to prevent spam and to show successful comment creation.  
* There are a lot of warnings in the NPM compile output. May want to look into some of these.
* Sidebar doesn't stretch all the way down on the topic or the post page. (It is especially noticeable on the latter. It probably has to do with flexboxes in CSS.)
* The settings page needs some CSS as well.
* Post text only takes up about 40% of the avaliable space on a post container, making the whole thing look very lopsided. 
* The posts on most feed pages are centered with the page and not with the non-sidebar white space and this makes me very upset.
* Inputs on Weave should eventually have some sort of help icon that shows the constraints behind each input.
* There really should be some way for the user to see what picture is currently in the upload queue. 
