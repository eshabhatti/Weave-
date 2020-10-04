import React, { useState } from "react";
//nimport "./forgotpassword.css";

export default function Login() {
  const [loginName, updateLoginName] = useState("");
  const [code, updatePassword] = useState("");
  const [errorMessage, updateErrorMessage] = useState("");
  const email = useState("");
  let newUserName;
  
  const onSubmit = (event) => {
    event.preventDefault();
   /* const body = {
      email: loginName,
      password: password
    }*/
    /*
     * post to backend
     */
    const endpoint = "";
    // fetch(endpoint).then(response => response.json()).then(data => {
    //   if (data.errorMessage) {
    //     updateErrorMessage(data.errorMessage);
    //   }
    // });
    updateErrorMessage("Incorrect code");
    //alert(JSON.stringify(body));
  }

  const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;

  return (
    <div>
      <h1 className="forgotpassword-page-title">Join the conversation</h1>
      <div className="password-container">
        <img src="./img/weave-icon.svg" className="password-icon" />
        <form className="password-form">
          <label className="password-form-label">username/email</label>
          <input
            
           className="password-form-input"
          />

          <label className="password-form-label">password</label>
          <input
            type="password"
            className="password-form-input" />
          <button type="submit" className="password-submit-btn" onClick={(e) => onSubmit(e)}>login</button>
        </form>
        {errObject}
      </div>
    </div>
  )
}

function ErrorBubble({ message }) {
  return (
    <div className="code-error-bubble">
      <p className="code-error-message">{message}</p>
    </div>
  )
}
