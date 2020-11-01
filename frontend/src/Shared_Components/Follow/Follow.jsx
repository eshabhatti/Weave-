import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

export default function Follow({ followType, toFollow, initialState, className }) {
  const [followed, setFollowed] = useState(initialState);

  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = '/login';
  }
  
  useEffect(() => {
	  setFollowed(initialState)
	  
  }, [initialState]);
  
  const followpoint = "http://localhost:5000/follow" + followType + "/";
  const follow = (value) => {
    const body = {
      following: toFollow,
      type: value,
    }
    fetch(followpoint, {
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
      const { followState } = data;
      setFollowed(followState);
    }).catch(err => {
      console.error(err);
    });
  }

  return (
    <div>
      {followed == 0 ? (
        <button type="button" className={className} onClick={(e) => follow(1)}>Follow</button>
      ) : (
          <button type="button" className={className} onClick={(e) => follow(-1)}>Unfollow</button>
        )}
    </div>
  );




}