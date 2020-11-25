import React, { useState } from "react";
import { useParams } from 'react-router-dom';
import NavBar from "../Shared_Components/NavBar";
import Sidebar from '../Shared_Components/Sidebar/Sidebar';
import ChatDisplay from '../Chat/ChatDisplay'

import "./chat.css";

//module.exports(isFormValid);
//module.exports(Login);

export default function Chat() {
  const { username: sender } = useParams();

  const [message, uploadChatMessage] = useState("")
  const [receiver, setReceiver] = useState("")
  const [errorMessage, updateErrorMessage] = useState("");
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  const onSubmit = (event) => {
    event.preventDefault();
    if (isMessageValid({ message: message, receiver: receiver, updateErrorMessage })) {
      const body = {
        content: message,
        receiver: receiver,
      }
      console.log(body)
      const endpoint = process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000" + "/createmessage/";
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
      <NavBar />
      <div className="chat-container">
        <Sidebar />
        <div className="chat-content">
          <ChatDisplay sender={sender} />
          <form className="chat-form">
            <label className="chat-form-label">Message</label>
            <input
              value={message}
              onChange={e => {
                uploadChatMessage(e.target.value);
                updateErrorMessage("");
              }} className="chat-form-input"
            />
            <label className="chat-form-label">Receiver</label>
            <input
              value={receiver}
              onChange={e => {
                setReceiver(e.target.value);
                updateErrorMessage("");
              }} className="chat-form-input"
            />
            <button type="submit" className="chat-submit-btn" onClick={(e) => onSubmit(e)}>Send Message</button>
          </form>
          {errObject}
        </div>
      </div>
    </div>
  )
}

function isMessageValid({ message, receiver, updateErrorMessage }) {
  if (message === "") {
    updateErrorMessage("Please enter a message.");
  }
  else if (receiver === "") {
    updateErrorMessage("Please enter a receiver.");
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