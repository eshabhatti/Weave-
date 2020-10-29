import React, { useState, useEffect } from "react";
import NavBar from "../../Shared_Components/NavBar";
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Feed from "../../Shared_Components/Feed/Feed";

import './savedposts.css';

export default function SavedPosts() {
  
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  return (
    <div>
        <NavBar />
		<div className="saved-posts-container">
			<Sidebar />
			<Feed route="savedposts/" />
		</div>
    </div>
  );
}