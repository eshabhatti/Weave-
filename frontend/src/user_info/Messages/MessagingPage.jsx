import React, { useState, useEffect } from 'react';

import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Feed from "../../Shared_Components/Feed/Feed";
import './messagingpage.css';

export default function MessagingPage(){	
  const [message, uploadChatMessage] = useState("")
  const [receiver, setReceiver] = useState("")
  const [reload, setReload] = useState(false)
  const [errorMessage, updateErrorMessage] = useState("");
  const [successMessage, updateSuccessMessage] = useState("");
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login";
  }

  const onSubmit = (event) => {
    event.preventDefault();
    if (isMessageValid({ message: message, receiver: receiver, updateErrorMessage })) {
      const body = {
        content: message,
        receiver: receiver,
      }
      console.log(body)
      const endpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/createmessage/";
      fetch(endpoint, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + access_token
        },
        body: JSON.stringify(body)
      }).then(response => response.json()).then(data => {
        if (data.error_message) {
          updateErrorMessage(data.error_message);
        } else {
		  updateSuccessMessage("Message Sent");
        }
      }).catch(err => {
        console.log(err);
        alert("error: check console for details");
	  });
	  setReload(reload => !reload)
    }
  }

  const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;
  const successObject = successMessage != "" ? <SuccessBubble message={successMessage} /> : null;

	return (
		<div>
		  <NavBar />
		  <div className="chat-page-container">
			<Sidebar />
			<div className="chat-page-content">
			  <h1 className="chat-page-feed-header">Your message feed</h1>
			  <div className="chat-page-feed">
			  	<Feed route="allmessages/" elementType="messages" reloadFlag={reload}/>
			  </div>
			  <h2 className="chat-page-form-header">Write a message</h2>
			  <form className="chat-page-form">
				<label className="chat-page-form-label">Message</label>
				<textarea
				  value={message}
				  onChange={e => {
					uploadChatMessage(e.target.value);
					updateErrorMessage("");
					updateSuccessMessage("");
				  }} 
				  className="chat-message-input"
				/>
				<label className="chat-page-form-label">Receiver</label>
				<input
				  value={receiver}
				  onChange={e => {
					setReceiver(e.target.value);
					updateErrorMessage("");
				  }} className="chat-page-form-input"
				/>
				<button type="submit" className="chat-submit-button" onClick={(e) => onSubmit(e)}>Send Message</button>
				{errObject}
			  	{successObject}
			  </form>
			</div>
		  </div>
		</div>
	  );
	}
	
	function isMessageValid({ message, receiver, updateErrorMessage }) {
	  if (message === "") {
		updateErrorMessage("Please enter a message.");
	  }
	  else if (receiver === "") {
		updateErrorMessage("Please enter a receiver.");
	  }
	  else if (message.length > 500) {
		updateErrorMessage("Message cannot exceed 500 characters.");  
	  }
	  else {
		return true;
	  }
	  return false;
	}
	
	function ErrorBubble({ message }) {
	  return (
		<div className="chat-error-bubble">
		  <p className="chat-error-message">{message}</p>
		</div>
	  )
	}
	
	function SuccessBubble({ message }) {
	return (
		<div className="success-error-bubble">
			<p className="post-error-message">{message}</p>
		</div>
	)
}
