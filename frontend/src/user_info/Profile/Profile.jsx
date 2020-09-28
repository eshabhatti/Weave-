import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import "./profile.css";

export default function Profile() {

    const [postsOrInt, updatePostOrInt] = useState("");


    displayPost = () => {
        updatePostOrInt(True);
    }

    displayInt = () => {
        updatePostOrInt(False);
    }

    return (
        <div className="profile-container">
            <Navbar expand="lg" bg="light" variant="light" sticky="top">
                <Navbar.Brand>Weave</Navbar.Brand>
                <Nav>
                    <Nav.Link>Messages</Nav.Link>
                    <Nav.Link>Notifications</Nav.Link>
                    <Nav.Link>Help</Nav.Link>
                </Nav>
            </Navbar>
            <div classname="profile-info">
                {/* pull user data */}
                <h1 className="profile-name">Name</h1>
                <p className="profile-username">Username</p>
                <button type="button" className="profile-follow-button" onClick={}>Follow</button>
                <p className="profile-followers"># Followers</p>
                <p className="profile-following"># Following</p>
                <h1 className="profile-bio-title">Bio</h1>
                <p className="profile-bio">Actual Bio</p>
                <h1 className="profile-about-title">About</h1>
                <p className="profile-about">About info</p>
            </div>
            <div className="profile-choice">
                <div className="profile-buttons">
                    <button type="button" className="profile-posts-button" onClick={displayPost}>Posts</button>
                    <button type="button" className="profile-interactions-button" onClick={displayInt}>Interactions</button>
                </div>
                <div className="profile-display">
                    {/* toggle between posts and int */}
                    <PostScreen active={postsOrInt} />
                    <InteractionScreen active={!postsOrInt} />
                </div>
            </div>
        </div>
    );
}