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
import SavedPosts from './user_info/SavedPosts/SavedPosts';
import PostPage from './user_info/Posts/PostPage';
import TopicPage from './user_info/Topics/TopicPage';
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
        <Route path="/savedposts">
          <SavedPosts />
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
		<Route path="/post/:post_id">
		  <PostPage />
		</Route>
		<Route path="/topic/:topic_name">
		  <TopicPage />
		</Route>
        <Route path="/">
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
