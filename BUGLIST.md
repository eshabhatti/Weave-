## BUG LOG FOR WEAVE

* Creating posts with images causes a race condition that may result in the image getting attached (and possibly overwriting) the wrong post.
* 404 routing no longer works on incorrect profile pages; returning to 404 profiles instead gives a React error.
* Certain backend paramaters are not checked, which may cause query errors (see backend files for specific notes).
* The back button on the profile modification page does not return the user to the correct profile if their username is modified.
* CSS elements "break" when multiple posts are expanded or when certain text fields are longer than expected.
