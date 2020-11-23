import React, { useState, useEffect } from "react";

import "./message.css";

export default function Comment({
  messageId
}) {

  const [errorMessage, updateErrorMessage] = useState("");
  const [messageData, setMessageData] = useState([]);

  let access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  const endpoint = "http://localhost:5000/message/" + messageId;

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
  }, [])

  const { date_created, content, sender} = messageData;

  return (
    <div>
        <div className="message-sender-container">
            {/* align these better later */}
            <p className="message-text">{date_created}</p>
            <p className="message-content">{content}</p>
        </div>
    </div>
  );
}