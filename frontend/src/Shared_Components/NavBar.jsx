import React, { useState, useEffect } from 'react';
import { Navbar, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import "./navbar.css";

export default function NavBar() {
	
  const [searchString, updateSearchString] = useState("");
  const [searchType, updateSearchType] = useState("profiles");
  
  const [errorMessage, updateErrorMessage] = useState("");
  const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;
  
  const search = () => {
	
	updateErrorMessage("");
	
	const body = {
      search_string: searchString,
      search_type: searchType,
    }	
	
	fetch((process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + '/search/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
	  body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      //TODO- check what data.msg does
      const errorMessage = data.error_message || data.msg;
      if (!data.error_message) {
        if (searchType == "profiles") {
		  window.location = "/profile/" + searchString;
		}
		else {
		  window.location = "/topic/" + searchString;
		}
      }
	  else {
	    updateErrorMessage("No Results.");
	  }
    }).catch(err => {
      console.error(err);
    });
  }
  
  return (
    <div>
      {/* Bootstrap Stylesheet */}
      <link
        rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
        integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
        crossOrigin="anonymous"
      />
      {/* Navbar */}
      <Navbar expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href="/timeline">
          <img src="/img/weave-icon.svg" width="50" height="50"
            className="d-inline-block align-top" alt="" />
        </Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="/messages">Messages</Nav.Link>
          <Nav.Link>Notifications</Nav.Link>
          <Nav.Link>Help</Nav.Link>
          <div className="search-form">
            <input 
              value={searchString}
              className="search-input"
              onChange={e => {
                updateSearchString(e.target.value);
                updateErrorMessage("");
              }}
            />
            <select 
              id="type" 
              className="search-selection" 
              onChange={e => {
                updateSearchType(e.target.value)
                updateErrorMessage("");
              }}
            >
              <option className="search-option" value="profiles">profiles</option>
              <option className="search-option" value="topics">topics</option>
            </select>
            <button className="search-button" onClick={(e) => search()}>Search</button>
            {errObject}
          </div>
        </Nav>
      </Navbar>
    </div>
  )
  //return CustomNavbar();
}

function ErrorBubble({ message }) {
  return (
    <div className="search-error-bubble">
      <p className="search-error-message">{message}</p>
    </div>
  )
}
