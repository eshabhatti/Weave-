import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

import NavBar from "../../../Shared_Components/NavBar";
import Sidebar from '../../../Shared_Components/Sidebar/Sidebar';
import Post from "../../../Shared_Components/Post/Post";
import Feed from "../../../Shared_Components/Feed/Feed";
import Follow from "../../../Shared_Components/Follow/Follow";

import './topicpage.css';

export default function TopicPosts() {
  const {topic_name: topic } = useParams();
  const [postData, setPostData] = useState([]);
  const [topicData, setTopicData] = useState([]);
  let access_token = localStorage.getItem('access_token');
  if (!access_token) {
    access_token = "";
  }

	useEffect(() => {
		fetch((process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + '/topic/' + topic, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + access_token
			},
		}).then(response => response.json()).then(data => {
			//TODO- check what data.msg does
			const errorMessage = data.error_message || data.msg;
			setTopicData(data);
		}).catch(err => {
		  console.error(err);
		});
  }, []);


  const { follower_count, topic_name, follow } = topicData;
  return (
    <div>
      <NavBar />
      <div className="topic-container">
		  <Sidebar />
        {/* List of posts */}
        <div className="topic-display">
		      <h1 className="topic-heading">Welcome to the <b>{topic}</b> topic:</h1>
		      <p className="topic-followers">Topic Followers: {follower_count}</p>
		      <Follow className="topic-follow-button" followType="topic" toFollow={topic} initialState={follow}/>
          <Feed route="topicposts/" topic={topic} />
		      <a href="javascript:history.back()" className="topic-return">go back</a>
        </div>
      </div>
    </div>
  );
}