import React, { useState, useEffect } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import ImageUploader from 'react-images-upload';

import "./createpost.css";

export default function Timeline() {
	const [postContent, updatePostContent] = useState("");
	const [postTitle, updatePostTitle] = useState("");
	const [postTopic, updatePostTopic] = useState("");
	const [isAnon, updateIsAnon] = useState(0);
	const [image, saveImage] = useState(null);
	const [errorMessage, updateErrorMessage] = useState("");
	const [successMessage, updateSuccessMessage] = useState("");
	
	const access_token = localStorage.getItem('access_token');
	window.onload = isLoggedIn(access_token);

	useEffect(() => {
		fetch("http://localhost:5000/protected", {
			method: "GET",
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
			}
		}).then(response => response.json()).then(data => {
			if (!data.logged_in) {
				window.location.href="/login";
			}
		}).catch(err => {
			alert("Err in console");
			console.error(err);
		});
	}, []);

	const onSubmit = (event) => {
		event.preventDefault();
		/* More to be added for posts eventually */
		if (isFormValid({ postTitle, postContent, postTopic, updateErrorMessage, updateSuccessMessage, image })) {
			const body = {
				title: postTitle,
				content: postContent,
				anon: isAnon,
				topic: postTopic
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

					//TO-DO: make sure this is being sent on the right post
					console.log(image);
					if (image !== null && image.length > 0) {
						const formData = new FormData();
						const lastImg = image[image.length - 1];
						formData.append('image', lastImg, lastImg.name);
						fetch("http://localhost:5000/createimage/", {
							method: "POST",
							headers: {
								'Authorization': 'Bearer ' + access_token
							},
							body: formData,
						}).then(response => response.json()).then(data => {
							console.log(data);
						});
					}
					updateSuccessMessage("Post Created!")
				}
			}).catch(err => {
				console.error(err);
				alert(err);
			});

		}
	}

	const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;
	const successObject = successMessage != "" ? <SuccessBubble message={successMessage} /> : null;

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
					
					<label className="post-form-label">Post Topic</label>
					<input
						value={postTopic}
						onChange={e => {
							updatePostTopic(e.target.value);
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
						onChange={e => {
							if (isAnon == 0){
								updateIsAnon(1);
							}
							else {
								updateIsAnon(0);
							}

						}}
					/>
					<label className="post-check-label">Make this post anonymously</label>

					<button type="submit" className="post-submit-btn" onClick={(e) => onSubmit(e)}>Create Post</button>
					{errObject}
					{successObject}
				</form>

				<a href="javascript:history.back()" className="return-link">go back</a>
			</div>
		</div>
	);
}

function isFormValid({ postTitle, postContent, postTopic, updateErrorMessage, updateSuccessMessage, image }) {
	updateSuccessMessage("")
	updateErrorMessage("")
	if (postTitle === "") {
		updateErrorMessage("Please enter a title for your post.");
	} else if (postContent === "") {
		updateErrorMessage("Post body cannot be empty.");
	} else if (postContent.length > 750 && image === null) {
		updateErrorMessage("Post body cannot exceed 750 characters");
	} else if (postContent.length > 100 && image !== null) {
		updateErrorMessage("Captions cannot exceed 100 characters");
	} else if (postTitle.length > 100) {
		updateErrorMessage("Post title cannot exceed 100 characters");
	} else if (postTopic.length > 20) {
		updateErrorMessage("Post topic cannot exceed 20 characters");
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

function SuccessBubble({ message }) {
	return (
		<div className="success-error-bubble">
			<p className="post-error-message">{message}</p>
		</div>
	)
}

function isLoggedIn(access_token) {
	if (access_token == "null") {
		window.location = "/login"
	}
}