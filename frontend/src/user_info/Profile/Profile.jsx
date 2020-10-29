import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './profile.css';

// import components
import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Post from '../../Shared_Components/Post/Post';
import Comment from '../../Shared_Components/Comment/Comment';
import Feed from "../../Shared_Components/Feed/Feed";

export default function Profile() {
  const { username: pageUsername } = useParams();
  const [errorMessage, updateErrorMessage] = useState('');
  const [userData, setUserData] = useState([]);
  // replace with API call to /secure to validate token
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = '/login';
  }

  useEffect(() => {
    fetch('http://localhost:5000/profile/' + pageUsername, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
    }).then(response => response.json()).then(data => {
      //TODO- check what data.msg does
      const errorMessage = data.error_message || data.msg;
      if (errorMessage) {
        updateErrorMessage(errorMessage);
      }
      setUserData(data);
    }).catch(err => {
      console.error(err);
    });
  }, []);
  
  useEffect(() => {
    // TODO - handle errors
  }, [errorMessage]);

  return (
    <div>
      <NavBar />
      <div className="profile-container">
        <Sidebar />
        <UserInfo userData={userData} pageUsername={pageUsername} />
        <UserPosts pageUsername={pageUsername} />
      </div>
    </div>
  );
}

function UserInfo({ userData, pageUsername }) {
  const { user_bio, user_pic, follower_count, first_name, last_name, date_joined, username } = userData;
  return (
    <div className="profile-container">
      <div className="profile-info">
        <ProfilePicture user_pic={user_pic} />
        <h1 className="profile-name">{first_name + " " + last_name}</h1>
        <p className="profile-username">{pageUsername}</p>
        <EditProfileButton pageUsername={pageUsername} username={username} />
        <button type="button" className="profile-follow-button">Follow</button>
        <p className="profile-followers">{follower_count} Followers</p>
        <p className="profile-following"># Following</p>
        <h1 className="profile-bio-title">Bio</h1>
        <p className="profile-bio">{user_bio}</p>
        <h1 className="profile-about-title">About</h1>
        <p className="profile-about">{date_joined}</p>
      </div>
    </div>
  );
}

function EditProfileButton({ pageUsername, username }) {
  const canUserEditProfile = (username === pageUsername);
  return canUserEditProfile ?
    <button onClick={() => window.location.href = '/editprofile'} type="button" className="profile-follow-button">Edit Profile</button> : null;
}

function ProfilePicture({ user_pic }) {
  return user_pic == null ? (
    <img src="/img/weave-icon.svg" className="profile-icon" alt="" />
  ) : (
      <img src={user_pic} className="profile-icon" alt="" />
    );
}

function UserPosts({pageUsername}) {
  return (
    <div className="profile-choice">
      <div className="profile-buttons">
        <button type="button" className="profile-posts-button">Posts</button>
        <button type="button" className="profile-interactions-button">Interactions</button>
      </div>
      <div className="profile-display">
		<Feed route="userposts/" username={pageUsername} />
      </div>
    </div>
  );
}