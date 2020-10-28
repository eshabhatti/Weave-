import React, { useEffect } from "react";
import "./sidebar.css";

export default function Sidebar() {
  const [xPosition, setX] = React.useState(-180);

  useEffect(() => {
    setX(0);
  }, []);

  const toggleMenu = () => {
    if (xPosition < 0) {
      setX(0);
    } else {
      setX(-180);
    }
  };

  //delete JWT token and refresh
  const logout = () => {
    const access_token = localStorage.getItem('access_token');
    const logoutEndpoint = "http://localhost:5000/logout";
    fetch(logoutEndpoint, {
      method: "DELETE",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
    }).then(response => response.json()).then(data => {
      const { refresh_token } = data;
      const endpoint2 = "http://localhost:5000/logout2";
      fetch(endpoint2, {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + refresh_token
        },
      }).then(response => response.json()).then(data => {
        localStorage.clear("access_token");
        localStorage.clear("refresh_token");
        window.location = "../"
      }).catch(err => {
        console.error(err);
        alert("error: check console for details");
      });
    }).catch(err => {
      console.error(err);
      alert("error: check console for details");
    });

  };

  return (
    <>
      <div
        className="sidebar"
        style={{ transform: `translatex(${xPosition}px)` }}
      >
        <button
          onClick={() => toggleMenu()}
          className="profile-toggle-menu"
          style={{
            transform: `translate(${180}px, 20vh)`
          }}
        ></button>
        <div className="side-bar-menu">
          {/* These need to link to actual pages eventually */}
          <h1 className="side-bar-heading">Explore your web:</h1>
          <a href="/timeline" className="side-bar-selection">Your timeline</a> <br />
          <a href="/createpost" className="side-bar-selection">Create a post</a> <br />
          <a href="/savedposts" className="side-bar-selection">Saved posts</a> <br />
		  <a href="/settings" className="side-bar-selection">Settings</a> <br />
          <button className="side-bar-logout" onClick={(e) => logout(e)}>Logout</button>
        </div>
      </div>
    </>
  );
}