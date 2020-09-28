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

//import ForgotPassword from "./auth/ForgotPassword/ForgotPassword";

function AppRouter() {
  return (
    <Router>
      <Switch>
        <Route path="/resetpassword">
          {/*<ForgotPassword />*/}
        </Route>
        <Route path="/register">
          <Register />
        </Route>
        <Route path="/login">
          <Login />
        </Route>
        <Route path="/profile">
          <Profile />
        </Route>
        <Route path="/">
          <Login />
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
