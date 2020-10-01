import React from 'react';
import './index.css';
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import Login from "./auth/Login/Login";
import Register from "./auth/Register/Register";
import Profile from "./user_info/Profile/Profile"
import EditProfile from "./user_info/Profile/EditProfile"
import NotFound from "./error_pages/NotFound"
import Timeline from "./user_info/Timeline/Timeline"
//import ForgotPassword from "./auth/ForgotPassword/ForgotPassword";

function AppRouter() {
  return (
    <Router>
      <Switch>
	    <Route exact path="/">
          <Login />
        </Route>
        <Route path="/resetpassword">
          {/*<ForgotPassword />*/}
        </Route>
        <Route path="/register">
          <Register />
        </Route>
        <Route path="/login">
          <Login />
        </Route>
        <Route path="/profile/:username">
          <Profile />
        </Route>
		<Route path="/editprofile">
		  <EditProfile />
		</Route>
		<Route path="/timeline">
		  <Timeline />
		</Route>
		<Route>
		  <NotFound />
		</Route>
      </Switch>
    </Router>
  )
}

ReactDOM.render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>,
  document.getElementById('root')
);
