import React, { useState } from "react";
import "./register.css";

export default function Login() {
  const [loginName, updateLoginName] = useState("");
  const [email, updateEmail] = useState("");
  const [password, updatePassword] = useState("");
  const [confirmPassword, updateConfirmPassword] = useState("");
  const [isOverThirteen, updateAgeCheck] = useState(false);

  const [errorMessage, updateErrorMessage] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    const body = {
      username: loginName,
      password,
      email,
      confirmPassword,
      isOverThirteen,
    }
    /*
     * post to backend
     */
    const endpoint = "";
    // fetch(endpoint).then(response => response.json()).then(data => {
    //   if (data.errorMessage) {
    //     updateErrorMessage(data.errorMessage);
    //   }
    // });
    updateErrorMessage("Incorrect username or password");
    alert(JSON.stringify(body));
  }

  const errObject = errorMessage !== "" ? <ErrorBubble message="Incorrect username or password" /> : null;

  return (
    <div>
      <h1 className="register-page-title">Join the conversation</h1>
      <div className="register-container">
        <img src="./img/weave-icon.svg" className="register-icon" />
        <form className="register-form">
          <label className="register-form-label">username</label>
          <input
            value={loginName}
            onChange={e => {
              updateLoginName(e.target.value);
              updateErrorMessage("");
            }} className="register-form-input"
          />

          <label className="register-form-label">email</label>
          <input
            value={email}
            onChange={e => {
              updateEmail(e.target.value);
              updateErrorMessage("");
            }} className="register-form-input"
          />

          <label className="register-form-label">password</label>
          <input
            value={password}
            onChange={e => {
              updatePassword(e.target.value);
              updateErrorMessage("");
            }}
            type="password"
            className="register-form-input" />

          <label className="register-form-label">confirm password</label>
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
          <label className="register-checkbox-label">I am over 13 years old</label>


          <button type="submit" className="register-submit-btn" onClick={(e) => onSubmit(e)}>create account</button>

        </form>
        {errObject}
        <a href="login" className="register-link">existing user login</a>
      </div>
    </div>
  )
}

function ErrorBubble({ message }) {
  return (
    <div className="register-error-bubble">
      <p className="register-error-message">{message}</p>
    </div>
  )
}