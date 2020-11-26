import React, { useState, useEffect } from "react";
import NavBar from "../../Shared_Components/NavBar";
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Feed from "../../Shared_Components/Feed/Feed";

import './savedposts.css';

export default function SavedPosts() {
  
  let access_token = localStorage.getItem('access_token');
  if (!access_token) {
    window.location = "/login";
  }

  return (
    <div>
      <NavBar />
		  <div className="saved-posts-content">
			  <Sidebar />
        <div className="saved-posts-container">
          <h1 className="saved-posts-heading">Your saved posts:</h1>
			    <Feed route="savedposts/" />
          <a href="javascript:history.back()" className="saved-posts-return">go back</a>
        </div>
		  </div>
    </div>
  );
}