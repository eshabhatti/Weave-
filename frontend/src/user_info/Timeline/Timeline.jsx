import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import ImageUploader from 'react-images-upload';

import "./timeline.css";

export default function Timeline() {
	const [postContent, updatePostContent] = useState("");
	const [postTitle, updatePostTitle] = useState("");
	const [isAnon, updateIsAnon] = useState("0");
	const access_token = localStorage.getItem('access_token');
	const [image, saveImage] = useState(null);

	const [errorMessage, updateErrorMessage] = useState("");
	if (access_token == null) {
		window.location = "/login"
	}

	const onSubmit = (event) => {
		event.preventDefault();
		/* More to be added for posts eventually */
		if (isFormValid({ postTitle, postContent, updateErrorMessage })) {
			const body = {
				title: postTitle,
				content: postContent,
				anon: isAnon,
				topic: "test"
			}
			const endpoint = "http://localhost:5000/createpost/";
			fetch(endpoint, {
				method: "POST",
				headers: {
					'Content-Type': 'application/json',
					'Authorization': 'Bearer ' + access_token
				},
				body: JSON.stringify(body)
			}).then(response => response.json()).then(data => {
				if (data.error_message) {
					updateErrorMessage(data.error_message);
				} else {

				}
			}).catch(err => {
				console.error(err);
				alert(err);
			});

			if (image !== null) {
				const formData = new FormData();
				formData.append('image', image);
				console.log(formData);
				fetch("http://localhost:5000/editprofilepic", {
					method: "POST",
					body: formData
				}).then(response => response.json()).then(data => {
					console.log(data);
				});
			}
		}
	}

	const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;

	function addImage(image) {
		addImage(image);
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
						onChange={saveImage}
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
					{errObject}
					<button type="submit" className="post-submit-btn" onClick={(e) => onSubmit(e)}>Create Post</button>
				</form>

				<a href="../../login" className="return-link">go back</a>
			</div>
		</div>
	);
}

function isFormValid({ postTitle, postContent, updateErrorMessage }) {
	if (postTitle === "") {
		updateErrorMessage("Please enter a title for your post.");
	} else if (postContent === "") {
		updateErrorMessage("Post body cannot be empty.");
	} else {
		return true;
	}
	return false;
}

function ErrorBubble({ message }) {
	return (
		<div className="post-error-bubble">
			<p className="post-error-message">{message}</p>
		</div>
	)
}