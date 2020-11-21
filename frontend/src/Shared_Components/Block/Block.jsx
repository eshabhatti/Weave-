import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

export default function Block({ toBlock, initialState, className, refresh }) {
  const [blocked, setBlocked] = useState(initialState);

  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = '/login';
  }
  
  useEffect(() => {
	  setBlocked(initialState)
	  
  }, [initialState]);
  
  const blockpoint = "http://localhost:5000/blockuser/";
  const block = (value) => {
    const body = {
      user_blocked: toBlock,
      type: value,
    }
    fetch(blockpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      if (data.msg) {
        window.location = "/login"
      }
      const { blockState } = data;
      refresh();
      setBlocked(blockState);
    }).catch(err => {
      console.error(err);
    });
  }

  return (
    <div>
      {blocked == 0 ? (
        <button type="button" className={className} onClick={(e) => block(1)}>Block</button>
      ) : (
          <button type="button" className={className} onClick={(e) => block(-1)}>Unblock</button>
        )}
    </div>
  );




}