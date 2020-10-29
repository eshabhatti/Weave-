import React, { useState, useEffect } from "react";
import NavBar from "../../../Shared_Components/NavBar";
import Sidebar from '../../../Shared_Components/Sidebar/Sidebar';
import Post from "./../../../Shared_Components/Post/Post";
import Feed from "../../../Shared_Components/Feed/Feed";
import './timeline.css';

export default function TimelinePosts() {
  
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  return (
    <div>
      <NavBar />
      <div className="timeline-container">
        {/* List of posts */}
		<Sidebar />
        <div className="timeline-display">
		  <h1 className="timeline-heading">Your timeline:</h1>
          <Feed route="timeline"/>
		  <a href="javascript:history.back()" className="timeline-return">go back</a>
        </div>        
      </div>
    </div>
  );
}