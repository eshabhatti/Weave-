import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './profile.css';

// import components
import NavBar from '../../Shared_Components/NavBar';
import Sidebar from '../../Shared_Components/Sidebar/Sidebar';
import Feed from "../../Shared_Components/Feed/Feed";
import Follow from "../../Shared_Components/Follow/Follow";

export default function Profile() {
  const { username: pageUsername } = useParams();
  const [errorMessage, updateErrorMessage] = useState('');
  const [userData, setUserData] = useState([]);
  const [contentView, setContentView] = useState(0);
  const [username, updateUsername] = useState(pageUsername);
  // replace with API call to /secure to validate token
  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = '/login';
  }

  useEffect(() => {
    if (!username) {
      fetch('http://localhost:5000/protected', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + access_token
        },
      }).then(response => response.json()).then(data => {
        // updateUsername(data.logged_in);
        window.location.href = "/profile/"+data.logged_in;
      }).catch(err => {
        console.error(err);
      });
    }
  }, []);

  useEffect(() => {
    if (username) {
      console.log(username);
      fetch('http://localhost:5000/profile/' + username, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + access_token
        },
      }).then(response => response.json()).then(data => {
        //TODO- check what data.msg does
        const errorMessage = data.error_message || data.msg;
        if (data.error_message) {
          window.location = "/404";
        }
        if (data.msg) {
          window.location = "/login";
        }
        setUserData(data);
      }).catch(err => {
        console.error(err);
      });
    }
  }, [username]);

  useEffect(() => {
    // TODO - handle errors
  }, [errorMessage]);

  useEffect(() => {

  }, [contentView])

  return (
    <div>
      <NavBar />
      <div className="profile-container">
        <Sidebar />
        <UserInfo userData={userData} pageUsername={pageUsername} />
        <UserPosts pageUsername={pageUsername} setContentView={setContentView} contentView={contentView} />
      </div>
    </div>
  );
}

function UserInfo({ userData, pageUsername }) {
  const { user_bio, user_pic, follower_count, following_count, topic_count, first_name, last_name, date_joined, username, follow} = userData;
  return (
    <div className="profile-container">
      <div className="profile-info">
        <ProfilePicture user_pic={user_pic} />
        <h1 className="profile-name">{first_name + " " + last_name}</h1>
        <p className="profile-username">{pageUsername}</p>
        <h1 className="profile-bio-title">Bio</h1>
        <p className="profile-bio">{user_bio}</p>
        <h1 className="profile-about-title">Joined</h1>
        <p className="profile-about">{date_joined}</p>
        <EditProfileButton pageUsername={pageUsername} username={username} follow={follow} />
        <p className="profile-followers">{follower_count} Followers</p>
        <p className="profile-following">{following_count} Following</p>
		<p className="profile-following">{topic_count} Topics Following</p>
      </div>
    </div>
  );
}

function EditProfileButton({ pageUsername, username, follow }) {
  const canUserEditProfile = (username === pageUsername);
  return canUserEditProfile ?
    <button onClick={() => window.location.href = '/editprofile'} type="button" className="profile-follow-button">Edit Profile</button> : <Follow className="profile-follow-button" followType="user" toFollow={pageUsername} initialState={follow} />
    ;
}

function ProfilePicture({ user_pic }) {
  return user_pic == null ? (
    <img src="/img/weave-icon.svg" className="profile-icon" alt="" />
  ) : (
      <img src={user_pic} className="profile-icon" alt="" />
    );
}

function UserPosts({ pageUsername, setContentView, contentView }) {

  const [route, setRoute] = useState("userposts/")
  const [element, setElem] = useState("post")

  useEffect(() => {
    if (contentView == 1) {
      setRoute("usercomments/")
      setElem("comment")
    }
    else {
      setRoute("userposts/")
      setElem("post")
    }
  }, [contentView])

  return (
    <div className="profile-choice">
      <div className="profile-buttons">
        <button type="button" className="profile-posts-button" onClick={(e) => setContentView(0)}>Posts</button>
        <button type="button" className="profile-interactions-button" onClick={(e) => setContentView(1)}>Interactions</button>
      </div>
      <div className="profile-display">
        {/*{contentView === 0 ? (
          <Feed route="userposts/" username={pageUsername} />
        ) : (
            <Feed route="usercomments/" username={pageUsername} elementType="comment" />
        )}*/}
        <Feed route={route} username={pageUsername} elementType={element} />
      </div>
    </div>
  );
}