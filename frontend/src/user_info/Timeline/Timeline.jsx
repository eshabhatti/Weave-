import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import ImageUploader from 'react-images-upload';

import "./timeline.css";

export default function Timeline() {
	const [postContent, updatePostContent] = useState("");
	const [postTitle, updatePostTitle] = useState("");
	const [isAnon, updateIsAnon] = useState("");
	const onSubmit = (event) => {}
	const access_token = localStorage.getItem('access_token');
	if (access_token == null) {
		window.location = "/login"
	}
    return (
		<div>
			<div>
				{/* Bootstrap Stylesheet */}
				<link
					rel="stylesheet"
					href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
					integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
					crossorigin="anonymous"
				/>
				<Navbar expand="lg" bg="dark" variant="dark" sticky="top">
					<Navbar.Brand href="/login">
						<img src="/img/weave-icon.svg" width="50" height="50"
							 className="d-inline-block align-top" alt="" />
					</Navbar.Brand>
					<Nav className="mr-auto">
						<Nav.Link>Messages</Nav.Link>
						<Nav.Link>Notifications</Nav.Link>
						<Nav.Link>Help</Nav.Link>
					</Nav>
				</Navbar>
			</div>
			<h1 className="post-header">Create a post</h1>
			<div className="post-container">
			  <form className="post-form">
			  	  
				<label className="post-form-label">Post Title</label>
				<input 
				  value={postTitle}
				  onChange={e => {
					  updatePostTitle(e.target.value);
				  }}
				  className="post-form-input-title"
				/>  

				<label className="post-form-label">Post Text</label>
				<textarea
				  value={postContent}
				  onChange={e => {
				    updatePostContent(e.target.value);
				  }}
				className="post-form-input-body" 
				/>

				<label className="post-form-label">Post Picture</label>
          		<ImageUploader
            	  withIcon={true}
                  imgExtension={['.jpg', 'jpeg', '.gif', '.png', '.gif']}
                  maxFileSize={10000000}
                  buttonText='Add a picture to your post.'
                  className="post-pic-upload"
                />
				  
				<input 
				  type="checkbox"
				  id="anon"
			      className="post-check-box"
				  checked={isAnon}
				  onChange={e => {
					  updateIsAnon(!isAnon);
				  }}
				/>
				<label for="anon" className="post-check-label">Make this post anonymously</label>

				<button type="submit" className="post-submit-btn" onClick={(e) => onSubmit(e)}>Create Post</button>
			  </form>

			  <a href="../../login" className="return-link">go back</a>
			</div>
		</div>
    );
}