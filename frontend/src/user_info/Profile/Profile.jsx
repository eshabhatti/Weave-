import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import "./profile.css";

export default function Profile() {

    const [postsOrInt, updatePostOrInt] = useState("");
    const [errorMessage, updateErrorMessage] = useState("");
    const [xPosition, setX] = React.useState(-250);

    const toggleMenu = () => {
        if (xPosition < 0) {
        setX(0);
        } else {
        setX(-250);
        }
    };

    React.useEffect(() => {
        setX(0);
    }, []);

    {/* testing with user in sql tests */}
    const username = "realuser2";
    const endpoint = "http://localhost:5000/profile/" + username;
    const userdata;
    fetch(endpoint, {
    method: "GET",
    headers: {
        'Content-Type': 'application/json'
    },
    }).then(response => response.json()).then(data => {
    if (data.error_message) {
        updateErrorMessage(data.error_message);
    }
    userdata = data;
    }).catch(err => {
    console.error(err);
    alert("error: check console for details");
    });
    const { user_bio, user_pic, follower_count, first_name, last_name, date_joined } = userdata;

    {/*
    displayPost = () => {
        updatePostOrInt(true);
    }

    displayInt = () => {
        updatePostOrInt(false);
    }
    */}

    return (
        <div>
            {/* Bootstrap Stylesheet */}
            <link
                rel="stylesheet"
                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
                integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
                crossorigin="anonymous"
            />
            {/* Navbar */}
            <Navbar expand="lg" bg="dark" variant="dark" sticky="top">
                <Navbar.Brand href="login">
                    <img src="./img/weave-icon.svg" width="50" height="50"
                         className="d-inline-block align-top" alt="" />
                </Navbar.Brand>
                <Nav className="mr-auto">
                    <Nav.Link>Messages</Nav.Link>
                    <Nav.Link>Notifications</Nav.Link>
                    <Nav.Link>Help</Nav.Link>
                </Nav>
            </Navbar>
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
                        <div>
                            <h1>Menu</h1>
                        </div>
                    </div>
                </React.Fragment>
                <div className="profile-container">
                    {/* Contains all the info of user */}
                    <div className="profile-info">
                        {/* pull user data */}
                        <img src="./img/weave-icon.svg" classname="profile-icon" alt="" />
                        <h1 className="profile-name">{first_name} {last_name}</h1>
                        <p className="profile-username">{username}</p>
                        {/* toggle active depending on who is viewing the page */}
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