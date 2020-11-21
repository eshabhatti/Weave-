import React, { useState } from "react";
import "./notfound.css";

export default function Blocked() {
  return (
	  <div className="error-box">
		<img className="error-image" src="./img/weave-icon.svg"></img>
		<h2 className="error-code">Blocked: Page Not Accessible</h2>
		<p className="error-message">A user has blocked you from viewing this content.</p>
	  </div>
  )
}