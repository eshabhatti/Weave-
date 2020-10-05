import React, { useState, useEffect } from "react";
import NavBar from "../../Shared_Components/NavBar";
import Post from "../../Shared_Components/Post";

export default function SavedPosts() {
  const [postIdList, updatePosts] = useState([]);

  useEffect(() => {
    const endpoint = "https://localhost:5000/savedposts/"
    fetch(endpoint).then(response => response.json()).then(data => {
      updatePosts(data);
    }).catch(err => {
      console.log(err);
      alert("Error in console");
    });
  }, []);

  let postsContent = [];

  postIdList.forEach(postId => {
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
        <div className="saved-posts-container">
          {postsContent}
        </div>
      </div>
    </div>
  );
}