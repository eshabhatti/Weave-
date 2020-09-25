import React, { useState } from "react";
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';

import "./timeline.css";

export default function Timeline() {
    return (
        <Navbar expand="lg" bg="light" variant="light" sticky="top">
            <Navbar.Brand>Weave</Navbar.Brand>
            <Nav>
                <Nav.Link>Messages</Nav.Link>
                <Nav.Link>Notifications</Nav.Link>
                <Nav.Link>Help</Nav.Link>
            </Nav>
        </Navbar>
    );
}