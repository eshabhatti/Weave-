import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import "./timeline.css";

export default function Timeline() {
	const [postContent, updatePostContent] = useState("");
	const onSubmit = (event) => {}
	
    return (
		<div>
			<div>
				{/* Bootstrap Stylesheet */}
				<link
					rel="stylesheet"
					href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
					integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
					crossorigin="anonymous"
				/>
				<Navbar expand="lg" bg="dark" variant="dark" sticky="top">
					<Navbar.Brand href="/login">
						<img src="/img/weave-icon.svg" width="50" height="50"
							 className="d-inline-block align-top" alt="" />
					</Navbar.Brand>
					<Nav className="mr-auto">
						<Nav.Link>Messages</Nav.Link>
						<Nav.Link>Notifications</Nav.Link>
						<Nav.Link>Help</Nav.Link>
					</Nav>
				</Navbar>
			</div>
			<div className="post-container">
			  <form className="post-form">
				  <label className="post-form-label">Post Text</label>
				  <textarea
					value={postContent}
					onChange={e => {
					  updatePostContent(e.target.value);
					}}
					className="post-form-input" />
				  <button type="submit" className="post-submit-btn" onClick={(e) => onSubmit(e)}>Create Post</button>
			  </form>
			</div>
		</div>
    );
}