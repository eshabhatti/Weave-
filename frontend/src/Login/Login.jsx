import React from "react";
import "./login.css";

export default function Login(props) {
  return (
    <div>
      <h1 className="login-page-title">Join the conversation</h1>
      <div className="login-container">
        <img src="./img/weave-icon.svg" className="login-icon" />
        <form className="login-form">
          <label className="login-form-label">username/email</label>
          <input className="login-form-input"/>
          <label className="login-form-label">password</label>
          <input type="password" className="login-form-input"/>
        </form>
        <button className="login-submit-btn">login</button>
        <a href="#" className="login-link">create an account</a>
        <a href="#" className="login-link">forgot password</a>
      </div>
    </div>
  )
}