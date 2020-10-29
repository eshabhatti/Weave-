import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';

// import components
import NavBar from '../../../Shared_Components/NavBar';
import Sidebar from '../../../Shared_Components/Sidebar/Sidebar';
import Post from '../../../Shared_Components/Post/Post';
import Feed from "../../../Shared_Components/Feed/Feed";
import CommentCreator from '../CommentCreator/CommentCreator';

export default function Profile() {
  const { post_id: pagePost } = useParams();

  const [errorMessage, updateErrorMessage] = useState("");
  const [postdata, setPostData] = useState([]);
  const [commentsData, setCommentsData] = useState([]);
  {/* keeps track if user has saved or voted */ }
  const [saveCheck, setSaved] = useState(0);
  const [voteCheck, setVoted] = useState(0);
  {/* current score of post */ }
  const [votes, setVotes] = useState(0);

  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  const endpoint = "http://localhost:5000/post/" + pagePost;
  const votepoint = "http://localhost:5000/vote/"
  const savepoint = "http://localhost:5000/save/"
  const statepoint = "http://localhost:5000/poststates/"
  const commentpoint = "http://localhost:5000/postcomments/"

  {/* renders the post with fetch data and the states of the save and voting buttons */ }
  useEffect(() => {
    fetch(endpoint, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
    }).then(response => response.json()).then(data => {
      if (data.error_message) {
        updateErrorMessage(data.error_message);
        window.location = "/404"
      }
      /* catches jwt errors that don't use the form "error_message:" */
      if (data.msg) {
        window.location = "/login"
      }
      setPostData(data);
      const { score } = data;
      setVotes(score);
    }).catch(err => {
      console.error(err);

    });

    const body = {
      post_id: pagePost,
    }

    fetch(statepoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      if (data.error_message) {
        updateErrorMessage(data.error_message);
        window.location = "/404"
      }
      /* catches jwt errors that don't use the form "error_message:" */
      if (data.msg) {
        window.location = "/login"
      }
      /* setStateData(data); */
      const { saved, voted } = data;
      setSaved(saved);
      setVoted(voted);
    }).catch(err => {
      console.error(err);
      alert(err);

    });
  }, [])

  const { topic_name, date_created, post_type, pic_path, title, content, creator } = postdata;

  {/* sends the votes to the server and receives the change in score */ }
  const vote = (value) => {
    setVoted(value);
    const body = {
      type: '1',
      id: pagePost,
      vote: value,
    }
    fetch(votepoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      if (data.error_message) {
        updateErrorMessage(data.error_message);
        window.location = "/404"
      }
      /* catches jwt errors that don't use the form "error_message:" */
      if (data.msg) {
        window.location = "/login"
      }
      const { change } = data;
      setVotes(votes + change);
    }).catch(err => {
      console.error(err);

    });
  };

  {/* sends the saved/unsaved postId to the server */ }
  const savePost = (value) => {
    setSaved(value);
    const body = {
      post: pagePost,
      type: value,
    }
    fetch(savepoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      if (data.error_message) {
        updateErrorMessage(data.error_message);
        window.location = "/404"
      }
      /* catches jwt errors that don't use the form "error_message:" */
      if (data.msg) {
        window.location = "/login"
      }
    }).catch(err => {
      console.error(err);

    });
  };

  return (
    <div>
      <p>Need the post information in a different format than this</p>
      <Post postId={pagePost} redesign={true} />
      <CommentCreator postId={pagePost} />
      <p>Comments:</p>
	  <div className="comments-container" >
		<Feed route="postcomments/" post_id={pagePost} elementType="comment" />
	  </div>
    </div>

  );
}