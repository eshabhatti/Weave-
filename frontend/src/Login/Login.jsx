import React, { useState } from "react";
import "./login.css";

export default function Login() {
  const [loginName, updateLoginName] = useState("");
  const [password, updatePassword] = useState("");

  const onSubmit = (event) => {
    event.preventDefault();
    const body = {
      username: loginName,
      password: password
    }
    console.log(body);
    /*
     * post to backend
     */
    // fetch();
    alert(JSON.stringify(body));
  }

  return (
    <div>
      <h1 className="login-page-title">Join the conversation</h1>
      <div className="login-container">
        <img src="./img/weave-icon.svg" className="login-icon" />
        <form className="login-form">
          <label className="login-form-label">username/email</label>
          <input
            value={loginName}
            onChange={e => updateLoginName(e.target.value)} className="login-form-input"
          />

          <label className="login-form-label">password</label>
          <input
            value={password}
            onChange={e => updatePassword(e.target.value)}
            type="password"
            className="login-form-input" />
          <button type="submit" className="login-submit-btn" onClick={(e) => onSubmit(e)}>login</button>

        </form>
        <a href="#" className="login-link">create an account</a>
        <a href="#" className="login-link">forgot password</a>
      </div>
    </div>
  )
}