import React, { useState } from "react";
import "./register.css";

//module.exports(isFormValid);
//module.exports(Login);

export default function Login() {
  const [loginName, updateLoginName] = useState("");
  const [firstName, updateFirstName] = useState("");
  const [lastName, updateLastName] = useState("");
  const [email, updateEmail] = useState("");
  const [password, updatePassword] = useState("");
  const [confirmPassword, updateConfirmPassword] = useState("");
  const [isOverThirteen, updateAgeCheck] = useState(false);

  const [errorMessage, updateErrorMessage] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    if (isFormValid({ loginName, firstName, lastName, password, confirmPassword, email, isOverThirteen,updateErrorMessage })) {
      const body = {
        username: loginName,
        firstName: firstName,
        lastName: lastName,
        password: password,
        email: email,
      }
      /*
       * post to backend
       */
      const endpoint = process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000" + "/register/";
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
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          window.location = "profile/" + loginName;
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
      <h1 className="register-page-title">Join the conversation</h1>
      <div className="register-container">
        <img src="./img/weave-icon.svg" className="register-icon" alt="" />
        <form className="register-form">
          <label className="register-form-label">Username</label>
          <input
            value={loginName}
            onChange={e => {
              updateLoginName(e.target.value);
              updateErrorMessage("");
            }} className="register-form-input"
          />

          <label className="register-form-label">First Name</label>
          <input
            value={firstName}
            onChange={e => {
              updateFirstName(e.target.value);
              updateErrorMessage("");
            }} className="register-form-input"
          />

          <label className="register-form-label">Last Name</label>
          <input
            value={lastName}
            onChange={e => {
              updateLastName(e.target.value);
              updateErrorMessage("");
            }} className="register-form-input"
          />
          
          <label className="register-form-label">Email</label>
          <input
            value={email}
            onChange={e => {
              updateEmail(e.target.value);
              updateErrorMessage("");
            }} className="register-form-input"
          />

          <label className="register-form-label">Password</label>
          <input
            value={password}
            onChange={e => {
              updatePassword(e.target.value);
              updateErrorMessage("");
            }}
            type="password"
            className="register-form-input" />

          <label className="register-form-label">Confirm Password</label>
          <input
            value={confirmPassword}
            onChange={e => {
              updateConfirmPassword(e.target.value);
              updateErrorMessage("");
            }}
            type="password"
            className="register-form-input"
          />

          <input
            className="register-checkbox"
            type="checkbox"
            checked={isOverThirteen}
            onChange={e => {
              updateAgeCheck(!isOverThirteen);
              updateErrorMessage("");
            }}
          />
          <label className="register-checkbox-label">I am 13 years old or older</label>


          <button type="submit" className="register-submit-btn" onClick={(e) => onSubmit(e)}>create account</button>

        </form>
        {errObject}
        <a href="login" className="register-link">existing user login</a>
      </div>
    </div>
  )
}

function isFormValid({ loginName, firstName, lastName, password, confirmPassword, isOverThirteen, email, updateErrorMessage }) {
  if (loginName === "") {
    updateErrorMessage("Please enter a username.");
  } else if (firstName === "") {
    updateErrorMessage("Please enter your first name.");
  } else if (lastName === "") {
    updateErrorMessage("Please enter your last name.");
  } else if (email === "") {
    updateErrorMessage("Please enter your email.");
  } else if (password === "") {
    updateErrorMessage("Please enter a password.");
  } else if (password !== confirmPassword) {
    updateErrorMessage("The passwords do not match.")
  }	else if (password.length < 6) {
	updateErrorMessage("Password should be 6 character minimum.")
  } else if (!isOverThirteen) {
    updateErrorMessage("You must be 13 or older to join Weave.")
  } else {
    return true;
  }
  return false;
}

//module.exports(isFormValid);

function ErrorBubble({ message }) {
  return (
    <div className="register-error-bubble">
      <p className="register-error-message">{message}</p>
    </div>
  )
}