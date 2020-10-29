import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

import NavBar from "../../../Shared_Components/NavBar";
import Sidebar from '../../../Shared_Components/Sidebar/Sidebar';
import Post from "../../../Shared_Components/Post/Post";
import Feed from "../../../Shared_Components/Feed/Feed";

import './topicpage.css';

export default function TopicPosts() {
  const {topic_name: topic } = useParams();
  const [postData, setPostData] = useState([]);
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }


  return (
    <div>
      <NavBar />
      <div className="topic-container">
		<Sidebar />
        {/* List of posts */}
        <div className="topic-display">
		  <h1 className="topic-heading">Welcome to the <b>{topic}</b> topic:</h1>
          <Feed route="topicposts/" topic={topic} />
		  <a href="javascript:history.back()" className="topic-return">go back</a>
        </div>
      </div>
    </div>
  );
}