import React, { useState } from "react";
import "./login.css";

//module.exports(isFormValid);
//module.exports(Login);

export default function Login() {
  const [loginName, updateLoginName] = useState("");
  const [password, updatePassword] = useState("");
  const [errorMessage, updateErrorMessage] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    if (isFormValid({ loginName, password, updateErrorMessage })) {
      const body = {
        username: loginName,
        password: password
      }
      /*
       * post to backend
       */
      const endpoint = "http://localhost:5000/login/";
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
          const { access_token, refresh_token, username } = data;
          console.log(access_token);
          localStorage.setItem('data', data);
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          window.location = "profile/" + username;
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
      <h1 className="login-page-title">Join the conversation</h1>
      <div className="login-container">
        <img src="./img/weave-icon.svg" className="login-icon" alt="" />
        <form className="login-form">
          <label className="login-form-label">username/email</label>
          <input
            value={loginName}
            onChange={e => {
              updateLoginName(e.target.value);
              updateErrorMessage("");
            }} className="login-form-input"
          />

          <label className="login-form-label">password</label>
          <input
            value={password}
            onChange={e => {
              updatePassword(e.target.value);
              updateErrorMessage("");
            }}
            type="password"
            className="login-form-input" />
          <button type="submit" className="login-submit-btn" onClick={(e) => onSubmit(e)}>login</button>

        </form>
        {errObject}
        <a href="register" className="login-link">create an account</a>
        <a href="profile/newuser2" className="login-link">forgot password</a>
      </div>
    </div>
  )
}

function isFormValid({ loginName, password, updateErrorMessage }) {
  if (loginName === "") {
    updateErrorMessage("Please enter your username or email.");
  } else if (password === "") {
    updateErrorMessage("Please enter your password.");
  } else {
    return true;
  }
  return false;
}

function ErrorBubble({ message }) {
  return (
    <div className="login-error-bubble">
      <p className="login-error-message">{message}</p>
    </div>
  )
}