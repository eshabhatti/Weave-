import React, { useState, useEffect } from "react";
import Message from '../Chat/Message'

import "./display.css";

export default function ChatDisplay({sender, receiver}) {
    const [messageContent, setMessageContent] = useState([]);
    const [messageData, setMessageData] = useState([]);
    const access_token = localStorage.getItem('access_token');
    if (access_token == null) {
      window.location = "/login"
    }
  
    useEffect(() => {
      const endpoint = "http://localhost:5000/directmessages"
      //console.log(endpoint)
      const body = {
        receiver: receiver
      }
      fetch(endpoint, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + access_token
        },
        body: JSON.stringify(body)
      }).then(response => response.json()).then(data => {
        const { pull_list: message_ids, rowCount: rowCount } = data;
        setMessageData(message_ids);
      }).catch(err => {
        console.log(err);
      });
    }, []);
    
    useEffect(() => {
      let tester = [];
      if (messageData) {
        messageData.forEach((messageId) => {
          console.log(messageId)
          tester.push(<Message key={messageId} messageId={messageId} user1={sender}/>)
        });
        setMessageContent(tester);
        if (messageContent.length === 0) {
          tester = <p>No Posts!</p>;
        }
      }
    }, [messageData])
  
    return (
      <div className="messages-display">
        {messageContent}
      </div>
    );
  }