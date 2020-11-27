import React, { useState, useEffect } from "react";
import Linkify from 'react-linkify';

import "./post.css";

export default function Post({
  postId, userName, redesign, isMinimized
}) {

  const [errorMessage, updateErrorMessage] = useState("");
  const [postdata, setPostData] = useState([]);
  {/* keeps track if user has saved or voted */ }
  const [saveCheck, setSaved] = useState(0);
  const [voteCheck, setVoted] = useState(0);
  {/* current score of post */ }
  const [votes, setVotes] = useState(0);


  let access_token = localStorage.getItem('access_token');
  if (!access_token) {
    access_token = "";
  }

  const endpoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/post/" + postId;
  const statepoint = (process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/poststates/"

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
      if (data.error_message == "Blocked from content"){
	      window.location = "/blocked";
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
	
	if (access_token != ""){
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
        const { saved, voted } = data;
        setSaved(saved);
        setVoted(voted);
      }).catch(err => {
        console.error(err);
        alert(err);

      });
	}
    setVoted(postdata.score);
  }, [])

  const { topic_name, date_created, post_type, pic_path: src, title, content, creator, score} = postdata;

  {/* sends the votes to the server and receives the change in score */ }
  const vote = (value) => {
	  
	if (access_token == "") {
	  window.location = "/login"
	}  
	  
    setVoted(value);
    const body = {
      username: userName,
      type: '1',
      id: postId,
      vote: value,
    }
    fetch((process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/vote/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      // if (data.error_message) {
      //   updateErrorMessage(data.error_message);
      //   window.location = "/404"
      // }
      /* catches jwt errors that don't use the form "error_message:" */
      // if (data.msg) {
      //   window.location = "/login"
      // }
      const { score, voteState } = data;
      setVotes(score);
      setVoted(voteState);
    }).catch(err => {
      console.error(err);
    });
  };

  {/* sends the saved/unsaved postId to the server */ }
  const savePost = (value) => {
	
	if (access_token == "") {
	  window.location = "/login"
	}
	
    setSaved(value);
    const body = {
      username: userName,
      post: postId,
      type: value,
    }
    fetch((process.env.NODE_ENV === 'production' ? "http://weave.projectcarbon.io/server" : "http://localhost:5000") + "/save/", {
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

  /**
   * Save check and vote state should not be mutable states in React. Should be moved to post response
   */

  const postLink = "/post/" + postId;
  const profileLink = "/profile/" + creator;
  const topicLink = "/topic/" + topic_name;

  return PostComponent({ author: creator, title, text: content, topic_name, score: votes, isSaved: saveCheck, savePost, voteCheck, vote, isMinimized, postId, src });

}

function PostComponent({ isUpvoted, isDownVoted, score, title, text, author, isSaved, savePost, voteCheck, vote, isMinimized, postId, src, topic_name }) {
  const bookmarkFill = (isSaved == 1) ? "red" : "rgba(225, 225, 225, 1)";
  const bookmarkClicked = () => {
    console.log(isSaved);
    if (isSaved == -1) {
      savePost(1);
    } else {
      savePost(-1);
    }
  }
  let isUpvotedFlag = voteCheck == 1;
  let isDownVotedFlag = voteCheck == -1;
  const upvote = () => {
    vote(1);
  }
  const downvote = () => {
    vote(-1);
  }
  const containerClass = isMinimized ? "post-component-container post-component-container-collapsed" : "post-component-container";
  const onClick = () => {
    if (isMinimized) {
      window.location.href = "/post/" + postId;
    }
  }
  return (
    <div className={containerClass}>
      <VerticalVoteBar
        isUpvoted={isUpvotedFlag}
        isDownVoted={isDownVotedFlag}
        score={score}
        upvoteClick={() => upvote()}
        downvoteClick={() => downvote()}
      />
      <BookmarkIcon className="post-component-bookmark" fill={bookmarkFill} onClick={() => bookmarkClicked()} />
      <p className="post-component-topic"><a href={"/topic/" + topic_name}> w/{topic_name}</a></p>
      <div className="post-component-content" onClick={() => onClick()}>
        <p className="post-component-author"><a href = {"/profile/" + author}> @{author}</a></p>
        <h2 className="post-component-title">{title}</h2>
        <img src={src} className="post-component-image" />
		<Linkify>
			<p className="post-component-content-text">
			  {text}
			</p>
		</Linkify>
      </div>
    </div>
  )
}

function VerticalVoteBar({ score, isUpvoted, isDownVoted, upvoteClick, downvoteClick }) {
  const upVoteFill = isUpvoted ? "#A866B9" : "#9C9C9C";
  const downVoteFill = isDownVoted ? "#A866B9" : "#9C9C9C";
  return (
    <div className="post-component-vertical-vote-bar">
      <div className="post-component-vertical-vote-container">
        <VoteArrowIcon
          fill={upVoteFill}
          className="post-component-vote-arrow-upvote"
          onClick={() => { upvoteClick() }}
        />
        <p className="post-component-score">{score}</p>
        <VoteArrowIcon
          fill={downVoteFill}
          className="post-component-vote-arrow-downvote"
          onClick={() => { downvoteClick() }}
        />
      </div>
    </div>
  );
}

function VoteArrowIcon({ fill, className, onClick }) {

  return (
    <svg width="24" height="14" viewBox="0 0 24 14" xmlns="http://www.w3.org/2000/svg" className={className} onClick={() => onClick()}>
      <path d="M10.9393 13.0607C11.5251 13.6464 12.4749 13.6464 13.0607 13.0607L22.6066 3.51472C23.1924 2.92893 23.1924 1.97919 22.6066 1.3934C22.0208 0.807611 21.0711 0.807611 20.4853 1.3934L12 9.87868L3.51472 1.3934C2.92893 0.807611 1.97919 0.807611 1.3934 1.3934C0.807611 1.97919 0.807611 2.92893 1.3934 3.51472L10.9393 13.0607ZM10.5 11V12H13.5V11H10.5Z" fill={fill} />
    </svg>
  )
}

function BookmarkIcon({ fill, className, onClick }) {
  return (

    <svg viewBox="-58 0 404 404.54135" width="404pt" xmlns="http://www.w3.org/2000/svg" className={className} onClick={() => onClick()}>
      <path d="m277.527344 0h-267.257813c-5.523437 0-10 4.476562-10 10v374.527344c-.011719 7.503906 4.183594 14.378906 10.855469 17.804687 6.675781 3.429688 14.707031 2.832031 20.796875-1.550781l111.976563-80.265625 111.976562 80.269531c6.097656 4.367188 14.121094 4.960938 20.792969 1.535156 6.667969-3.425781 10.863281-10.292968 10.863281-17.792968v-374.527344c0-5.523438-4.480469-10-10.003906-10zm0 0" fill={fill}  />
    </svg>
  )
}