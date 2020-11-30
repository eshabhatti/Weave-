import React, { useState, useEffect } from "react";

import "./message.css";

export default function Message({
  messageId
}) {

  const [errorMessage, updateErrorMessage] = useState("");
  const [messageData, setMessageData] = useState([]);

  let access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  {/*Delete Message Function*/}
  const delete_message = (event) => {
    
    event.preventDefault();
    const JSONbody = {
			message_id: messageId,
		}

    const deletepoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/deletemessage/";
    fetch(deletepoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(JSONbody)
    }).then(response => response.json()).then(data => {
      // Update message feed with deletion?
    }).catch(err => {
      console.error(err);
    });
  }

  const endpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/message/" + messageId + "/";

  {/* renders the post with fetch data and the states of the save and voting buttons */ }
  useEffect(() => {
    fetch(endpoint, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
    }).then(response => response.json()).then(data => {
      if (data.error_message) {
        updateErrorMessage(data.error_message);
        window.location = "/404"
      }
      /* catches jwt errors that don't use the form "error_message:" */
      setMessageData(data);
    }).catch(err => {
      console.error(err);

    });
  }, [messageId])

  const { date_created, content, receiver, sender, username} = messageData;
  return (
    <div>
        { username === receiver ? (
          <div className="message-receiver-container">
            <p className="message-text">{date_created}</p>
            <p className="message-text">from: {sender}</p>
            <p className="message-content">{content}</p>
            <button className="message-delete" onClick={(e) => delete_message(e)}>Delete this message</button>
          </div>
        ) : (
          <div className="message-sender-container">
            <p className="message-text">{date_created}</p>
            <p className="message-text">sent to: {receiver}</p>
            <p className="message-content">{content}</p>
            <button className="message-delete" onClick={(e) => delete_message(e)}>Delete this message</button>
          </div>
          )}
        
    </div>
  );
}