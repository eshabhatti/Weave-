import React from 'react';
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import "./navbar.css";

export default function NavBar() {
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
      <Navbar expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href="/timeline">
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
  //return CustomNavbar();
}

function CustomNavbar() {
  return (
    <div className="navbar-wrapper">
      <div className="navbar">
        <div className="navbar-heading">
          <img src="./img/weave-icon.svg" className="navbar-icon" />
          <h3 className="navbar-title">weave</h3>
        </div>
        <NavSearch />
        <NavButtonGroup />
      </div>
    </div>
  )
}

function NavSearch() {
  return (
    <div className="navbar-search">

    </div>
  )
}

function NavButtonGroup() {
  return (
    <div className="navbar-button-group">

    </div>
  )
}