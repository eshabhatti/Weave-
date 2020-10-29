import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

import NavBar from "../../../Shared_Components/NavBar";
import Sidebar from '../../../Shared_Components/Sidebar/Sidebar';
import Post from "../../../Shared_Components/Post/Post";

import './topicpage.css';

export default function TopicPosts() {
  const {topic_name: topic } = useParams();
  const [postData, setPostData] = useState([]);
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }
  useEffect(() => {
    const endpoint = "http://localhost:5000/topicposts/"
    fetch(endpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify({
        start: 0,
        end: 5,
		topic: topic
      })
    }).then(response => response.json()).then(data => {
	  const { pull_list: post_ids } = data;
      setPostData(post_ids);
    }).catch(err => {
      console.log(err);
      alert("Error in console");
    });
  }, []);

  let postsContent = [];
  
  postData.forEach((postId) => {
    postsContent.push(<Post postId={postId} userName={"sahilkapur"} />)
  });

  if (postsContent.length === 0) {
    postsContent = <p>Posts are loading</p>;
  }

  return (
    <div>
      <NavBar />
      <div className="topic-container">
		<Sidebar />
        {/* List of posts */}
        <div className="topic-display">
		  <h1 className="topic-heading">Welcome to the <b>{topic}</b> topic:</h1>
          {postsContent}
		  <a href="javascript:history.back()" className="topic-return">go back</a>
        </div>
      </div>
    </div>
  );
}