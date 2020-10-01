import React, { useState } from "react";
import "./editprofile.css";

//module.exports(isFormValid);
//module.exports(Login);

export default function EditProfile() {
  const [username, updateUsername] = useState("");
  const [firstName, updateFirstName] = useState("");
  const [lastName, updateLastName] = useState("");
  const [bio, updateBio] = useState("");
  const [errorMessage, updateErrorMessage] = useState("");
  
  const onSubmit = (event) => {
    event.preventDefault();
    if (isFormValid({ username, firstName, lastName, bio })) {
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
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
      }).then(response => response.json()).then(data => {
        if (data.error_message) {
          updateErrorMessage(data.error_message);
        } else {
          const { access_token, refresh_token } = data;
        }
      }).catch(err => {
        console.error(err);
        alert("error: check console for details");
      });
    }
  }

  const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;

  return (
    <div>
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
          <input
            value={bio}
            onChange={e => {
              updateBio(e.target.value);
              updateErrorMessage("");
            }}
            className="bio-form-input" 
		  />
          
		  <button type="submit" className="edit-update-btn" onClick={(e) => onSubmit(e)}>Update</button>

        </form>
        {errObject}
        <a href="login" className="edit-link">go back</a>
      </div>
    </div>
  )
}

function isFormValid({ username, firstName, lastName, bio }) {
  return true;
}

function ErrorBubble({ message }) {
  return (
    <div className="edit-error-bubble">
      <p className="edit-error-message">{message}</p>
    </div>
  )
}