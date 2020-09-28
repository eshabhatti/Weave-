import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import "./profile.css";

export default function Profile() {

    const [postsOrInt, updatePostOrInt] = useState("");

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
            <link
                rel="stylesheet"
                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
                integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
                crossorigin="anonymous"
            />
            <Navbar expand="lg" bg="light" variant="light" sticky="top">
                <Navbar.Brand>Weave</Navbar.Brand>
                <img src="./img/weave-icon.svg" className="profile-icon" alt="" />
                <Nav className="mr-auto">
                    <Nav.Link>Messages</Nav.Link>
                    <Nav.Link>Notifications</Nav.Link>
                    <Nav.Link>Help</Nav.Link>
                </Nav>
            </Navbar>
            <div className="profile-container">
                <div classname="profile-info">
                    {/* pull user data */}
                    <h1 className="profile-name">Name</h1>
                    <p className="profile-username">Username</p>
                    {/* toggle active depending on who is viewing the page */}
                    <button type="button" className="profile-follow-button">Follow</button>
                    <p className="profile-followers"># Followers</p>
                    <p className="profile-following"># Following</p>
                    <h1 className="profile-bio-title">Bio</h1>
                    <p className="profile-bio">Actual Bio</p>
                    <h1 className="profile-about-title">About</h1>
                    <p className="profile-about">About info</p>
                </div>
                <div className="profile-choice">
                    <div className="profile-buttons">
                        <button type="button" className="profile-posts-button">Posts</button>
                        <button type="button" className="profile-interactions-button">Interactions</button>
                    </div>
                    <div className="profile-display">
                        {/* toggle between posts and int
                        <PostScreen active={postsOrInt} />
                        <InteractionScreen active={!postsOrInt} />
                        */}
                    </div>
                </div>
            </div>
        </div>
    );
}