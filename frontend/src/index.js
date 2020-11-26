import React from 'react';
import './index.css';
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import Login from "./pages/auth/Login/Login";
import Register from "./pages/auth/Register/Register";
import Profile from "./user_info/Profile/Profile";
import EditProfile from "./user_info/Profile/EditProfile";
import NotFound from "./error_pages/NotFound";
import Blocked from "./error_pages/Blocked";
import CreatePost from "./pages/post_info/CreatePost/CreatePost";
import SavedPosts from './user_info/SavedPosts/SavedPosts';
import PostPage from './pages/post_info/PostPage/PostPage';
import TopicPage from './pages/post_info/Topics/TopicPage';
import Timeline from './pages/post_info/Timeline/Timeline';
import Settings from "./user_info/Settings/Settings";
import Messages from "./user_info/Messages/MessagingPage";
import BlockedUsers from "./user_info/BlockedUsers/BlockedUsers";
import Chat from "./Chat/Chat"
//import ForgotPassword from "./auth/ForgotPassword/ForgotPassword";
// import PostPage from "./pages/PostsPage/PostsPage";

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
        <Route path="/profile">
          <Profile />
        </Route>
        <Route path="/editprofile">
          <EditProfile />
        </Route>
        <Route path="/chat/:username">
          <Chat />
        </Route>
		<Route path="/settings">
		  <Settings />
		</Route>
        <Route path="/timeline">
          <Timeline />
        </Route>
        <Route path="/createpost">
          <CreatePost />
        </Route>
        <Route path="/post/:post_id">
          <PostPage />
        </Route>
        <Route path="/topic/:topic_name">
          <TopicPage />
        </Route>
		<Route path="/blocked">
		  <Blocked />
		</Route>
		<Route path="/blockedusers">
		  <BlockedUsers />
		</Route>
		<Route path="/messages">
		  <Messages />
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
