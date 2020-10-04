import React, { useState } from "react";
import "./notfound.css";

export default function NotFound() {
  return (
	  <div className="error-box">
		<img className="error-image" src="./img/weave-icon.svg"></img>
		<h2 className="error-code">404: Page Not Found</h2>
		<p className="error-message">Looks like you got tangled up, this page doesn't exist!</p>
	  </div>
  )
}