import React, { useState, useEffect } from "react";
import NavBar from "../../Shared_Components/NavBar";
import Post from "../../Shared_Components/Post";
import './savedposts.css';

export default function SavedPosts() {
  const [postData, setPostData] = useState([]);
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }
  useEffect(() => {
    const endpoint = "http://localhost:5000/savedposts/"
    fetch(endpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify({
        start: 0,
        end: 5
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
      <div className="saved-posts-page-content">
        {/* List of posts */}
        <h1 className="saved-posts-heading">Your saved posts</h1>
        <div className="saved-posts-container">
          {postsContent}
        </div>
        <a href="javascript:history.back()" className="saved-posts-return">go back</a>
      </div>
    </div>
  );
}