import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

export default function Follow({ followType, toFollow, initialState, className, refresh }) {
  const [followed, setFollowed] = useState(initialState);

  let access_token = localStorage.getItem('access_token');
  if (!access_token) {
    access_token = "";
  }
  
  useEffect(() => {
	  setFollowed(initialState)
	  
  }, [initialState]);
  
  const followpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/follow" + followType + "/";
  const follow = (value) => {
	
	if (access_token == "") {
	  window.location = "/login";
	}
	  
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
      const { followState } = data;
      refresh();
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