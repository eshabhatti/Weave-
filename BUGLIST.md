## BUG LOG FOR WEAVE

### Functionality Errors
 
* Creating posts with images causes a race condition that may result in the image getting attached (and possibly overwriting) the wrong post.
* Image posting no longer seems to work?
* 404 routing no longer works on incorrect profile pages; returning to 404 profiles instead gives a React error.
* The back button on the profile modification page does not return the user to the correct profile if their username is modified.
* Cannot switch between posts and interactions on a user's profile.
* Saving posts does not work right -- each click of the button seems to call the save route twice, and the database sends an exception when saving posts for this reason.
* Somewhat minor, but deleting an account will also rewrite the account's anonymous posts as DELETED, which breaks the garuntee of anonymousness that the functionality was supposed to have.
* For some reason, the cursor doesn't work in the forth follow test and thus the test only relies on what the backend says rather than the actual database entity. 

### Style Errors

* There needs to be navigation to the user's profile page somewhere on the website. The Weave icon in the navigation bar could be used for this.
* There need to be ways for the user to access topics and other users directly from the UI. Posts could be modified like before to include this information.
* CSS elements may "break" when certain text fields are longer than expected.
* After successful post creation, the form should refresh to prevent spam and to show successful post creation.
* After successful comment creation, the post page should refresh to prevent spam and to show successful comment creation. 
* Next and back buttons on each feed should probably be made more prominent and easier to click. 
* The user's name on their profile should not say "NULL NULL" before a name is added to the account.
* There are a lot of warnings in the NPM compile output. May want to look into some of these.
* Posts have their bookmark highlighted when first viewed, making it seem as if the post has been saved before it actually has.
