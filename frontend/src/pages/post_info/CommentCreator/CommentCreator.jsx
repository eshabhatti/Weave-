import React, { useState, useEffect } from "react";

import "./commentcreator.css";

export default function CommentCreator({
  postId
}) {
  const [commentContent, updateCommentContent] = useState("");
  const [errorMessage, updateErrorMessage] = useState("");
  const [successMessage, updateSuccessMessage] = useState("");

  const errObject = errorMessage !== "" ? <ErrorBubble message={errorMessage} /> : null;
  const successObject = successMessage != "" ? <SuccessBubble message={successMessage} /> : null;

  const access_token = localStorage.getItem('access_token');
  if (access_token == null) {
    window.location = "/login"
  }

  const commentpoint = "http://localhost:5000/createcomment/"
  const onSubmit = (event) => {
    event.preventDefault();
    const body = {
      content: commentContent,
      post_id: postId,
    }
    fetch(commentpoint, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
      },
      body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
      if (data.error_message) {
        updateErrorMessage(data.error_message);
      }
      updateSuccessMessage("comment added!");
      /* catches jwt errors that don't use the form "error_message:" */
      if (data.msg) {
        window.location = "/login"
      }
    }).catch(err => {
      console.error(err);
      alert(err);
    });
  }

  return (
    <div>
      <h1 className="comment-header">Comment:</h1>
      <div className="comment-container">
        <form className="comment-form">

          <label className="comment-form-label">Comment Text</label>
          <textarea
            value={commentContent}
            onChange={e => {
              updateCommentContent(e.target.value);
            }}
            className="comment-form-input-body"
          />
          
          <button type="submit" className="comment-submit-btn" onClick={(e) => onSubmit(e)}>Add Comment</button>
          {errObject}
          {successObject}
        </form>
      </div>
    </div>
  );
}

function ErrorBubble({ message }) {
  return (
    <div className="comment-error-bubble">
      <p className="comment-error-message">{message}</p>
    </div>
  )
}

function SuccessBubble({ message }) {
  return (
    <div className="comment-success-bubble">
      <p className="comment-error-message">{message}</p>
    </div>
  )
}