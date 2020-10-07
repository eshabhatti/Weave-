import React, { useState, useEffect } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import { useParams, Route } from 'react-router-dom';
import NavBar from "../../Shared_Components/NavBar";
import Post from "../../Shared_Components/Post";

import "./profile.css";

export default function Profile() {
    const { username } = useParams();
    const [postsOrInt, updatePostOrInt] = useState("");
    const [errorMessage, updateErrorMessage] = useState("");
    const [xPosition, setX] = React.useState(-250);
    const [userdata, setUserData] = useState([]);
    const [postdata, setPostData] = useState([])

    const canUserEditProfile = (userdata !== [] && userdata.username === username);

    const access_token = localStorage.getItem('access_token');
    if (access_token == null) {
        window.location = "/login"
    }

    const toggleMenu = () => {
        if (xPosition < 0) {
            setX(0);
        } else {
            setX(-250);
        }
    };

    useEffect(() => {
        setX(0);
    }, []);

    const logout = () => {

        /* The frontend needs to blacklist the refresh tokens and access tokens. */
        /* This request blacklists access tokens. */
        const access_token = localStorage.getItem('access_token');
        const endpoint1 = "http://localhost:5000/logout";
        fetch(endpoint1, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            },
        }).then(response => response.json()).then(data => {
            const { access_token } = data;
            console.log(access_token);
            //localStorage.setItem('data', data);
            localStorage.setItem('access_token', access_token);
            /* This request blacklists refresh tokens. */
            const refresh_token = localStorage.getItem('refresh_token');
            const endpoint2 = "http://localhost:5000/logout2";
            fetch(endpoint2, {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + refresh_token
                },
            }).then(response => response.json()).then(data => {
                const { refresh_token } = data;
                console.log(refresh_token);
                //localStorage.setItem('data', data);
                localStorage.setItem('refresh_token', refresh_token);
                window.location = "../"
            }).catch(err => {
                console.error(err);
                alert("error: check console for details");
            });
            // localStorage.setItem('refresh_token', null); // May have to call /logout2
            // window.location = "../"
        }).catch(err => {
            console.error(err);
            alert("error: check console for details");
        });

    };

    const postpoint = "http://localhost:5000/userposts/";
    {/* testing with user in sql tests */ }
    const endpoint = "http://localhost:5000/profile/" + username;
    useEffect(() => {
        fetch(endpoint, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            },
        }).then(response => response.json()).then(data => {
            if (data.error_message) {
                updateErrorMessage(data.error_message);
                window.location = "/404"
            }
            /* catches jwt errors that don't use the form "error_message:" */
            if (data.msg) {
                window.location = "/login"
            }
            setUserData(data);
        }).catch(err => {
            console.error(err);
        });

        const body = {
            username: username,
            start: 0,
            end: 5,
        }

        //    const postpoint = "http://localhost:5000/userposts/";
        fetch(postpoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access_token
            },
            body: JSON.stringify(body)
        }).then(response => response.json()).then(data => {
            if (data.error_message) {
                updateErrorMessage(data.error_message);
                window.location = "/404"
            }
            /* catches jwt errors that don't use the form "error_message:" */
            if (data.msg) {
                window.location = "/login"
            }
            const { pull_list: post_ids } = data;
            //let post_ids = pull_list.split(",");
            console.log(post_ids)
            setPostData(post_ids);
        }).catch(err => {
            console.error(err);
        });
    }, [])
    const { user_bio, user_pic, follower_count, first_name, last_name, date_joined } = userdata;

    {/*
  displayPost = () => {
    updatePostOrInt(true);
  }

  displayInt = () => {
    updatePostOrInt(false);
  }
  */}

    const editProfileBtn = canUserEditProfile ? <button onClick={() => window.location.href = '/editprofile'} type="button" className="profile-follow-button">Edit Profile</button> : null;

    return (
        <div>
            <NavBar />
            <link
                rel="stylesheet"
                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
                integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
                crossorigin="anonymous"
            />
            <div className="profile-container">
                {/* Sidebar */}
                <React.Fragment>
                    <div
                        className="profile-side-bar"
                        style={{
                            transform: `translatex(${xPosition}px)`,
                            width: 250,
                            minHeight: 800,
                        }}
                    >
                        <button
                            onClick={() => toggleMenu()}
                            className="profile-toggle-menu"
                            style={{
                                transform: `translate(${250}px, 20vh)`
                            }}
                        ></button>
                        <div className="side-bar-menu">
                            {/* These need to link to actual pages eventually */}
                            <h1 className="side-bar-heading">Explore your web:</h1>
                            <a href="../timeline/" className="side-bar-selection">Your timeline</a> <br />
                            <a href="" className="side-bar-selection">Saved posts</a> <br />
                            <button className="side-bar-logout" onClick={(e) => logout(e)}>Logout</button>
                        </div>
                    </div>
                </React.Fragment>
                <div className="profile-container">
                    {/* Contains all the info of user */}
                    <div className="profile-info">
                        {/* pull user data */}
                        {user_pic == null ? (
                            <img src="/img/weave-icon.svg" className="profile-icon" alt="" />
                        ) : (
                                <img src={user_pic} className="profile-icon" alt="" />
                            )}
                        <h1 className="profile-name">{first_name} {last_name}</h1>
                        <p className="profile-username">{username}</p>
                        {/* toggle active depending on who is viewing the page */}
                        {editProfileBtn}
                        <button type="button" className="profile-follow-button">Follow</button>
                        <p className="profile-followers">{follower_count} Followers</p>
                        <p className="profile-following"># Following</p>
                        <h1 className="profile-bio-title">Bio</h1>
                        <p className="profile-bio">{user_bio}</p>
                        <h1 className="profile-about-title">About</h1>
                        <p className="profile-about">{date_joined}</p>
                    </div>
                    <div className="profile-choice">
                        <div className="profile-buttons">
                            <button type="button" className="profile-posts-button">Posts</button>
                            <button type="button" className="profile-interactions-button">Interactions</button>
                        </div>
                        {/* will contain the toggle display of users */}
                        <div className="profile-display">
                            {Posts(postdata, username)}
                            {/* <Post postId="002" userName="realuser2" /> */}
                            {/* toggle between posts and int
                                <PostScreen active={postsOrInt} />
                                <InteractionScreen active={!postsOrInt} />
                            */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

//post_ids: list of post ID's
// could return before completion
function Posts(post_ids, username) {
    let postComponents = [];
    post_ids.forEach(id => {
        postComponents.push(<Post userName={username} postId={id} />)
    });
    return postComponents;
}