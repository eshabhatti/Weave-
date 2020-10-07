import React, { useState } from "react";
import { Navbar, Nav, Form } from 'react-bootstrap';
import ImageUploader from 'react-images-upload';
import "./editprofile.css";

//module.exports(isFormValid);
//module.exports(Login);

export default function EditProfile() {
  const [username, updateUsername] = useState("");
  const [firstName, updateFirstName] = useState("");
  const [lastName, updateLastName] = useState("");
  const [bio, updateBio] = useState("");
  const [errorMessage, updateErrorMessage] = useState("");
  const [image, saveImage] = useState(null);
  const [access_token, updateToken] = useState(localStorage.getItem('access_token'));
  if (access_token == null) {
    window.location = "/login"
  }

  const onSubmit = (event) => {
    event.preventDefault();
    if (isFormValid({ username, firstName, lastName, bio, access_token })) {
      const body = {
        newusername: username,
        firstname: firstName,
        lastname: lastName,
        biocontent: bio,
      }
      /*
       * post to backend
       */
      const endpoint = "http://localhost:5000/editprofile/";
      fetch(endpoint, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + access_token
        },
        body: JSON.stringify(body)
      }).then(response => response.json()).then(data => {
        if (data.msg) {
          window.location = "/login"
        }
        if (data.error_message) {
          updateErrorMessage(data.error_message);
        } else {
          const { access_token, refresh_token } = data;
		  localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
		  updateToken(localStorage.getItem('access_token'));
        }
      }).catch(err => {
        console.error(err);
        alert("error: check console for details");
      });

	}
	
	if (image !== null && image.length > 0) {
	  const formData = new FormData();
	  const lastImg = image[image.length - 1];
	  formData.append('image', lastImg, lastImg.name);
	  fetch("http://localhost:5000/editprofilepic/", {
		method: "POST",
		headers: {
		  'Authorization': 'Bearer ' + access_token
		},
		body: formData
	  }).then(response => response.json()).then(data => {
		console.log(data);
	  });
	}
  }

  const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;

  return (
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
      <h1 className="edit-page-title">Update Your Information</h1>
      <div className="edit-container">
        <img src="./img/weave-icon.svg" className="login-icon" alt="" />
        <form className="edit-form">

          <label className="edit-form-label">New Username</label>
          <input
            value={username}
            onChange={e => {
              updateUsername(e.target.value);
              updateErrorMessage("");
            }} className="edit-form-input"
          />

          <label className="edit-form-label">First Name</label>
          <input
            value={firstName}
            onChange={e => {
              updateFirstName(e.target.value);
              updateErrorMessage("");
            }}
            className="edit-form-input"
          />
          <label className="edit-form-label">Last Name</label>
          <input
            value={lastName}
            onChange={e => {
              updateLastName(e.target.value);
              updateErrorMessage("");
            }}
            className="edit-form-input"
          />

          <label className="edit-form-label">Bio</label>
          <textarea
            value={bio}
            onChange={e => {
              updateBio(e.target.value);
              updateErrorMessage("");
            }}
            className="bio-form-input"
          />

          <label className="edit-form-label">Profile Picture</label>
          <ImageUploader
            withIcon={true}
            imgExtension={['.jpg', 'jpeg', '.gif', '.png', '.gif']}
            maxFileSize={10000000}
            buttonText='Select your profile picture.'
            className="profile-pic-upload"
            onChange={saveImage}
          />


          <button type="submit" className="edit-update-btn" onClick={(e) => onSubmit(e)}>Update</button>

        </form>
        {errObject}
        <a href="login" className="edit-link">go back</a>
      </div>
    </div>
  )
}

function isFormValid({ username, firstName, lastName, bio, access_token }) {
  if (!access_token) {
    alert("Invalid access token");
    return false;
  }
  return true;
}

function ErrorBubble({ message }) {
  return (
    <div className="edit-error-bubble">
      <p className="edit-error-message">{message}</p>
    </div>
  )
}