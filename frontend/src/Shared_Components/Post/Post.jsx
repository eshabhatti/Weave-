import React, { useState, useEffect } from "react";
import Collapsible from 'react-collapsible';

import "./post.css";

export default function Post({
  postId, userName, redesign
}) {

  const [errorMessage, updateErrorMessage] = useState("");
  const [postdata, setPostData] = useState([]);
  {/* keeps track if user has saved or voted */ }
  const [saveCheck, setSaved] = useState(0);
  const [voteCheck, setVoted] = useState(0);
  {/* current score of post */ }
  const [votes, setVotes] = useState(0);


  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  const endpoint = "http://localhost:5000/post/" + postId;
  const votepoint = "http://localhost:5000/vote/"
  const savepoint = "http://localhost:5000/save/"
  const statepoint = "http://localhost:5000/poststates/"

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
      username: userName,
      post_id: postId,
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
  const vote = (value, arrow) => {
    setVoted(arrow);
    const body = {
      username: userName,
      type: '1',
      id: postId,
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
      username: userName,
      post: postId,
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

  const postLink = "/post/" + postId;
  const profileLink = "/profile/" + creator;
  const topicLink = "/topic/" + topic_name;

  if (redesign)
    return PostComponent({});


  return (
    <div>
      {/* <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link> */}
      <Collapsible className="post-content-header" openedClassName="post-content-header-open" triggerClassName="post-trigger" triggerOpenedClassName="post-trigger-open" trigger={title}>
        <div className="post-content-container">
          <div className="post-vote-container">

            {voteCheck > 0 ? (
              <i class="fa fa-arrow-circle-up" style={{ fontSize: '36px', color: 'red' }} onClick={() => vote(1, 0)} ></i>

            ) : (
                <i class="fa fa-arrow-circle-up" style={{ fontSize: '36px' }} onClick={() => vote(1, 1)} ></i>
              )}
            <p className="post-vote-score">{votes}</p>
            {voteCheck < 0 ? (
              <i class="fa fa-arrow-circle-down" style={{ fontSize: '36px', color: 'red' }} onClick={() => vote(-1, 0)} ></i>
            ) : (
                <i class="fa fa-arrow-circle-down" style={{ fontSize: '36px' }} onClick={() => vote(-1, -1)} ></i>
              )}
          </div>
          <div className="post-text-container">

            <p className="post-text"><a href={profileLink}>{creator}</a></p>
            <p className="post-text">{date_created}</p>
            <p className="post-text"><a href={topicLink}>{topic_name}</a></p>
            <h1 className="post-title">{title}</h1>
            <p className="post-content">{content}</p>
            <p><a href={postLink}>View Comments</a></p>
            {saveCheck === -1 ? (
              <button className="post-save-button" onClick={() => savePost(1)}>Save</button>
            ) : (
                <button className="post-save-button" onClick={() => savePost(-1)}>Unsave</button>
              )}
          </div>
          <div className="post-pic-container">
            {pic_path ? <img src={pic_path} className="post-pic" alt="" /> : null}
          </div>
        </div>
      </Collapsible>
    </div>
  );

}

function PostComponent() {
  return (
    <div className="post-component-container">
      <VerticalVoteBar />
      <div className="post-component-content">
        <p>@realuser2020</p>
        <h2>Post Title</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quod autem principium officii quaerunt, melius quam Pyrrho; Nunc agendum est subtilius. Sed ad haec, nisi molestum est, habeo quae velim. Duo Reges: constructio interrete. Vos autem cum perspicuis dubia debeatis illustrare, dubiis perspicua conamini tollere. Hanc ergo intuens debet institutum illud quasi signum absolvere.
        </p>
      </div>
    </div>
  )
}

function VerticalVoteBar({ votes, isUpvoted, isDownVoted }) {
  const upVoteFill = isUpvoted ? "#A866B9" : "#9C9C9C";
  const downVoteFill = isDownVoted ? "#A866B9" : "#9C9C9C";
  return (
    <div className="post-component-vertical-vote-bar">
      <div className="post-component-vertical-vote-container">
        <VoteArrowIcon
          fill={upVoteFill}
          className="post-component-vote-arrow-upvote"
          onClick={() => { }}
        />
        <p className="post-component-score">121</p>
        <VoteArrowIcon
          fill={downVoteFill}
          className="post-component-vote-arrow-downvote"
          onClick={() => { }}
        />
      </div>
    </div>
  );
}

function VoteArrowIcon({ fill, className }) {

  return (
    <svg width="24" height="14" viewBox="0 0 24 14" xmlns="http://www.w3.org/2000/svg" className={className}>
      <path d="M10.9393 13.0607C11.5251 13.6464 12.4749 13.6464 13.0607 13.0607L22.6066 3.51472C23.1924 2.92893 23.1924 1.97919 22.6066 1.3934C22.0208 0.807611 21.0711 0.807611 20.4853 1.3934L12 9.87868L3.51472 1.3934C2.92893 0.807611 1.97919 0.807611 1.3934 1.3934C0.807611 1.97919 0.807611 2.92893 1.3934 3.51472L10.9393 13.0607ZM10.5 11V12H13.5V11H10.5Z" fill={fill} />
    </svg>
  )
}