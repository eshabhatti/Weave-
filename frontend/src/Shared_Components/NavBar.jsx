import React from 'react';
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';


export default function NavBar(){
    return(
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
    )
}